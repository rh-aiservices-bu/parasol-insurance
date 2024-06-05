package org.parasol.resources;

import org.parasol.ai.ClaimService;
import org.parasol.model.ClaimBotQuery;
import org.parasol.model.ClaimBotQueryResponse;

import io.quarkus.websockets.next.OnOpen;
import io.quarkus.websockets.next.OnTextMessage;
import io.quarkus.websockets.next.WebSocket;
import io.smallrye.mutiny.Multi;

@WebSocket(path = "/ws/query")
public class ClaimWebsocketChatBot {
        private final ClaimService bot;

    public ClaimWebsocketChatBot(ClaimService bot) {
        this.bot = bot;
    }

    @OnOpen
    public void onOpen() {
        System.out.println("Websocket opened");
    }
    @OnTextMessage
    public Multi<ClaimBotQueryResponse> onMessage(ClaimBotQuery query) {
        return bot.chat(query.claim(), query.query())
          .map(resp -> new ClaimBotQueryResponse("token", resp, ""));
    }
}


