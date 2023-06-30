<template>
    <div>
      <div class="chat-message" v-for="message in messages" :key="message.id">
        <div class="sender">{{ message.sender }}</div>
        <div class="content">{{ message.message }}</div>
        <div class="timestamp">{{ formatTimestamp(message.timestamp) }}</div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ChatMessages',
    props: {
      messages: {
        type: Array,
        required: true
      }
    },
    methods: {
      formatTimestamp(timestamp) {
        return moment(timestamp).format('YYYY-MM-DD HH:mm:ss');
      }
    }
  };
  </script>
  
  <style scoped>
  .chat-message {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-bottom: 10px;
  }
  
  .sender {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .content {
    margin-bottom: 5px;
  }
  
  .timestamp {
    font-size: 12px;
    color: #888;
  }
  </style>
  