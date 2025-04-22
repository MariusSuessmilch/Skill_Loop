<template>
  <div class="app-bg">
    <aside class="app-sidebar">
      <div class="sidebar-logo-title">
        <img src="/logo-skillloop.svg" alt="Skill Loop Logo" class="sidebar-logo" />
        <span class="sidebar-rotated">Skill Loop</span>
      </div>
      <div class="sidebar-progress">
        <!-- No progress here, moved to top right -->
      </div>
    </aside>
    <div class="app-main-content">
      <ProgressPanel :generalLevel="generalLevel" :topicLevels="topicLevels" />
      <main>
        <CodingTutor v-model:generalLevel="generalLevel" v-model:topicLevels="topicLevels" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CodingTutor from './components/CodingTutor.vue'
import ProgressPanel from './components/ProgressPanel.vue'

const generalLevel = ref(0)
const topicLevels = ref({})
</script>

<style>
html, body, #app, .app-bg {
  min-height: 100vh;
  height: 100%;
  margin: 0;
  padding: 0;
  background: #10131a;
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
}
.app-bg {
  min-height: 100vh;
  background: #10131a;
  display: flex;
}
.app-sidebar {
  width: 170px;
  min-width: 170px;
  background: linear-gradient(180deg, #232836 70%, #10131a 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  box-shadow: 2px 0 10px rgba(44,114,252,0.07);
  padding-top: 2.5em;
}
.sidebar-logo-title {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2em;
  width: 100%;
}
.sidebar-logo {
  width: 56px;
  height: 56px;
  margin-bottom: 0.7em;
  margin-top: 0.5em;
  filter: drop-shadow(0 2px 8px #0a0d13);
}
.sidebar-rotated {
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  font-family: 'Orbitron', 'Inter', 'Segoe UI', Arial, sans-serif;
  font-weight: 900;
  font-size: 2.7em;
  color: #7cc4fa;
  letter-spacing: 2px;
  text-shadow: 0 2px 12px #0a0d13;
  user-select: none;
}
.sidebar-progress {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.app-main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  max-width: 100vw;
  box-sizing: border-box;
  position: relative;
}
main {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
  min-height: 70vh;
  width: 100%;
  max-width: 100vw;
  box-sizing: border-box;
}
</style>
