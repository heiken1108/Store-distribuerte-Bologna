<template>
  <div class="weather-component">
    <input
      v-model="location"
      @keyup.enter="fetchWeather"
      type="text"
      placeholder="Enter location"
      class="location-input"
    />
    <button @click="fetchWeather" class="fetch-button">Get Weather</button>

    <div v-if="weatherData" class="weather-data">
      <h2>Weather for {{ location }}</h2>

      <!-- OpenWeather Data -->
      <div class="weather-section">
        <h3>OpenWeatherMap 5-day Forecast</h3>
        <ul>
          <li v-for="(entry, index) in weatherData.openWeather.list" :key="index">
            <strong>{{ entry.dt_txt }}</strong
            >: {{ entry.main.temp }}°C, {{ entry.weather[0].description }}
          </li>
        </ul>
      </div>

      <!-- WeatherAPI Data -->
      <div class="weather-section">
        <h3>WeatherAPI Forecast</h3>
        <ul>
          <li v-for="(forecast, index) in weatherData.weatherAPI.forecast.forecastday" :key="index">
            <strong>{{ forecast.date }}</strong
            >: {{ forecast.day.maxtemp_c }}°C / {{ forecast.day.mintemp_c }}°C,
            {{ forecast.day.condition.text }}
          </li>
        </ul>
      </div>
    </div>

    <div v-else-if="loading" class="loading">Loading...</div>
    <div v-else class="error">No data available. Try another location.</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { getWeatherData, CombinedWeatherData } from "../services/weatherService";

const location = ref(""); // User input
const weatherData = ref<CombinedWeatherData | null>(null); // Weather data
const loading = ref(false); // Loading state

const fetchWeather = async () => {
  if (!location.value.trim()) return;

  loading.value = true;
  weatherData.value = null;

  try {
    const data = await getWeatherData(location.value.trim());
    weatherData.value = data;
  } catch (error) {
    console.error("Error fetching weather:", error);
  } finally {
    loading.value = false;
  }
};
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
