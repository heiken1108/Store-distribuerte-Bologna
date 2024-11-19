<template>
  <div class="weather-component">
    <input
      v-model.lazy="location"
      type="text"
      placeholder="Enter location"
      class="location-input"
      @keyup.enter="fetchWeather"
    />
    <button class="fetch-button" @click="fetchWeather">Get Weather</button>

    <TabSystem />
  </div>
</template>

<script setup lang="ts">
import { computed, provide, ref } from 'vue'
import { getWeatherData, CombinedWeatherData } from '../services/weatherService'
import TabSystem from './TabSystem.vue'

const location = ref('') // User input
const weatherData = ref<CombinedWeatherData | null>(null) // Weather data
const loading = ref(false) // Loading state

provide(
  'location',
  computed(() => location)
)

const fetchWeather = async () => {
  if (!location.value.trim()) return

  loading.value = true
  weatherData.value = null

  try {
    const data = await getWeatherData(location.value.trim())
    weatherData.value = data
    console.log(data)
  } catch (error) {
    console.error('Error fetching weather:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.weather-component {
  font-family: Arial, sans-serif;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.location-input {
  padding: 8px;
  font-size: 16px;
  width: 80%;
  margin-bottom: 10px;
}

.fetch-button {
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
}

.weather-data {
  margin-top: 20px;
  text-align: left;
}

.weather-section {
  margin-bottom: 20px;
}

.loading {
  color: blue;
}

.error {
  color: red;
}
</style>
