export default class WebSocketService {
    constructor() {
      this.socket = null;
    }
  
    connect(url) {
      this.socket = new WebSocket(url);
  
      this.socket.addEventListener('open', () => {
        console.log('WebSocket connection established');
      });
  
      this.socket.addEventListener('message', () => {
        // Handle the received message, update the UI, etc.
      });
  
      this.socket.addEventListener('close', () => {
        console.log('WebSocket connection closed');
      });
  
      this.socket.addEventListener('error', (error) => {
        console.error('WebSocket error:', error);
      });
    }
  
    send(message) {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify(message));
      }
    }
  
    disconnect() {
      if (this.socket && this.socket.readyState !== WebSocket.CLOSED) {
        this.socket.close();
      }
    }
  }
  