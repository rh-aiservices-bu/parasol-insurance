package org.parasol.ai;

import jakarta.enterprise.context.SessionScoped;

import org.parasol.model.ClaimBotQuery;

import dev.langchain4j.service.SystemMessage;
import dev.langchain4j.service.UserMessage;
import io.quarkiverse.langchain4j.RegisterAiService;
import io.smallrye.mutiny.Multi;

@RegisterAiService
@SessionScoped
public interface ClaimService {
    @SystemMessage("""
        You are a helpful, respectful and honest assistant named "Parasol Assistant".
        You will be given a claim summary, references to provide you with information, and a question. You must answer the question based as much as possible on this claim with the help of the references.
        Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
        """
    )
    @UserMessage("""
        Claim Summary:
        {{query.claim}}

        Question: {{query.query}}
    """)
    Multi<String> chat(ClaimBotQuery query);
}
