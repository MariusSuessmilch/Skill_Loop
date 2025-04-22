<template>
  <div class="progress-circle-container">
    <div class="progress-circle" :style="{ background: circleBg }">
      <svg viewBox="0 0 100 100" class="circle-svg">
        <circle cx="50" cy="50" r="44" class="circle-bg" />
        <circle
          cx="50"
          cy="50"
          r="44"
          class="circle-bar"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="circumference - (generalPercent / 100) * circumference"
        />
      </svg>
      <div class="circle-content">
        <div class="circle-label">Level</div>
        <div class="circle-value">{{ generalLevel }}</div>
        <button class="plus-btn" @click="showTopics = !showTopics">+</button>
      </div>
    </div>
    <transition name="fade">
      <div v-if="showTopics" class="mini-topic-progress">
        <div class="mini-topic-row" v-for="(level, topic) in topicLevels" :key="topic">
          <span class="mini-topic-name">{{ topicLabel(topic) }}</span>
          <div class="mini-topic-bar">
            <div class="mini-topic-bar-fill" :style="{ width: Math.min(100, level * 20) + '%' }"></div>
          </div>
          <span class="mini-topic-level">Lv {{ level }}</span>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
const props = defineProps({
  generalLevel: Number,
  topicLevels: Object
})
const generalPercent = computed(() => Math.min(100, (props.generalLevel || 0)))
const circumference = 2 * Math.PI * 44
const showTopics = ref(false)
const circleBg = 'linear-gradient(135deg, #232836 70%, #10131a 100%)'
function topicLabel(topic) {
  const map = {
    variables: 'Variablen',
    operators: 'Operatoren',
    if_else: 'If/Else',
    loops: 'Schleifen',
    lists: 'Listen',
    functions: 'Funktionen',
    strings: 'Strings',
    dictionaries: 'Dicts',
    classes: 'Klassen',
  }
  return map[topic] || topic
}
</script>

<style scoped>
.progress-circle-container {
  position: fixed;
  top: 2.5em;
  right: 2.5em;
  z-index: 100;
}
.progress-circle {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #232836 70%, #10131a 100%);
  box-shadow: 0 2px 10px rgba(44,114,252,0.07);
  display: flex;
  align-items: center;
  justify-content: center;
}
.circle-svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}
.circle-bg {
  fill: none;
  stroke: #181c24;
  stroke-width: 10;
}
.circle-bar {
  fill: none;
  stroke: url(#gradient);
  stroke: #7cc4fa;
  stroke-width: 10;
  stroke-linecap: round;
  transition: stroke-dashoffset 0.7s cubic-bezier(0.4,0,0.2,1);
}
.circle-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 2;
}
.circle-label {
  color: #facc15;
  font-size: 1em;
  font-weight: 700;
  margin-bottom: 0.2em;
}
.circle-value {
  color: #7cc4fa;
  font-size: 1.3em;
  font-weight: 900;
  margin-bottom: 0.1em;
}
.plus-btn {
  margin-top: 0.2em;
  background: #232836;
  color: #7cc4fa;
  border: 2px solid #7cc4fa;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  font-size: 1.4em;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(37,99,235,0.10);
  transition: background 0.2s, border-color 0.2s, color 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  outline: none;
}
.plus-btn:hover, .plus-btn:focus {
  background: #1d4ed8;
  color: #fff;
  border-color: #facc15;
  box-shadow: 0 0 0 3px rgba(250,204,21,0.4);
}
.plus-btn:active {
  background: #2563eb;
  color: #fff;
  border-color: #facc15;
}
.mini-topic-progress {
  position: absolute;
  top: 130px;
  right: 0;
  background: #232836;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(44,114,252,0.11);
  padding: 1em 1.5em;
  min-width: 220px;
  z-index: 30;
}
.mini-topic-row {
  display: flex;
  align-items: center;
  margin-bottom: 0.4em;
}
.mini-topic-name {
  flex: 0 0 80px;
  font-size: 1em;
  color: #7cc4fa;
  font-weight: 600;
}
.mini-topic-bar {
  flex: 1 1 auto;
  margin: 0 0.5em;
  background: #181c24;
  border-radius: 6px;
  height: 10px;
  overflow: hidden;
}
.mini-topic-bar-fill {
  background: linear-gradient(90deg, #059669 0%, #7cc4fa 100%);
  height: 100%;
  transition: width 0.4s;
}
.mini-topic-level {
  font-size: 1em;
  color: #facc15;
  font-weight: 700;
  min-width: 32px;
  text-align: right;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
@media (max-width: 600px) {
  .progress-circle-container {
    top: 1em;
    right: 1em;
    width: 90px;
    height: 90px;
  }
  .progress-circle {
    width: 90px;
    height: 90px;
  }
}
</style>
