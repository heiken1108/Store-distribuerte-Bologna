<template>
  <div class="weather-component">
    <input
      v-model="location"
      placeholder="Enter location"
      type="text"
      class="location-input"
      @keyup.enter="fetchWeather"
    />
    <button class="fetch-button" @click="fetchWeather">Get Weather</button>

    <div v-if="weatherData" class="weather-data">
      <h2>Weather for {{ location }}</h2>

      <CurrentConditions :weather-data="weatherData" />
    </div>

    <div v-else-if="loading" class="loading">Loading...</div>
    <div v-else class="error">No data available. Try another location.</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { getWeatherData, CombinedWeatherData } from '../services/weatherService'
import CurrentConditions from './CurrentConditions.vue'

const location = ref('') // User input
const weatherData = ref<CombinedWeatherData | null>(null) // Weather data
const loading = ref(false) // Loading state

const fetchWeather = async () => {
  if (!location.value.trim()) return

  loading.value = true
  weatherData.value = null

  try {
    const data = await getWeatherData(location.value.trim())
    weatherData.value = data
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
