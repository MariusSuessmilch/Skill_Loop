<template>
  <div class="coding-tutor">
    <ProgressPanel :generalLevel="generalLevel" :topicLevels="topicLevels" />
    <div v-if="missingUserId" class="error-block">
      <p style="color: red;">Kein Nutzer eingeloggt. Fortschritt kann nicht geladen werden.</p>
    </div>

    <transition name="fade">
      <div v-if="loadingExercise" class="fullscreen-loading">
        <div class="spinner"></div>
        <div class="loading-text">Aufgabe wird generiert ...</div>
      </div>
    </transition>

    <div v-if="exercise.code && !loadingExercise" class="main-flex">
      <!-- Sidebar mit Aufgabenbeschreibung -->
      <aside class="exercise-sidebar">
        <div class="exercise-description">
          <h2 style="color: #facc15;">Aufgabenstellung</h2>
          <div v-html="renderedExercise" class="exercise-markdown"></div>
        </div>
      </aside>
      <!-- Hauptbereich: Editor -->
      <section class="editor-section">
        <MonacoCodeEditor v-model="userCode" />
        <div class="editor-buttons">
          <button class="ct-primary-btn" @click="runCode" :disabled="loadingRun">Ausführen</button>
          <button class="ct-primary-btn" @click="submitCode" :disabled="loadingFeedback">Abgabe + Feedback</button>
          <button class="ct-primary-btn" @click="fetchExercise" :disabled="loadingExercise || streaming">Neue Aufgabe</button>
        </div>
        <div v-if="runOutput" class="run-output-block">
          <h3>Output</h3>
          <pre>{{ runOutput }}</pre>
        </div>
        <ExerciseAssistant :code="userCode" :exercise="exercise" />
        <div v-if="feedback" class="feedback-drawer" :class="{ open: feedbackDrawerOpen }">
          <div class="feedback-drawer-header">
            <!-- <h2 class="feedback-title">KI Feedback</h2> -->
          </div>
          <div v-if="loadingFeedback" class="feedback-loading">
            <span class="loading-spinner"></span> Feedback wird geladen...
          </div>
          <div v-else v-html="renderedFeedback" class="feedback-markdown"></div>
          <div v-if="solved && !loadingFeedback" class="solved-feedback">
            <span class="solved-badge">🎉 Aufgabe korrekt gelöst!</span>
            <button class="ct-primary-btn next-ex-btn" @click="nextExercise">Nächste Aufgabe anzeigen</button>
          </div>
        </div>
        <button v-if="feedback && !feedbackDrawerOpen" class="open-feedback-btn ct-primary-btn" @click="showFeedbackAndScroll">
          Feedback anzeigen
        </button>
      </section>
    </div>

    <div v-if="error" class="error-block">
      <p style="color: red;">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import { streamExercise, getFeedback, executeCode } from '../api'
import { marked } from 'marked'
import MonacoCodeEditor from './MonacoCodeEditor.vue'
import ExerciseAssistant from './ExerciseAssistant.vue'
import ProgressPanel from './ProgressPanel.vue'
import { getProgress, updateProgress } from '../api/progress'
import hljs from 'highlight.js/lib/core'
import python from 'highlight.js/lib/languages/python'
import 'highlight.js/styles/github-dark.css'

hljs.registerLanguage('python', python)

marked.setOptions({
  breaks: true,
  gfm: true,
  headerIds: false,
  mangle: false,
  langPrefix: 'language-',
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  }
})

