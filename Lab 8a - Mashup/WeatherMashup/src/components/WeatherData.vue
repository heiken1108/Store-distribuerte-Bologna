<template>
  <div class="weather-component">
    <input
      v-model.lazy="location"
      type="text"
      placeholder="Enter location"
      class="location-input"
      @keyup.enter="setLocation"
    />
    <button class="fetch-button" @click="setLocation">Get Weather</button>

    <TabSystem />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TabSystem from './TabSystem.vue'
import { useLocationStore } from '../stores/locationStore'

const location = ref('')

const locationStore = useLocationStore()

const setLocation = async () => {
  if (!location.value.trim()) return

  locationStore.setLocation(location.value)
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
</style>
