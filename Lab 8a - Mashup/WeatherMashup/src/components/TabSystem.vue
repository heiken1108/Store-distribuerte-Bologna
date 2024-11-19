<script setup lang="ts">
import { ref } from 'vue'
import HourlyForecast from './HourlyForecast.vue'
import { useLocationStore } from '../stores/locationStore'
import CurrentConditions from './CurrentConditions.vue'
import DayOutlook from './DayOutlook.vue'

const locationStore = useLocationStore()
const emit = defineEmits<{
  (e: 'tabChanged', index: number): void
}>()

const activeTab = ref(0)

const tabs = [
  { title: 'Current Condition' },
  { title: 'Hourly Forecast' },
  { title: 'Day Outlook' },
]

const setActiveTab = (index: number) => {
  activeTab.value = index
  emit('tabChanged', index)
}
</script>

<template>
  <div class="tabs-container">
    <!-- Tab Navigation -->
    <div class="tab-nav">
      <button
        v-for="(tab, index) in tabs"
        :key="index"
        class="tab-button"
        :class="{ active: activeTab === index }"
        @click="setActiveTab(index)"
      >
        {{ tab.title }}
      </button>
    </div>

    <!-- Tab Content using named slots -->
    <div class="tab-content">
      <CurrentConditions
        v-if="activeTab === 0"
        :location="locationStore.location"
      />
      <HourlyForecast
        v-if="activeTab === 1"
        :location="locationStore.location"
      />
      <DayOutlook v-if="activeTab === 2" :location="locationStore.location" />
    </div>
  </div>
</template>

<style scoped>
.tabs-container {
  margin: 20px;
  font-family: Arial, sans-serif;
}

.tab-nav {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.tab-button {
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  margin-right: 5px;
  border-radius: 4px 4px 0 0;
  transition: all 0.3s ease;
}

.tab-button:hover {
  background-color: #f5f5f5;
}

.tab-button.active {
  border: 1px solid #ddd;
  border-bottom: none;
  margin-bottom: -1px;
  background-color: white;
}

.tab-content {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 0 4px 4px 4px;
}

.tab-panel {
  min-height: 200px;
}
</style>
