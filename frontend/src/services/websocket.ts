import { Alert } from "./api";

class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout = 1000;
  private alertCallbacks: ((alert: Alert) => void)[] = [];

  connect(token: string) {
    if (this.ws) {
      this.ws.close();
    }

    const wsUrl = `ws://localhost:7001/ws/alerts?token=${token}`;
    console.log("Connecting to WebSocket:", wsUrl);
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log("WebSocket connected successfully");
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      try {
        console.log("Received WebSocket message:", event.data);
        const alert = JSON.parse(event.data) as Alert;
        this.alertCallbacks.forEach((callback) => callback(alert));
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    this.ws.onclose = (event) => {
      console.log("WebSocket disconnected", event.code, event.reason);
      this.attemptReconnect(token);
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }

  private attemptReconnect(token: string) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(
        `Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`
      );
      setTimeout(
        () => this.connect(token),
        this.reconnectTimeout * this.reconnectAttempts
      );
    } else {
      console.error("Max reconnection attempts reached");
    }
  }

  onAlert(callback: (alert: Alert) => void) {
    this.alertCallbacks.push(callback);
    return () => {
      this.alertCallbacks = this.alertCallbacks.filter((cb) => cb !== callback);
    };
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.alertCallbacks = [];
  }
}

export const websocketService = new WebSocketService();
