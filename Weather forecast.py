import requests
import csv

# API key from Open Weather Map
api_key = '48b1928ffc21d8d575b753aec345d33f'

# List of 5 different cities with their country codes
cities = [
    {'name': 'Las Vegas', 'country_code': 'US'},
    {'name': 'Boulder', 'country_code': 'US'},
    {'name': 'Denver', 'country_code': 'US'},
    {'name': 'Boise', 'country_code': 'US'},
    {'name': 'San Diego', 'country_code': 'US'}
]

def get_weather_info(city):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city["name"]},{city["country_code"]}&appid={api_key}'
    
    # Sends a GET request to Open Weather Map API
    response = requests.get(url)
    
    # Checks if a request is successful or not
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get weather information for {city['name']}")
        return None

# Function to parse weather forecast data and extract required information
def weather_data(data, city):
    # Checking if the data is available or not
    if data is None: 
        return None
        
    # Get the list of forecasts from the data    
    forecasts = data.get('list', [])
    
    # Initializing an empty list to store the information
    data_info = []
    for forecast in forecasts:
        date_time = forecast.get('dt_txt', '').split(' ')  # Split the date and time
        if len(date_time) != 2:  # Check if date and time are in the expected format
            continue
        date, time = date_time
        
        # Extracting weather information
        weather_id = forecast['weather'][0].get('id', '')
        weather = forecast['weather'][0].get('description', '')
        
        # Extracting temperature information
        temp_min = '{:.2f}'.format(forecast['main'].get('temp_min', 0))
        temp_max = '{:.2f}'.format(forecast['main'].get('temp_max', 0))
        feels_like = '{:.2f}'.format(forecast['main'].get('feels_like', 0))
        temperature = '{:.2f}'.format(forecast['main'].get('temp', 0))
        temp_kf = '{:.2f}'.format(forecast['main'].get('temp_kf', 0))
        
        # Extracting humidity information
        humidity = '{:.2f}'.format(forecast['main'].get('humidity', 0))
        
        # Extracting wind speed information
        wind_speed = '{:.2f}'.format(forecast['wind'].get('speed', 0))
        wind_deg = forecast['wind'].get('deg', 0)
        wind_gust = forecast['wind'].get('gust', 0)
        
        # Extracting pressure information
        pressure = forecast['main'].get('pressure', 0)
        
        # Extracting sea level pressure
        sea_level = forecast['main'].get('sea_level', 0)
        
        # Extracting ground level pressure
        grnd_level = forecast['main'].get('grnd_level', 0)
        
        # Extracting cloudiness percentage
        cloudiness = forecast['clouds'].get('all', 0)
        
        # Extracting visibility information
        visibility = forecast.get('visibility', 0) 
        
        # Extracting probability of precipitation information
        pop = forecast.get('pop', 0) 
        
        # Storing all the information in a dictionary
        data_info.append({'City': city['name'], 'Country Code': city['country_code'], 'Date': date, 'Time': time, 
                          'Weather_Id': weather_id, 'Weather': weather,
                          'Temp Min (F)': temp_min, 'Temp Max (F)': temp_max, 'Feels Like (F)': feels_like, 'Temperature (F)': temperature, 'Temp KF': temp_kf,
                          'Humidity (%)': humidity, 
                          'Wind Speed (mph)': wind_speed, 'Wind Degree': wind_deg, 'Wind Gust': wind_gust, 'Pressure': pressure,
                          'Sea Level': sea_level, 'Ground Level': grnd_level, 
                          'Cloudiness': cloudiness,  'Visibility': visibility, 'Probability of percipitation ': pop})
    return data_info

# Function to export data to CSV file
def export_to_csv(data, filename):
    if not data:
        print("No weather data to export.")
        return
    header = list(data[0].keys())
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data exported to {filename}")

# Main function
def main():
    full_data = []
    for city in cities:
        weather = get_weather_info(city)
        if weather:
            data = weather_data(weather, city)
            if data:
                full_data += data
    if full_data:
        export_to_csv(full_data, 'weather_forecast.csv')
    else:
        print("No weather data to export.")

if __name__ == "__main__":
    main()