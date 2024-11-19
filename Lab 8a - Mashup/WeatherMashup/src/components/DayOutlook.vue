<template>
  <div>
    <h2>
      {{ '5 day outlook for ' + (location.length > 1 ? location : '...') }}
    </h2>
    <div v-if="weather" class="forecast-container">
      <table class="table">
        <thead>
          <tr class="table-header">
            <th class="table-data">Timestamp</th>
            <th class="table-data">OpenWeatherMap</th>
            <th class="table-data">WeatherAPI</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, timestamp) in weather" :key="timestamp">
            <td class="table-data text-center">
              {{ new Date(timestamp * 1000).toLocaleString('it-it') }}
            </td>
            <td class="table-data">
              <div>Temp: {{ data.openWeather?.main.temp.toFixed(1) }}°C</div>
              <div>Humidity: {{ data.openWeather?.main.humidity }}%</div>
              <div>
                Wind:
                {{ data.openWeather?.wind.speed }} m/s
              </div>
              <div>
                Description: {{ data.openWeather?.weather[0].description }}
              </div>
            </td>
            <td class="table-data">
              <div>Temp: {{ data.weatherAPI?.temp_c.toFixed(1) }}°C</div>
              <div>Humidity: {{ data.weatherAPI?.humidity }}%</div>
              <div>
                Wind: {{ (data.weatherAPI?.wind_kph! / 3.6).toFixed(1) }} m/s
              </div>
              <div>Description: {{ data.weatherAPI?.condition.text }}</div>
            </td>
            <hr />
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="loading" class="center">
      <LoadingSymbol />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { getFiveDayForecast } from '../services/weatherService'
import { CombinedFiveDayForecast } from '../types'
import LoadingSymbol from './LoadingSymbol.vue'

const weather = ref<CombinedFiveDayForecast | null>(null)
const loading = ref(false)

const props = defineProps<{
  location: string
}>()

onMounted(() => updateForecast())

watch(props, async () => await updateForecast())

const updateForecast = async () => {
  console.log('Fetching weather data')
  loading.value = true
  try {
    weather.value = await getFiveDayForecast(props.location)
    console.log(weather.value)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.table-data {
  padding: 0.5rem;
}

.table-header {
  background-color: #f3f4f6;
}

.table {
  border-collapse: collapse;
  width: 100%;
}
</style>
