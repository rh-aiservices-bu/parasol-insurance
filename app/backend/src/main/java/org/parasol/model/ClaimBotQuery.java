package org.parasol.model;

import com.fasterxml.jackson.annotation.JsonCreator;

public record ClaimBotQuery(String claim, String query) {

        @JsonCreator
        public ClaimBotQuery {
        }

}
