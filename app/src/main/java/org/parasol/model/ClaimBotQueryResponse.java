package org.parasol.model;

import com.fasterxml.jackson.annotation.JsonCreator;

public record ClaimBotQueryResponse(String type, String token, String source) {

        @JsonCreator
        public ClaimBotQueryResponse {
        }

}