const curriculum = [
  'Integer-Datentyp',                  // 1
  'Float-Datentyp',                    // 2
  'String-Datentyp',                   // 3
  'Boolean-Datentyp',                  // 4
  'Addition (+)',                      // 5
  'Subtraktion (–)',                   // 6
  'Multiplikation (*)',                // 7
  'Division (/)',                      // 8
  'Ganzzahliger Rest (%)',             // 9
  'Potenzierung (**)',                 // 10
  'Vergleichsoperator ==',             // 11
  'Vergleichsoperator !=',             // 12
  'Vergleichsoperator < und >',        // 13
  'Vergleichsoperator <= und >=',      // 14
  'Logisches "and"',                  // 15
  'Logisches "or"',                   // 16
  'Logisches "not"',                  // 17
  'if',                                // 18
  'elif',                              // 19
  'else',                              // 20
  'for‑Schleife',                      // 21
  'while‑Schleife',                    // 22
  'break und continue',                // 23
  'Liste – append(), insert(), remove()', // 24
  'Liste – sort(), reverse(), Slicing',   // 25
  'Listen‑Comprehension',              // 26
  'Dict-Grundoperationen – keys(), values(), items()', // 27
  'Dict – get(), Standard‑Werte, Verschachtelung',     // 28
  'Funktion mit def, Rückgabewert',    // 29
  'Funktion – Parameter (positional, keyword)', // 30
  'Klasse – __init__ und Attribute',   // 31
  'Klasse – Methoden',                 // 32
  'Klasse – Vererbung und Overriding'  // 33
];

const topicMap = [
  'variables',    // 1: Integer-Datentyp
  'variables',    // 2: Float-Datentyp
  'variables',    // 3: String-Datentyp
  'variables',    // 4: Boolean-Datentyp
  'operators',    // 5: Addition (+)
  'operators',    // 6: Subtraktion (–)
  'operators',    // 7: Multiplikation (*)
  'operators',    // 8: Division (/)
  'operators',    // 9: Ganzzahliger Rest (%)
  'operators',    // 10: Potenzierung (**)
  'operators',    // 11: Vergleichsoperator ==
  'operators',    // 12: Vergleichsoperator !=
  'operators',    // 13: Vergleichsoperator < und >
  'operators',    // 14: Vergleichsoperator <= und >=
  'operators',    // 15: Logisches "and"
  'operators',    // 16: Logisches "or"
  'operators',    // 17: Logisches "not"
  'if_else',      // 18: if
  'if_else',      // 19: elif
  'if_else',      // 20: else
  'loops',        // 21: for‑Schleife
  'loops',        // 22: while‑Schleife
  'loops',        // 23: break und continue
  'lists',        // 24: Liste – append(), insert(), remove()
  'lists',        // 25: Liste – sort(), reverse(), Slicing
  'lists',        // 26: Listen‑Comprehension
  'dictionaries', // 27: Dict-Grundoperationen – keys(), values(), items()
  'dictionaries', // 28: Dict – get(), Standard‑Werte, Verschachtelung
  'functions',    // 29: Funktion mit def, Rückgabewert
  'functions',    // 30: Funktion – Parameter (positional, keyword)
  'classes',      // 31: Klasse – __init__ und Attribute
  'classes',      // 32: Klasse – Methoden
  'classes'       // 33: Klasse – Vererbung und Overriding
];

// Mapping der deutschen Begriffe auf Backend-konforme Topics
const topicKeywordToBackend = {
  'Integer-Datentyp': 'variables',
  'Float-Datentyp': 'variables',
  'String-Datentyp': 'variables',
  'Boolean-Datentyp': 'variables',
  'Addition (+)': 'operators',
  'Subtraktion (–)': 'operators',
  'Multiplikation (*)': 'operators',
  'Division (/)': 'operators',
  'Ganzzahliger Rest (%)': 'operators',
  'Potenzierung (**)': 'operators',
  'Vergleichsoperator ==': 'operators',
  'Vergleichsoperator !=': 'operators',
  'Vergleichsoperator < und >': 'operators',
  'Vergleichsoperator <= und >=': 'operators',
  'Logisches "and"': 'operators',
  'Logisches "or"': 'operators',
  'Logisches "not"': 'operators',
  'if': 'if_else',
  'elif': 'if_else',
  'else': 'if_else',
  'for‑Schleife': 'loops',
  'while‑Schleife': 'loops',
  'break und continue': 'loops',
  'Liste – append(), insert(), remove()': 'lists',
  'Liste – sort(), reverse(), Slicing': 'lists',
  'Listen‑Comprehension': 'lists',
  'Dict-Grundoperationen – keys(), values(), items()': 'dictionaries',
  'Dict – get(), Standard‑Werte, Verschachtelung': 'dictionaries',
  'Funktion mit def, Rückgabewert': 'functions',
  'Funktion – Parameter (positional, keyword)': 'functions',
  'Klasse – __init__ und Attribute': 'classes',
  'Klasse – Methoden': 'classes',
  'Klasse – Vererbung und Overriding': 'classes'
}

