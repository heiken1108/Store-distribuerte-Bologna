<template>
  <div>
    <h2>
      {{
        'Current conditions for ' +
        (location.length > 1
          ? location.charAt(0).toUpperCase() + location.slice(1)
          : '...')
      }}
    </h2>
    <div v-if="weather" class="wrapper">
      <div
        v-for="source in weatherSources"
        :key="source.name"
        class="container"
      >
        <h3>{{ source.name }}</h3>
        <div class="icon-wrapper">
          <img
            :src="source.icon"
            class="weather-icon"
            :alt="source.description"
          />
        </div>
        <h4 class="temp">{{ source.temp.toFixed(1) }}°C</h4>
        <h5>Feels like {{ source.feelsLike.toFixed(1) }}°C</h5>
        <h4 class="rain">{{ source.rain }}mm rain last hour</h4>
        <h4 class="wind">Wind: {{ source.wind }}m/s</h4>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { getCurrentConditions } from '../services/weatherService'
import { CombinedWeatherDataCurrent } from '../types'

const props = defineProps<{
  location: string
}>()

const weather = ref<CombinedWeatherDataCurrent | null>(
  props.location.length > 0
    ? localStorage.getItem('currentConditions')
      ? JSON.parse(localStorage.getItem('currentConditions')!)
      : null
    : null
)
const loading = ref(false)

onMounted(() => {
  if (
    props.location.length > 0 &&
    weather.value?.openWeather.name !==
      props.location.charAt(0).toUpperCase() + props.location.slice(1)
  ) {
    updateForecast()
  }
})

watch(props, async () => await updateForecast())

const updateForecast = async () => {
  console.log('Fetching current conditions')
  loading.value = true
  try {
    weather.value = await getCurrentConditions(props.location)
    localStorage.setItem('currentConditions', JSON.stringify(weather.value))
    console.log(weather.value)
  } finally {
    loading.value = false
  }
}

const weatherSources = computed(() => {
  if (!weather.value) return []
  return [
    {
      name: 'OpenWeatherMap',
      icon: `https://openweathermap.org/img/wn/${weather.value.openWeather.weather[0].icon}@2x.png`,
      description: weather.value.openWeather.weather[0].description,
      temp: weather.value.openWeather.main.temp,
      feelsLike: weather.value.openWeather.main.feels_like,
      rain: weather.value.openWeather.rain?.['1h'] ?? 0,
      wind: weather.value.openWeather.wind.speed.toFixed(1),
    },
    {
      name: 'WeatherAPI',
      icon: weather.value.weatherAPI.current.condition.icon,
      description: weather.value.weatherAPI.current.condition.text,
      temp: weather.value.weatherAPI.current.temp_c,
      feelsLike: weather.value.weatherAPI.current.feelslike_c,
      rain: weather.value.weatherAPI.current.precip_mm,
      wind: (weather.value.weatherAPI.current.wind_kph / 3.6).toFixed(1),
    },
  ]
})
</script>

<style scoped>
.wrapper {
  display: flex;
  justify-content: space-around;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: -1rem;
}

.icon-wrapper {
  width: 100px;
  height: 100px;
}

.temp {
  color: red;
}

.rain {
  color: blue;
}
</style>
