import axios from 'axios'

const API_KEYS = {
    openWeatherMap: import.meta.env.VITE_OPENWEATHERMAP_KEY,
    weatherAPI: import.meta.env.VITE_WEATHERAPI_KEY,
}

interface OpenWeatherData {
    weather: {
        description: string
        icon: string
    }[]
    main: {
        temp: number
        feels_like: number
        humidity: number
    }
    wind: {
        speed: number
    }
}

interface WeatherAPIData {
    current: {
        condition: {
            text: string
            icon: string
            temp_c: string
            last_updated: string
            wind_kph: string
            wind_dir: string
            humidity: string
            feelslike_c: string
            uv: string
        }
    }
    forecast: {
        forecastday: {
            date: string
            day: {
                maxtemp_c: number
                mintemp_c: number
                condition: {
                    text: string
                }
            }
        }[]
    }
}

export interface CombinedWeatherData {
    openWeather: OpenWeatherData
    weatherAPI: WeatherAPIData
}

export const getWeatherData = async (
    location: string
): Promise<CombinedWeatherData | null> => {
    try {
        const [openWeatherResponse, weatherAPIResponse] = await Promise.all([
            axios.get<OpenWeatherData>(
                `https://api.openweathermap.org/data/2.5/forecast?q=${location}&appid=${API_KEYS.openWeatherMap}&units=metric`
            ),
            axios.get<WeatherAPIData>(
                `https://api.weatherapi.com/v1/forecast.json?key=${API_KEYS.weatherAPI}&q=${location}&days=5`
            ),
        ])

        console.log(openWeatherResponse.data, weatherAPIResponse.data)
        return {
            openWeather: openWeatherResponse.data,
            weatherAPI: weatherAPIResponse.data,
        }
    } catch (error) {
        console.error('Error fetching weather data:', error)
        return null
    }
}
