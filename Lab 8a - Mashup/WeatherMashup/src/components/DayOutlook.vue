<template>
  <div>
    <h2>
      {{
        '5 day outlook for ' +
        (location.length > 1
          ? location.charAt(0).toUpperCase() + location.slice(1)
          : '...')
      }}
    </h2>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { getWeatherData } from '../services/weatherService'
import { CombinedWeatherData } from '../types'
import { useLocationStore } from '../stores/locationStore'

const locationStore = useLocationStore()

const props = defineProps<{
  location: string
}>()

const weather = ref<CombinedWeatherData | null>(
  props.location.length > 0
    ? localStorage.getItem('weatherData')
      ? JSON.parse(localStorage.getItem('weatherData')!)
      : null
    : null
)
const loading = ref(false)

onMounted(() => {
  if (
    props.location.length > 0 &&
    locationStore.outlookLocation !== props.location
  ) {
    updateForecast()
  }
})

watch(props, async () => await updateForecast())

const updateForecast = async () => {
  console.log('Fetching weather data')
  loading.value = true
  try {
    weather.value = await getWeatherData(props.location)
    localStorage.setItem('weatherData', JSON.stringify(weather.value))
    locationStore.setOutlookLocation()
    console.log(weather.value)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped></style>
