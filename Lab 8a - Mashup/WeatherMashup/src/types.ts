interface WeatherLocation {
    name: string
    region: string
    country: string
    lat: number
    lon: number
    tz_id: string
    localtime_epoch: number
    localtime: string
}

interface WeatherCondition {
    text: string
    icon: string
    code: number
}

interface CurrentWeather {
    last_updated_epoch: number
    last_updated: string
    temp_c: number
    temp_f: number
    is_day: number
    condition: WeatherCondition
    wind_mph: number
    wind_kph: number
    wind_degree: number
    wind_dir: string
    pressure_mb: number
    pressure_in: number
    precip_mm: number
    precip_in: number
    humidity: number
    cloud: number
    feelslike_c: number
    feelslike_f: number
    windchill_c: number
    windchill_f: number
    heatindex_c: number
    heatindex_f: number
    dewpoint_c: number
    dewpoint_f: number
    vis_km: number
    vis_miles: number
    uv: number
    gust_mph: number
    gust_kph: number
}

interface HourlyWeather {
    time_epoch: number
    time: string
    temp_c: number
    temp_f: number
    is_day: number
    condition: WeatherCondition
    wind_mph: number
    wind_kph: number
    wind_degree: number
    wind_dir: string
    pressure_mb: number
    pressure_in: number
    precip_mm: number
    precip_in: number
    snow_cm: number
    humidity: number
    cloud: number
    feelslike_c: number
    feelslike_f: number
    windchill_c: number
    windchill_f: number
    heatindex_c: number
    heatindex_f: number
    dewpoint_c: number
    dewpoint_f: number
    will_it_rain: number
    chance_of_rain: number
    will_it_snow: number
    chance_of_snow: number
    vis_km: number
    vis_miles: number
    gust_mph: number
    gust_kph: number
    uv: number
}

interface AstronomicalData {
    sunrise: string
    sunset: string
    moonrise: string
    moonset: string
    moon_phase: string
    moon_illumination: number
    is_moon_up: number
    is_sun_up: number
}

interface DailyForecast {
    date: string
    date_epoch: number
    day: {
        maxtemp_c: number
        maxtemp_f: number
        mintemp_c: number
        mintemp_f: number
        avgtemp_c: number
        avgtemp_f: number
        maxwind_mph: number
        maxwind_kph: number
        totalprecip_mm: number
        totalprecip_in: number
        totalsnow_cm: number
        avgvis_km: number
        avgvis_miles: number
        avghumidity: number
        daily_will_it_rain: number
        daily_chance_of_rain: number
        daily_will_it_snow: number
        daily_chance_of_snow: number
        condition: WeatherCondition
        uv: number
    }
    astro: AstronomicalData
    hour: HourlyWeather[]
}

interface WeatherAPIData {
    location: WeatherLocation
    current: CurrentWeather
    forecast: {
        forecastday: DailyForecast[]
    }
}

interface OpenWeatherApiResponse {
    cod: string
    message: number
    cnt: number
    list: OpenWeatherData[]
}

interface OpenWeatherData {
    dt: number // Unix timestamp
    main: OpenMainWeatherData
    weather: OpenWeatherCondition[]
    clouds: OpenClouds
    wind: OpenWind
    visibility: number // in meters
    pop: number // Probability of precipitation
    rain?: OpenRainData // Optional because not always present
    sys: OpenSys
    dt_txt: string // Forecast time in ISO format
}

interface OpenMainWeatherData {
    temp: number // Current temperature
    feels_like: number // Feels-like temperature
    temp_min: number // Minimum temperature
    temp_max: number // Maximum temperature
    pressure: number // Atmospheric pressure at sea level
    sea_level?: number // Optional sea-level atmospheric pressure
    grnd_level?: number // Optional ground-level atmospheric pressure
    humidity: number // Humidity percentage
    temp_kf?: number // Internal parameter, temp adjustment
}

interface OpenWeatherCondition {
    id: number // Weather condition ID
    main: string // Group of weather parameters (e.g., Rain, Snow, Clouds)
    description: string // Description of the weather
    icon: string // Weather icon ID
}

interface OpenClouds {
    all: number // Cloudiness percentage
}

interface OpenWind {
    speed: number // Wind speed in m/s
    deg: number // Wind direction in degrees
    gust?: number // Optional gust speed in m/s
}

interface OpenRainData {
    '1h'?: number
    '3h'?: number
}

interface OpenSys {
    pod: string // Part of the day (n = night, d = day)
}

interface OpenWeatherCurrentResponse {
    coord: {
        lon: number
        lat: number
    }
    weather: {
        id: number
        main: string
        description: string
        icon: string
    }[]
    base: string
    main: {
        temp: number
        feels_like: number
        temp_min: number
        temp_max: number
        pressure: number
        humidity: number
        sea_level?: number
        grnd_level?: number
    }
    visibility: number
    wind: {
        speed: number
        deg: number
        gust?: number
    }
    rain?: {
        '1h': number
    }
    clouds: {
        all: number
    }
    dt: number
    sys: {
        type?: number
        id?: number
        country: string
        sunrise: number
        sunset: number
    }
    timezone: number
    id: number
    name: string
    cod: number
}
interface CombinedWeatherData {
    openWeather: OpenWeatherApiResponse
    weatherAPI: WeatherAPIData
}

interface CombinedWeatherDataCurrent {
    openWeather: OpenWeatherCurrentResponse
    weatherAPI: WeatherAPIData
}

interface DateHours {
    [date: string]: HourlyWeather[]
}

interface CombinedFiveDayForecast {
    [unix_timestamp: number]: {
        openWeather: OpenWeatherData | null
        weatherAPI: HourlyWeather | null
    }
}

export type {
    WeatherLocation,
    WeatherCondition,
    CurrentWeather,
    HourlyWeather,
    AstronomicalData,
    DailyForecast,
    WeatherAPIData,
    DateHours,
    OpenWeatherData,
    CombinedWeatherData,
    OpenWeatherApiResponse,
    OpenWeatherCurrentResponse,
    CombinedWeatherDataCurrent,
    CombinedFiveDayForecast,
}
