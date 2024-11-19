<template>
  <div class="weather-component">
    <h1>Current Conditions</h1>
    <div class="weather-data">
      <div class="weather-section">
        <p>{{ weatherData?.openWeather.weather[0].description }}</p>
        <img
          :src="weatherData?.openWeather.weather[0].icon"
          alt="Weather icon"
        />
        <p>Temperature: {{ weatherData?.openWeather.main.temp }}°C</p>
        <p>
          Feels like:
          {{ weatherData?.openWeather.main.feels_like }}°C
        </p>
        <p>Humidity: {{ weatherData?.openWeather.main.humidity }}</p>
        <p>Wind Speed: {{ weatherData?.openWeather.wind.speed }} km/h</p>
      </div>
    </div>
    <button
      class="fetch-button"
      @click="console.log(weatherData?.openWeather.weather[0].description)"
    >
      Fetch Weather
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { CombinedWeatherData } from '../services/weatherService'

const props = defineProps<{
  weatherData: CombinedWeatherData
}>()

const weatherData = ref<CombinedWeatherData | null>(props.weatherData)
</script>

<style scoped></style>
