# install
# pandas

import pandas as pd
import json
from urllib.request import urlopen  
import time
from datetime import datetime
import csv
from my_config import LIST_PATH_FILES, DATA_LOG_FOLDER, CITIES, APPID, FREQUENCY_SEC


def write_files_path(file_name, now_time):
    fields = [file_name, now_time]
    with open(LIST_PATH_FILES, "a") as f:
        writer = csv.writer(f)
        writer.writerow(fields)

def fetch_data(cities):
    try:
        json_array = []
        for city in cities:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APPID}"
            try:
                dataUrl = urlopen(url)
            except:
                pass
            print(url)
            jsonData = dataUrl.read().decode('utf-8')
            json_array.append(jsonData)
        return json_array
    except ValueError:
        print("Cannot fetch cause ", ValueError)

def normalize_save_data(cities):
    try:
        while(True):
            now_time = datetime.now().strftime('%Y%m%d%H%M%S')
            file_name = f'{DATA_LOG_FOLDER}/datalog_{now_time}.csv'
            rawlist = fetch_data(cities)
            json_array = []
            for raw in rawlist:
                # print(raw)
                if(raw != None and raw!=''):
                    json_load = json.loads(raw)
                    weather = json_load['weather'][0]
                    json_load['weather'] = weather
                    json_load['ingestion_time'] = now_time
                    json_array.append(json_load)
            # data = pd.json_normalize(json_array, record_path=['weather'])
            data = pd.json_normalize(json_array)

            data.to_csv(file_name, sep='\t')
            write_files_path(f'datalog_{now_time}.csv', now_time)
            print(f'Fetch data to datalog_{now_time}.csv success')
            time.sleep(FREQUENCY_SEC)
    except ValueError:
        print('Cannot get fetch data cause ', ValueError)

if __name__ == "__main__":
    normalize_save_data(CITIES)
