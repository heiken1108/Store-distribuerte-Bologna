<template>
  <div>
    <h2>{{ 'Hourly forecast for ' + location }}</h2>
    <div v-if="hourlyForecast" class="forecast-container">
      <div
        v-for="(day, name, idx) in hourlyForecast"
        :key="idx"
        class="day-container"
      >
        <span class="date-string">{{
          new Date(name).toLocaleDateString('en-gb', {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
          })
        }}</span>
        <div class="column-description">
          <span class="relative">Hour</span>
          <span class="relative">Weather</span>
          <span class="relative">Temperature</span>
          <span class="relative">Precipitation</span>
          <span class="relative">Wind (gust)</span>
        </div>
        <div v-for="hour in day" class="hour-container">
          <div class="weather-info-container">
            <span>
              {{
                new Date(hour.time).getHours().toString().padStart(2, '0')
              }}</span
            >
            <img
              :src="hour.condition.icon"
              class="weather-icon"
              :alt="hour.condition.text"
            />
            <span :class="hour.temp_c < 0 ? 'cold' : 'hot'">{{
              ` ${hour.temp_c.toFixed(1)}${'\u{00B0}'}`
            }}</span>
            <span class="cold"> {{ hour.precip_mm.toFixed(1) + 'mm' }}</span>
            <span>
              {{
                `${(hour.wind_kph / 3.6).toFixed(0)} (${(hour.gust_kph / 3.6).toFixed(0)})`
              }}
            </span>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading hourly forecast...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getHourlyForecast } from '../services/weatherService'
import { onMounted, Ref, ref, watch } from 'vue'
import { DateHours } from '../types'

const hourlyForecast = ref<DateHours | null>(null)

const props = defineProps<{
  location: Ref<string>
}>()

onMounted(async () => {
  await updateForecast()
})

watch(props.location, async () => await updateForecast())

const updateForecast = async () =>
  (hourlyForecast.value = await getHourlyForecast(
    props.location.value,
    Date.now()
  ))
</script>
<style lang="css" scoped>
.column-description {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-inline: 0.625rem;
  width: 100%;
}

.day-container {
  display: flex;
  flex-direction: column;
  position: relative;
  align-items: start;
}

.date-string {
  margin-inline: 0.625rem;
  font-weight: bold;
}

.forcast-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hour-container {
  position: relative;
  display: flex;
  flex-direction: column;
  margin-inline: 0.625rem;
  height: 3rem;
  width: 100%;
}

.weather-icon {
  height: 100%;
  margin-inline: 0.625rem;
  overflow: hidden;
}

.weather-info-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  height: inherit;
}

.cold {
  color: #1767d0;
}

.hot {
  color: #b6251a;
}

.relative {
  position: relative;
}
</style>
