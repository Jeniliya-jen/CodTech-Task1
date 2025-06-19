# Import necessary libraries
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (for securely storing API key)
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Ask user to input the city for which weather data is needed
city = input("Enter a city name: ")

# Build the API request URL with the given city and API key
url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
response = requests.get(url)

# Check if the API request was successful
if response.status_code != 200:
    print("Failed to fetch data. Check your API key or city name.")
    exit()

data = response.json()
weather_list = data['list']

# Extract relevant data: datetime, temperature, and humidity for each forecast entry
weather_data = []
for entry in weather_list:
    dt = datetime.fromtimestamp(entry['dt'])
    temp = entry['main']['temp']
    humidity = entry['main']['humidity']
    weather_data.append({'datetime': dt, 'temp': temp, 'humidity': humidity})

# Create a DataFrame from the extracted data for easy analysis and visualization
df = pd.DataFrame(weather_data)

# Set the plot size
plt.figure(figsize=(12, 6))

# Plot temperature as a line graph
sns.lineplot(data=df, x='datetime', y='temp', label='Temperature (°C)', marker='o')

# Plot humidity as a line graph
sns.lineplot(data=df, x='datetime', y='humidity', label='Humidity (%)', marker='o')

# Set the chart title and axis labels
plt.title(f'5-Day Weather Forecast for {city}')
plt.xlabel('Date & Time')
plt.ylabel('Value')
plt.xticks(rotation=45)

# Add legend and grid for clarity
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()
