<template>
  <VueMonacoEditor
    :value="modelValue"
    language="python"
    theme="vs-dark"
    :options="editorOptions"
    class="monaco-editor-container"
    :style="{ height: '640px', minHeight: '320px', width: '100%' }"
    @update:value="onUpdate"
  />
</template>

<script setup>
import VueMonacoEditor from '@guolao/vue-monaco-editor'
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  modelValue: String
})

const emit = defineEmits(['update:modelValue'])

function onUpdate(val) {
  emit('update:modelValue', val)
}

const editorOptions = {
  fontSize: 16,
  minimap: { enabled: false },
  automaticLayout: true,
  scrollBeyondLastLine: false,
  wordWrap: 'on',
  lineNumbers: 'on',
  tabSize: 4,
  bracketPairColorization: { enabled: true }
}
</script>

<style scoped>
.monaco-editor-container {
  border-radius: 8px;
  overflow-x: auto;
  overflow-y: hidden;
  border: 1px solid #232836;
  margin-bottom: 1.2em;
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
  background: #181c24;
}
</style>
