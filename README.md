# Weather Cities
This is my source to fetch data and process data with simple python code. 

### 2 steps to fetch and process data:

- Fetch data from api: fetch data of all city CITIES with every FREQUENCY_SEC seconds and save it into a folder LIST_PATH_FILES variable in my_config.py

- Process data: after fetching data to a local folder, take them to process every AGGREGATE_PERIOD_SEC seconds and show them into console

### Requirement: before running application, please install:

- python: sudo apt-get install python3.8

- pandas: python3 -m pip install pandas

### Before running application, edit variables in my_config.py:

 location to save file.csv which contains info of files data fetched and its ingestion time

- LIST_PATH_FILES = '/home/lenovo/Desktop/mytest_demo/my_source/files_path.csv' 

location folder to save all data fetched from api

- DATA_LOG_FOLDER = '/home/lenovo/Desktop/mytest_demo/my_source/raw_data'

### To run application, run parallel 2 files below:

- Run fetch data: python3 fetch_data.py

- To process data: python3 process_data.py 
