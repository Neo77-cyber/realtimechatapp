<template>
    <div class="chat-input">
      <input type="text" v-model="messageText" placeholder="Type your message..." @keydown.enter="sendMessage">
      <button @click="sendMessage">Send</button>
    </div>
  </template>
  
  <script>
  import WebSocketService from '../services/WebSocketService';
  import { createMessage } from '../api';
  
  export default {
    name: 'ChatInput',
    data() {
      return {
        messageText: '',
        websocketService: null,
        recipient: 'recipient_username', // Replace with the recipient's username
      };
    },
    created() {
      this.websocketService = new WebSocketService();
      this.websocketService.connect('ws://localhost:8000/ws');
    },
    beforeUnmount() {
      this.websocketService.disconnect();
    },
    methods: {
      sendMessage() {
        if (this.messageText.trim() !== '') {
          createMessage(this.messageText, this.recipient)
            .then(() => {
              this.websocketService.send(this.messageText);
              this.messageText = '';
            })
            .catch((error) => {
              console.error(error);
            });
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .chat-input {
    display: flex;
    align-items: center;
    padding: 10px;
    background-color: #f1f1f1;
  }
  
  .chat-input input[type="text"] {
    flex: 1;
    padding: 5px;
    border: none;
    border-radius: 3px;
    margin-right: 5px;
  }
  
  .chat-input button {
    padding: 5px 10px;
    background-color: #4caf50;
    color: #fff;
    border: none;
    border-radius: 3px;
    cursor: pointer;
  }
  
  .chat-input button:hover {
    background-color: #45a049;
  }
  </style>
  