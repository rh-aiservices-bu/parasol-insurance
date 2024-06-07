package org.parasol.resources;

import org.parasol.ai.ClaimService;
import org.parasol.model.ClaimBotQuery;
import org.parasol.model.ClaimBotQueryResponse;

import io.quarkus.logging.Log;
import io.quarkus.websockets.next.OnClose;
import io.quarkus.websockets.next.OnOpen;
import io.quarkus.websockets.next.OnTextMessage;
import io.quarkus.websockets.next.WebSocket;
import io.quarkus.websockets.next.WebSocketConnection;

import io.smallrye.mutiny.Multi;

@WebSocket(path = "/ws/query")
public class ClaimWebsocketChatBot {
    private final ClaimService bot;

    public ClaimWebsocketChatBot(ClaimService bot) {
        this.bot = bot;
    }

    @OnOpen
    public void onOpen(WebSocketConnection connection) {
        Log.infof("Websocket connection %s opened", connection.id());
    }

    @OnClose
    public void onClose(WebSocketConnection connection) {
        Log.infof("Websocket connection %s closed", connection.id());
    }

    @OnTextMessage
    public Multi<ClaimBotQueryResponse> onMessage(ClaimBotQuery query) {
        return bot.chat(query)
          .invoke(response -> Log.debugf("Got chat response: %s", response))
          .map(resp -> new ClaimBotQueryResponse("token", resp, ""));
    }
}


