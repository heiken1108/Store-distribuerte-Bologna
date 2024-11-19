<template>
  <div>
    <h2>
      {{ '5 day outlook for ' + (location.length > 1 ? location : '...') }}
    </h2>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { getWeatherData } from '../services/weatherService'
import { CombinedWeatherData } from '../types'

const weather = ref<CombinedWeatherData | null>(null)
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
    weather.value = await getWeatherData(props.location)
    console.log(weather.value)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped></style>
