import axios from 'axios'

export async function executeCode(code) {
  const res = await axios.post('/api/code/execute', { code })
  return res.data
}

export async function streamExercise({ language, skill_level, skill }) {
  const res = await axios.post('/api/exercises/', { language, skill_level, skill })
  return res.data
}

export async function generateExercise(language, skill_level, skill) {
  const res = await axios.post('/api/exercises/', { language, skill_level, skill })
  return res.data
}

export async function getFeedback(code, exercise) {
  // Send full exercise object, not just description
  const res = await axios.post('/api/feedback/', { code, exercise })
  return res.data // Expects { feedback, solved }
}
