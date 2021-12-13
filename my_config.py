# the input locations to fetch
CITIES = ["HongKong", "Singapore", "Tokyo","Seoul", "London" ,"Paris", "NewYork"]
APPID = '86360c8475357ebb01df5334aa34a6ed'
# fetch data every 15 seconds, can be 5, 10, 15, 20, 30
FREQUENCY_SEC = 15
# aggregate data every minute
AGGREGATE_PERIOD_SEC = 60
# location to save file.csv which contains info of files data fetched and its ingestion time
LIST_PATH_FILES = '/home/lenovo/Desktop/mytest_demo/my_source/files_path.csv' 
# location folder to save all data fetched from api
DATA_LOG_FOLDER = '/home/lenovo/Desktop/mytest_demo/my_source/raw_data'