// Funktion, um aus dem Curriculum-Text das Backend-Topic zu bestimmen
function getBackendTopic(curriculumItem) {
  return topicKeywordToBackend[curriculumItem] || null
}

export default {
  name: 'CodingTutor',
  components: { MonacoCodeEditor, ExerciseAssistant, ProgressPanel },
  props: {
    modelValue: {
      type: Number,
      default: 1
    },
    topicLevels: {
      type: Object,
      default: () => ({})
    },
    userId: {
      type: String,
      default: 'testuser-fake-123'
    }
  },
  data() {
    return {
      userCode: '',
      exercise: {},
      feedback: '',
      loadingExercise: false,
      streaming: false,
      loadingRun: false,
      loadingFeedback: false,
      runOutput: '',
      solved: false,
      error: '',
      generalLevel: 1,
      missingUserId: false,
      feedbackDrawerOpen: true
    }
  },
  computed: {
    renderedExercise() {
      let desc = this.exercise.description
        ? this.exercise.description.replace(/\n{3,}/g, '\n\n').replace(/(^\s+|\s+$)/g, '')
        : ''
      // Füge Überschrift hinzu, falls keine vorhanden ist
      if (desc && !/^\s*#/.test(desc)) {
        desc = '## Aufgabe\n' + desc
      }
      return marked.parse(desc)
    },
    renderedFeedback() {
      if (!this.feedback) return ''
      return marked.parse(this.feedback)
    }
  },
  watch: {
    generalLevel(newVal) {
      this.$emit('update:generalLevel', newVal)
    },
    modelValue(newVal) {
      this.generalLevel = newVal
    },
    topicLevels: {
      handler(newVal) {
        this.$emit('update:topicLevels', newVal)
      },
      deep: true
    }
  },
  methods: {
    async fetchExercise() {
      this.loadingExercise = true
      this.exercise = {}
      this.userCode = ''
      this.feedback = ''
      this.runOutput = ''
      this.solved = false
      this.error = ''
      this.feedbackDrawerOpen = false
      try {
        const res = await streamExercise({
          language: 'de',
          skill_level: this.generalLevel,
          skill: curriculum[this.generalLevel - 1] || ''
        })
        this.exercise = res
        if (res && res.code) {
          this.userCode = res.code
        }
        this.loadingExercise = false
      } catch (err) {
        this.error = 'Fehler beim Laden der Aufgabe.'
        this.loadingExercise = false
      }
    },
    async runCode() {
      this.loadingRun = true
      try {
        const res = await executeCode(this.userCode)
        this.runOutput = res.output
        this.loadingRun = false
      } catch (err) {
        this.error = 'Fehler beim Ausführen des Codes.'
        this.loadingRun = false
      }
    },
    async submitCode() {
      this.loadingFeedback = true
      this.feedbackDrawerOpen = true
      try {
        // Pass full exercise object to getFeedback
        const res = await getFeedback(this.userCode, this.exercise)
        this.feedback = res.feedback
        this.solved = res.solved
        this.loadingFeedback = false
        this.$nextTick(() => {
          const el = this.$el.querySelector('.feedback-drawer')
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' })
          }
        })
        if (res.solved && this.userId) {
          // Logging: Zeige Curriculum-Text und Topic-Mapping
          const currentCurriculum = curriculum[this.generalLevel - 1]
          const mappedTopic = getBackendTopic(currentCurriculum)
          console.log('[Progress-Update] generalLevel:', this.generalLevel, '| curriculum:', currentCurriculum, '| mappedTopic:', mappedTopic)
          // Logging: Zeige UserId und Amount
          console.log('[Progress-Update] userId:', this.userId, '| amount:', 1)
          if (!mappedTopic) {
            this.error = 'Interner Fehler: Topic Mapping ungültig.'
            return
          }
          // Logging: Zeige den Request-Body vor dem Senden
          console.log('[Progress-Update] Request payload:', { user_id: this.userId, topic: mappedTopic, amount: 1 })
          await updateProgress(this.userId, mappedTopic, 1)
          await this.fetchProgress()
        } else {
          await this.fetchProgress()
        }
      } catch (err) {
        this.error = 'Fehler beim Abrufen des Feedbacks.'
        this.loadingFeedback = false
        // Logging: Zeige Fehlerobjekt
        console.error('[submitCode] Fehler:', err)
      }
    },
    async nextExercise() {
      this.feedback = ''
      this.solved = false
      this.userCode = ''
      this.runOutput = ''
      this.feedbackDrawerOpen = false
      await this.fetchExercise()
    },
    async fetchProgress() {
      try {
        const res = await getProgress(this.userId)
        this.generalLevel = res.general_level
        this.$emit('update:generalLevel', this.generalLevel)
        this.$emit('update:topicLevels', res.topic_levels)
      } catch (err) {
        this.error = 'Fehler beim Laden des Fortschritts.'
      }
    },
    showFeedbackAndScroll() {
      this.feedbackDrawerOpen = true
      this.$nextTick(() => {
        const el = this.$el.querySelector('.feedback-drawer')
        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
      })
    },
  },
  mounted() {
    if (!this.userId) {
      this.missingUserId = true
      return
    }
    this.fetchExercise()
    this.fetchProgress()
  }
}
</script>

