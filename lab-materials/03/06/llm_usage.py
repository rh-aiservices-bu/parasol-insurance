from langchain.evaluation import load_evaluator
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.llms import VLLMOpenAI

INFERENCE_SERVER_URL = "http://granite-7b-instruct-predictor.ic-shared-llm.svc.cluster.local:8080"
MAX_NEW_TOKENS = 512
TOP_P = 0.95
TEMPERATURE = 0.01
PRESENCE_PENALTY = 1.03

def infer_with_template(input_text, template, max_tokens = MAX_NEW_TOKENS):
    llm = VLLMOpenAI(
        openai_api_key="EMPTY",
        openai_api_base= f"{INFERENCE_SERVER_URL}/v1",
        model_name="granite-7b-instruct",
        max_tokens=max_tokens,
        top_p=TOP_P,
        temperature=TEMPERATURE,
        presence_penalty=PRESENCE_PENALTY,
        streaming=False,
        verbose=False,
    )
    
    prompt = PromptTemplate(input_variables=["car_claim"], template=template)
    
    conversation = prompt | llm
    
    return conversation.invoke(input=input_text)
    
def similarity_metric(predicted_text, reference_text):
    embedding_model = HuggingFaceEmbeddings()
    evaluator = load_evaluator("embedding_distance", embeddings=embedding_model)
    distance_score = evaluator.evaluate_strings(prediction=predicted_text, reference=reference_text)
    return 1-distance_score["score"]
    
if __name__ == '__main__':
    with open('example_text.txt') as f:
        input_text = f.read()
    
    with open('template.txt') as f:
        template = f.read()
    
    infer_with_template(input_text, template)