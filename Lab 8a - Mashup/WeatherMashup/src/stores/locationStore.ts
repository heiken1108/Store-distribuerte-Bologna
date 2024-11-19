import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLocationStore = defineStore('location', () => {
    const location = ref<string>('')
    const hourlyLocation = ref<string>('')
    const outlookLocation = ref<string>('')

    function setLocation(newLocation: string) {
        location.value = newLocation
    }

    function setHourlyLocation() {
        hourlyLocation.value = location.value
    }

    function setOutlookLocation() {
        outlookLocation.value = location.value
    }

    return {
        location,
        hourlyLocation,
        outlookLocation,
        setLocation,
        setHourlyLocation,
        setOutlookLocation,
    }
})
