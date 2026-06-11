import pandas as pd
import json
import os
import glob

def transform_latest_data():
    
    list_of_files = glob.glob('data/raw/*.json')
    if not list_of_files:
        print("No raw data found to tranform")
        return
    
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Transforming: {latest_file}")
    
    with open(latest_file, 'r') as f:
        raw_data = json.load(f)

    current_weather = raw_data['current']
    
    current_weather['latitude'] = raw_data['latitude']
    current_weather['longitude'] = raw_data['longitude']
 
    
    df = pd.DataFrame([current_weather])
    
    df = df.rename(columns={
        'temperature_2m' : 'temp_celsius',
        'wind_speed_10m' : 'wind_kmh',
        'time': 'observation_time'
    })
    
    output_file = "data/cleaned/weather_processed.csv"
    
    if not os.path.isfile(output_file):
        df.to_csv(output_file, index=False)
    else:
        df.to_csv(output_file, mode = 'a', index=False, header= False)
        
    print(f"Transformation complete! Data append to {output_file}")
    
if __name__ == "__main__":
    transform_latest_data()
