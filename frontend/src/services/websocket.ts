// In production, this should be the deployed backend WS URL
const WS_BASE_URL = import.meta.env.VITE_BACKEND_WS_URL || 'ws://localhost:8000';

let ws: WebSocket | null = null;

export const connectWebSocket = (clientId: string, onMessage: (event: MessageEvent) => void): WebSocket => {
  // Ensure we close any existing connection before opening a new one
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.close();
  }

  ws = new WebSocket(`${WS_BASE_URL}/ws/${clientId}`);

  ws.onopen = (event) => {
    console.log('WebSocket connected:', event);
  };

  ws.onmessage = (event) => {
    onMessage(event);
  };

  ws.onclose = (event) => {
    console.log('WebSocket disconnected:', event);
    // Optional: Implement reconnect logic here
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  return ws;
};

export const disconnectWebSocket = (currentWs: WebSocket | null) => {
  if (currentWs) {
    currentWs.close();
    ws = null;
    console.log('WebSocket manually disconnected.');
  }
};

export const sendWebSocketMessage = (message: string) => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(message);
  } else {
    console.warn('WebSocket is not open. Message not sent.');
  }
};