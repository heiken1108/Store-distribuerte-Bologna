import axios from 'axios'
import {
    WeatherAPIData,
    CombinedWeatherData,
    DateHours,
    OpenWeatherApiResponse,
    OpenWeatherCurrentResponse,
    CombinedWeatherDataCurrent,
    CombinedFiveDayForecast,
    WeatherApiCurrentResponse,
} from '../types'

const API_KEYS = {
    openWeatherMap: import.meta.env.VITE_OPENWEATHERMAP_KEY,
    weatherAPI: import.meta.env.VITE_WEATHERAPI_KEY,
}

export const getWeatherData = async (
    location: string
): Promise<CombinedWeatherData | null> => {
    try {
        const [openWeatherResponse, weatherAPIResponse] = await Promise.all([
            axios.get<OpenWeatherApiResponse>(
                `https://api.openweathermap.org/data/2.5/forecast?q=${location}&appid=${API_KEYS.openWeatherMap}&units=metric`
            ),
            axios.get<WeatherAPIData>(
                `https://api.weatherapi.com/v1/forecast.json?key=${API_KEYS.weatherAPI}&q=${location}&days=5&unixdt=${Date.now()}`
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

export const getCurrentConditions = async (
    location: string
): Promise<CombinedWeatherDataCurrent | null> => {
    try {
        const [openWeatherResponse, weatherAPIResponse] = await Promise.all([
            axios.get<OpenWeatherCurrentResponse>(
                `https://api.openweathermap.org/data/2.5/weather?q=${location}&appid=${API_KEYS.openWeatherMap}&units=metric`
            ),
            axios.get<WeatherApiCurrentResponse>(
                `https://api.weatherapi.com/v1/current.json?key=${API_KEYS.weatherAPI}&q=${location}`
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

export const getHourlyForecast = async (
    location: string,
    unixTimestamp: number
): Promise<DateHours | null> => {
    try {
        const response = await axios.get<WeatherAPIData>(
            `https://api.weatherapi.com/v1/forecast.json?key=${API_KEYS.weatherAPI}&q=${location}&days=2&unixdt=${Date.now()}`
        )

        const dateHours: DateHours = {}

        response.data?.forecast.forecastday.forEach((day) => {
            const filteredHours = day.hour.filter(
                (hour) => hour.time_epoch > Math.floor(unixTimestamp / 1000)
            )

            if (filteredHours.length > 0) {
                dateHours[day.date] = filteredHours
            }
        })

        return dateHours
    } catch (error) {
        console.error('Error fetching hourly forecast:', error)
        return null
    }
}

export const getFiveDayForecast = async (
    location: string
): Promise<CombinedFiveDayForecast | null> => {
    try {
        const response1 = await axios.get<OpenWeatherApiResponse>(
            `https://api.openweathermap.org/data/2.5/forecast?q=${location}&appid=${API_KEYS.openWeatherMap}&units=metric`
        )
        const response2 = await axios.get<WeatherAPIData>(
            `https://api.weatherapi.com/v1/forecast.json?key=${API_KEYS.weatherAPI}&q=${location}&days=6&unixdt=${Date.now()}`
        )

        const groupedByHour: CombinedFiveDayForecast = {}

        response1.data.list.forEach((entry) => {
            groupedByHour[entry.dt] = {
                openWeather: entry,
                weatherAPI: null,
            }
        })

        response2.data.forecast.forecastday.forEach((entry) => {
            entry.hour.forEach((hour) => {
                if (hour.time_epoch.toString() in groupedByHour)
                    groupedByHour[hour.time_epoch].weatherAPI = hour
            })
        })

        return groupedByHour
    } catch (error) {
        console.error('Error fetching five day forecast:', error)
        return null
    }
}
