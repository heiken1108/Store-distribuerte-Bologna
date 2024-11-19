import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLocationStore = defineStore('location', () => {
    const location = ref<string>('')

    function setLocation(newLocation: string) {
        location.value = newLocation
    }

    return {
        location,
        setLocation,
    }
})
