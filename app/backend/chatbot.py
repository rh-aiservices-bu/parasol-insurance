import time
import os
from collections.abc import Generator
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import RetrievalQA
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import VLLMOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Milvus
from milvus_retriever_with_score_threshold import MilvusRetrieverWithScoreThreshold
from queue import Empty, Queue
from threading import Thread


class QueueCallback(BaseCallbackHandler):
    """Callback handler for streaming LLM responses to a queue."""

    def __init__(self, q, logger):
        self.q = q
        self.logger = logger

    def on_llm_new_token(self, token: str, **kwargs: any) -> None:
        data = {"type": "token", "token": token}
        self.q.put(data)

    def on_llm_end(self, *args, **kwargs: any) -> None:
        return self.q.empty()


class Chatbot:
    def __init__(self, config, logger):
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        self.logger = logger
        self.config = config

        self.model_kwargs = {"trust_remote_code": True}
        self.embeddings = HuggingFaceEmbeddings(
            model_name="nomic-ai/nomic-embed-text-v1",
            model_kwargs=self.model_kwargs,
            show_progress=False,
        )

        self.rag_template = """<s>[INST] <<SYS>>
                        You are a helpful, respectful and honest assistant named "Parasol Assistant".
                        You will be given a claim summary, references to provide you with information, and a question. You must answer the question based as much as possible on this claim with the help of the references.
                        Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

                        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
                        <</SYS>>

                        Claim Summary:
                        {claim}

                        References: 
                        {{context}}

                        Question: {{question}} [/INST]"""

        self.rag_template_no_summary = """<s>[INST] <<SYS>>
                        You are a helpful, respectful and honest assistant named "Parasol Assistant".
                        You will be given a context to provide you with information, and a question. You must answer the question based as much as possible on this context. Please don't mention you are using a context in your response.
                        Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

                        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
                        <</SYS>>

                        Context: 
                        {context}

                        Question: {question} [/INST]"""


    def format_sources(self, input_list):
        sources = ""
        if len(input_list) != 0:
            sources += input_list[0].metadata["source"] + ', page: ' + str(input_list[0].metadata["page"])
            page_list = [input_list[0].metadata["page"]]
            for item in input_list:
                if item.metadata["page"] not in page_list: # Avoid duplicates
                    page_list.append(item.metadata["page"])
                    sources += ', ' + str(item.metadata["page"])
        return sources

    def stream(self, query, claim) -> Generator:
        # A Queue is needed for Streaming implementation
        q = Queue()
        job_done = object()

        llm = VLLMOpenAI(
            openai_api_key="EMPTY",
            openai_api_base=self.config["INFERENCE_SERVER_URL"],
            model_name=self.config["MODEL_NAME"],
            max_tokens=int(self.config["MAX_TOKENS"]),
            top_p=float(self.config["TOP_P"]),
            temperature=float(self.config["TEMPERATURE"]),
            presence_penalty=float(self.config["PRESENCE_PENALTY"]),
            streaming=True,
            verbose=False,
            callbacks=[QueueCallback(q, self.logger)],
        )

        """ conversation_chain = ConversationChain(
            llm=llm,
            prompt=self.PROMPT,
            verbose=True
        ) """

        retriever = MilvusRetrieverWithScoreThreshold(
            embedding_function=self.embeddings,
            collection_name=self.config["MILVUS_COLLECTION"],
            collection_description="",
            collection_properties=None,
            connection_args={
                "host": self.config.get("MILVUS_HOST", "default_host"),
                "port": self.config.get("MILVUS_PORT", "default_port"),
                "user": self.config.get("MILVUS_USERNAME", "default_username"),
                "password": self.config.get("MILVUS_PASSWORD", "default_password"),
            },
            consistency_level="Session",
            search_params=None,
            k=int(self.config.get("MAX_RETRIEVED_DOCS", 4)),
            score_threshold=float(self.config.get("SCORE_THRESHOLD", 0.99)),
            metadata_field="metadata",
            text_field="page_content",
        )

        # Inject claim summary into the prompt
        if claim != "":
            prompt_template = self.rag_template.format(claim=claim)
        else:
            prompt_template = self.rag_template_no_summary
        prompt = PromptTemplate.from_template(prompt_template)

        # Instantiate RAG chain
        rag_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True,
        )

        # Create a function to call - this will run in a thread
        def task():
            resp = rag_chain.invoke({"query": query, "claim": claim})
            sources = self.format_sources(resp['source_documents'])
            if len(sources) != 0:
                data = {"type": "source", "source": sources}
                q.put(data)
            q.put(job_done)

        # Create a thread and start the function
        t = Thread(target=task)
        t.start()

        # Get each new item from the queue and yield for our generator
        while True:
            try:
                next_item = q.get(True, timeout=1)
                if next_item is job_done:
                    break
                if isinstance(next_item, dict):
                    yield next_item
            except Empty:
                continue
