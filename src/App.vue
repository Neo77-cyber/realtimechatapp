<template>
  <div id="app">
    <ChatMessages :messages="messages" />
    <ChatInput @send="sendMessage" />
  </div>
</template>

<script>
import ChatMessages from './components/ChatMessages.vue';
import ChatInput from './components/ChatInput.vue';

export default {
  name: 'App',
  components: {
    ChatMessages,
    ChatInput
  },
  data() {
    return {
      messages: []
    };
  },
  methods: {
    sendMessage(message) {
  // Send the message to the backend WebSocket
  this.websocketService.send(message);

  // Update the messages array with the new message
  this.messages.push({
    sender: 'current_user', // Replace with the sender's username
    message: message,
    timestamp: new Date()
  });
}
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
