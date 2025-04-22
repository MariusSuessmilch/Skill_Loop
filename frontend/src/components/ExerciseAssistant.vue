<template>
  <div class="exercise-assistant">
    <form @submit.prevent="askAssistant">
      <input
        v-model="question"
        type="text"
        placeholder="Frage den KI-Assistenten zu dieser Aufgabe"
        :disabled="loading"
        class="assistant-input"
      />
      <button type="submit" :disabled="loading || !question" class="assistant-btn coding-main-btn">Fragen</button>
    </form>
    <div v-if="loading" class="assistant-loading">
      <span class="loading-spinner"></span> Antwort wird geladen...
    </div>
    <div v-if="answer" class="assistant-answer">
      <strong>Assistent:</strong>
      <span v-html="renderedAnswer"></span>
    </div>
    <div v-if="error" class="assistant-error">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import { marked } from 'marked'

export default {
  name: 'ExerciseAssistant',
  props: {
    code: { type: String, required: true },
    exercise: { type: Object, required: false }
  },
  data() {
    return {
      question: '',
      answer: '',
      loading: false,
      error: ''
    }
  },
  computed: {
    renderedAnswer() {
      return this.answer ? marked.parse(this.answer) : ''
    }
  },
  methods: {
    async askAssistant() {
      this.loading = true;
      this.error = '';
      this.answer = '';
      try {
        const res = await axios.post('/api/assistant/', {
          code: this.code,
          question: this.question,
          exercise: this.exercise ? this.exercise.prompt : undefined,
          role: 'assistant',
          instruction: 'Sei ein hilfreicher Tutor. Antworte auf Fragen zum Code und zur Aufgabe, aber gib niemals die Lösung oder den vollständigen Code. Gib Tipps, Hinweise, Erklärungen und stelle Verständnisfragen.'
        })
        this.answer = res.data.answer;
        this.question = '';
      } catch (e) {
        this.error = 'Beim Laden der Antwort ist ein Fehler aufgetreten.';
      }
      this.loading = false;
    }
  }
}
</script>

<style scoped>
.exercise-assistant {
  margin: 2em 0 0 0;
  padding: 1.2em;
  background: #232836;
  border-radius: 8px;
  color: #fff;
  box-shadow: 0 2px 12px #0002;
}
.assistant-input {
  width: 70%;
  padding: 0.7em;
  border-radius: 4px;
  border: none;
  background: #181b26;
  color: #fff;
  margin-right: 1em;
}
.assistant-btn {
  padding: 0.7em 1.5em;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}
.coding-main-btn {
  background: #2563eb;
  color: #fff;
  font-size: 1em;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(37,99,235,0.08);
}
.coding-main-btn:disabled {
  background: #3b4252;
  cursor: not-allowed;
}
.coding-main-btn:hover:not(:disabled) {
  background: #1d4ed8;
}
.assistant-loading {
  margin-top: 1em;
  color: #38bdf8;
}
.assistant-answer {
  margin-top: 1em;
  background: #181b26;
  padding: 1em;
  border-radius: 6px;
  color: #fff;
  max-width: 100%;
  overflow-x: auto;
  word-break: break-word;
}
.assistant-answer pre {
  background: #232836;
  color: #38bdf8;
  padding: 0.6em;
  border-radius: 5px;
  font-size: 0.98em;
  overflow-x: auto;
}
.assistant-error {
  margin-top: 1em;
  color: #ff6b6b;
}
</style>
