import axios from 'axios'

const API_URL = '/api/progress'

export async function getProgress(userId) {
  const res = await axios.get(`${API_URL}?user_id=${userId}`)
  return res.data
}

export async function updateProgress(userId, topic, amount = 1) {
  // Debug: Logge den Request-Body, der an das Backend geschickt wird
  console.log('[updateProgress] Request payload:', { user_id: userId, topic, amount })
  const res = await axios.post(`${API_URL}/update`, {
    user_id: userId,
    topic,
    amount
  })
  return res.data
}
