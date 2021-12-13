import pandas as pd
import time
from datetime import datetime
import os
from my_config import LIST_PATH_FILES, DATA_LOG_FOLDER, AGGREGATE_PERIOD_SEC

def check_file_existence(list_files):
    check_file_exist = []
    for file in list_files:
        if(os.path.exists(f'{DATA_LOG_FOLDER}/{file}')):
            check_file_exist.append(file)
    return check_file_exist

def get_list_files_after_period_minutes(last_time):
    try:
        df = pd.read_csv(LIST_PATH_FILES, header=None)
        df.columns = ["name", "time"]
        df2 = df.loc[df['time'] > last_time].sort_values(by=['time'], ascending=False)
        lastime_next = df2["time"].max()
        list_name = df2['name'].tolist()
        return list_name, lastime_next
    except ValueError :
        print('Cannot get list file cause ', ValueError)



def process_data(list_file):
    try:
        list_file = check_file_existence(list_file)
        if(len(list_file) > 0 ):
            df_from_each_file = (pd.read_csv(f'{DATA_LOG_FOLDER}/{f}', sep='\t') for f in list_file)
            concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
            now_time = datetime.now().strftime("%Y-%m-%dT%H:%m:%sZ")
            df = concatenated_df[["id", "name", "main.temp", "weather.main", "weather.description", "ingestion_time"]]

            # calculate mean 
            average_temp_df = df.groupby(['name'])['main.temp'].mean().to_frame().rename(columns={"main.temp": "average_temp"})

            end_time_checkpointdf = df.loc[df['ingestion_time'] == df['ingestion_time'].max()] 
            start_time_checkpointdf = df.loc[df['ingestion_time'] == df['ingestion_time'].min()]
            end_time_checkpointdf['min'] = start_time_checkpointdf['main.temp'].values
            end_time_checkpointdf['temperature_diff'] = end_time_checkpointdf['main.temp'] - end_time_checkpointdf['min']
            merge_df = pd.merge(end_time_checkpointdf, average_temp_df, on='name').drop(columns=['weather.main', 'weather.description', 'min'])

            weather_description_df = df.groupby(['name', 'weather.description'])['weather.main'].count().sort_values() \
            .groupby(level=0).tail(1).reset_index().rename(columns={"weather.description": "decription"}).drop(columns=['weather.main'])
            result = pd.merge(merge_df, weather_description_df, on='name').drop(columns=['id', 'ingestion_time', 'main.temp'])
            print("********************************************************************")
            result['datetime'] = now_time
            result = result.rename(columns={"name": "location"})
            print(str(result.T.to_dict()))
            return str(result.T.to_dict())
        else:
            print('No data')
            return
    except ValueError:
        print('Cannot handle data cause ', ValueError)
    

def handle_data():
    try:
    # should start now
        # last_time = datetime.now().strftime('%Y%m%d%H%M%S')
        last_time = 0
        while(True):
            list_file, lastime_next = get_list_files_after_period_minutes(last_time)
            process_data(list_file)
            last_time = lastime_next
            time.sleep(AGGREGATE_PERIOD_SEC)
    except ValueError:
        print('Cannot handle data cause ', ValueError)


if __name__ == "__main__":
    handle_data()
