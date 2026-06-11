# import pandas as pd
# import os
# import shutil
# from datetime import datetime

# def load_data_to_production():
#     source_path = "data/cleaned/weather_processed.csv"

#     target_path = "data/weather_database_simulation.csv"

#     print("Starting the load process")

#     try:
#         if os.path.exists(source_path):
            
#             df = pd.read_csv(source_path)

#             shutil.copyfile(source_path, target_path)

#             print(f"Load Successful! Data is now in 'Production': {target_path}")
#             print(f"Total records loaded: {len(df)}")

#         else:
#             print(f"Source file not found, Did you run transform.py?")

#     except Exception as e:
#         print(f"Error during Load: {e}")

# if __name__ == "__main__":
#     load_data_to_production()


import pypyodbc as odbc #pip install pypyodbc
import pandas as pd
import os
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = r'sandeep\SQLEXPRESS'
DATABASE_NAME = 'Weather_forcast'

#  uid=<username>;
#     pwd=<password>;
connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={{{SERVER_NAME}}};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""
def load_data_to_sql():
    source_path = "data/cleaned/weather_processed.csv"
    
    if not os.path.exists(source_path):
        print("Source file not found. Run transform first!")
        return

    try:
        # 1. Connect to SQL Server
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()
        print("Connected to SQL Server successfully.")

        # 2. Create Table if it doesn't exist (Automated Setup)
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Weather_Fact')
            BEGIN
                CREATE TABLE Weather_Fact (
                    observation_time DATETIME2,
                    temp_celsius FLOAT,
                    wind_kmh FLOAT,
                    latitude FLOAT,
                    longitude FLOAT,
                    ingested_at DATETIME DEFAULT GETDATE()
                )
            END
        """)
        conn.commit()

        # 3. Read the cleaned CSV
        df = pd.read_csv(source_path)

        # FIX: Convert the string column to actual Python Datetime objects
        # This removes the "Conversion failed" error because Python sends 
        # the data in a format SQL Server understands perfectly.
        df['observation_time'] = pd.to_datetime(df['observation_time'])
        
        # 4. Insert Data (Iterating through the DataFrame)
        # Note: In production, we use 'executemany' for speed
        insert_query = """
            INSERT INTO Weather_Fact (observation_time, temp_celsius, wind_kmh, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        """

        for index, row in df.iterrows():
            cursor.execute(insert_query, (
                row['observation_time'], 
                row['temp_celsius'], 
                row['wind_kmh'], 
                row['latitude'], 
                row['longitude']
            ))

        conn.commit()
        print(f"Success! {len(df)} records loaded into MS SQL Server.")

    except Exception as e:
        print(f"Error during Load: {e}")
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    load_data_to_sql()
