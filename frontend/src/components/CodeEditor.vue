<template>
  <div>
    <textarea v-model="code" rows="10" cols="60"></textarea>
    <button @click="runCode">Ausführen</button>
    <div v-if="output">
      <h4>Ausgabe:</h4>
      <pre>{{ output }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { executeCode } from '../api'

const code = ref('')
const output = ref('')

async function runCode() {
  const res = await executeCode(code.value)
  output.value = res.output
}
</script>
