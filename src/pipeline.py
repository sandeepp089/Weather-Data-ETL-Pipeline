from extract import extract_weather_data
from transform import transform_latest_data
from load import load_data_to_sql
import logging

logging.basicConfig(level= logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    logging.info("--- STARTING WEATHER ETL PIPELINE ---")

    raw_file = extract_weather_data()
    if not raw_file:
        logging.error("Pipeline failed at Extract stage.")
        return
    
    transform_latest_data()

    load_data_to_sql()

    logging.info("--- PIPELINE COMPLETED SUCCESSFULLY ---")

if __name__ == "__main__":
    run_pipeline()
