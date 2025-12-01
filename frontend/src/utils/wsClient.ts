type Message = {
  type: string;
  [k: string]: any;
};

export class WSClient {
  ws: WebSocket | null = null;
  roomId: string;
  onMessage: (msg: Message) => void = () => {};
  url: string;

  constructor(roomId: string, onMessage?: (msg: Message) => void) {
    this.roomId = roomId;
    this.url = (import.meta.env.VITE_WS_BASE || "ws://localhost:8000/api") + `/ws/${roomId}`;
    if (onMessage) this.onMessage = onMessage;
  }

  connect() {
    this.ws = new WebSocket(this.url);
    this.ws.onopen = () => console.log("ws open", this.url);
    this.ws.onmessage = (ev) => {
      try {
        const msg = JSON.parse(ev.data);
        this.onMessage(msg);
      } catch (e) {
        console.error("invalid ws message", e);
      }
    };
    this.ws.onclose = () => console.log("ws closed");
    this.ws.onerror = (e) => console.error("ws error", e);
  }

  send(obj: Message) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return;
    this.ws.send(JSON.stringify(obj));
  }

  close() {
    this.ws?.close();
    this.ws = null;
  }
}
