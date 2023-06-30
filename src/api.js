import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export async function createMessage(message, recipient) {
  try {
    const response = await api.post(`/messages/${recipient}`, { message });
    return response.data;
  } catch (error) {
    throw new Error('Failed to create message');
  }
}

export async function getMessages(username) {
  try {
    const response = await api.get(`/messages/${username}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to get messages');
  }
}