<style scoped>
.coding-tutor {
  width: 100vw;
  min-height: 100vh;
  background: #10131a;
  padding-bottom: 2em;
  box-sizing: border-box;
}
.main-flex {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 2.2em;
  width: 100%;
  max-width: 100vw;
  box-sizing: border-box;
}
.exercise-sidebar {
  min-width: 260px;
  max-width: 460px;
  width: 30vw;
  word-break: break-word;
  overflow-wrap: anywhere;
  box-sizing: border-box;
  background: #181c24;
  border-radius: 10px;
  padding: 2em 1.2em 1.2em 1.2em;
  box-shadow: 0 2px 10px rgba(44,114,252,0.07);
  position: sticky;
  top: 2em;
  align-self: flex-start;
  height: fit-content;
}
.exercise-description {
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  overflow-y: visible;
  /* Ermögliche automatisches Wachsen bei viel Inhalt */
  max-height: none;
  height: auto;
}
.exercise-markdown {
  max-width: 100%;
  overflow-x: auto;
  overflow-y: visible;
  word-break: break-word;
  white-space: pre-line;
  color: #fff;
  font-size: 1.13em;
  line-height: 1.19;
  margin-bottom: 0;
  background: #232836;
  border-radius: 8px;
  padding: 1.2em 1.4em 1.2em 1.4em;
  box-shadow: 0 2px 10px rgba(44,114,252,0.07);
  max-height: none;
  height: auto;
}
.exercise-markdown p,
.exercise-markdown ul,
.exercise-markdown ol {
  margin-top: 0.3em;
  margin-bottom: 0.3em;
}
.exercise-markdown li {
  margin-bottom: 0.1em;
}
.exercise-markdown h1,
.exercise-markdown h2,
.exercise-markdown h3,
.exercise-markdown h4,
.exercise-markdown h5,
.exercise-markdown h6 {
  margin-top: 0.2em;
  margin-bottom: 0.16em;
  font-weight: 700;
}
.exercise-markdown h1 {
  font-size: 1.3em;
}
.exercise-markdown h2 {
  font-size: 1.17em;
}
.exercise-markdown code, .exercise-markdown pre {
  background: #181c24;
  color: #7cc4fa;
  font-size: 1em;
  padding: 0.2em 0.5em;
  border-radius: 5px;
  overflow-x: auto;
  display: block;
  white-space: pre;
  word-break: normal;
  max-width: 100%;
  box-sizing: border-box;
}
.exercise-markdown pre {
  padding: 0.7em 1em;
  margin: 0.6em 0;
}
.exercise-description h2 {
  color: #facc15;
  font-size: 1.4em;
  font-weight: 700;
  margin-bottom: 0.7em;
  letter-spacing: 0.01em;
}
.feedback-drawer {
  position: relative;
  left: unset;
  bottom: unset;
  width: 100%;
  max-width: 100vw;
  background: #232836;
  box-shadow: 0 -2px 24px rgba(44,114,252,0.13);
  border-radius: 18px;
  z-index: 10;
  padding: 2.2em 2.5em 2.5em 2.5em;
  min-height: 220px;
  max-height: 58vh;
  overflow-y: auto;
  color: #fff;
  display: flex;
  flex-direction: column;
  gap: 1.1em;
  margin-top: 2em;
}
.feedback-drawer.open {
  display: flex;
}
@media (max-width: 700px) {
  .feedback-drawer {
    padding: 1.2em 0.6em 1.2em 0.6em;
  }
}
/* Modern, auffällige Buttons wie der "Frage"-Button */
.ct-primary-btn, .editor-buttons button, .open-feedback-btn, .next-ex-btn {
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 0.85em 2em;
  font-size: 1.13em;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(37,99,235,0.10);
  transition: background 0.2s, box-shadow 0.2s, transform 0.08s;
  margin: 0.2em 0.6em 0.2em 0;
  outline: none;
  letter-spacing: 0.01em;
}
.ct-primary-btn:active, .editor-buttons button:active, .open-feedback-btn:active, .next-ex-btn:active {
  background: #1d4ed8;
  transform: scale(0.98);
}
.ct-primary-btn:focus, .editor-buttons button:focus, .open-feedback-btn:focus, .next-ex-btn:focus {
  box-shadow: 0 0 0 3px rgba(37,99,235,0.18);
}
.ct-primary-btn:disabled, .editor-buttons button:disabled, .open-feedback-btn:disabled, .next-ex-btn:disabled {
  background: #3b4252;
  color: #cbd5e1;
  cursor: not-allowed;
  box-shadow: none;
}
.editor-section {
  flex: 1 1 0;
  width: 100vw;
  max-width: 100vw;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  padding-right: 0;
  margin-top: 32px;
}
.monaco-editor-container {
  width: 100% !important;
  width: 100vw;
  max-width: 100vw;
  box-sizing: border-box;
  overflow-x: auto;
  padding-right: 0;
  background: #151a22;
  border-radius: 8px;
  transition: box-shadow 0.2s;
  box-shadow: 0 2px 12px rgba(44,114,252,0.08);
}
@media (max-width: 1100px) {
  .editor-section {
    padding-right: 0;
    margin-top: 18px;
  }
  .monaco-editor-container {
    padding-right: 0;
  }
}
@media (max-width: 700px) {
  .editor-section {
    padding-right: 0;
    margin-top: 8px;
  }
  .monaco-editor-container {
    padding-right: 0;
  }
}
.run-output-block {
  background: #181c24;
  color: #f8fafc !important;
  border-radius: 8px;
  padding: 1.1em 1.5em 1em 1.5em;
  margin-top: 1.1em;
  margin-bottom: 0.6em;
  font-size: 1.16em;
  font-family: 'Fira Mono', 'Consolas', 'Menlo', monospace;
  box-shadow: 0 2px 10px rgba(44,114,252,0.07);
  word-break: break-word;
  white-space: pre-line;
  max-width: 100%;
  overflow-x: auto;
}
.run-output-block pre {
  background: transparent;
  color: #f8fafc !important;
  margin: 0;
  padding: 0;
  font-size: 1em;
  font-family: inherit;
}
.solved-feedback {
  display: flex;
  align-items: center;
  gap: 2.2em;
  margin-top: 1.2em;
  margin-bottom: 0.5em;
}
.solved-badge {
  background: #059669;
  color: #fff;
  font-size: 1.14em;
  font-weight: 700;
  border-radius: 8px;
  padding: 0.8em 1.6em;
  margin-right: 0.7em;
  box-shadow: 0 2px 8px rgba(5,150,105,0.12);
  letter-spacing: 0.01em;
}
.next-ex-btn {
  margin-left: 2.5em !important;
  min-width: 230px;
  box-shadow: 0 2px 8px rgba(37,99,235,0.10);
}
</style>
