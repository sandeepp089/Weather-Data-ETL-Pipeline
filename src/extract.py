import requests 
import json
import os
from datetime import datetime

def extract_weather_data():
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    
    print("Checking for new data...")
    
    try:
        
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/raw/weather_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"Success! Raw data saved to: {filename}")
        return filename
    
    except Exception as e:
        print(f"Error during extraction: {e}")
        return None
    
if __name__ == "__main__":
    extract_weather_data();


