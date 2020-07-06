import os
import json
import sys
import duckdb

def run(dbFilename):
  print("connecting to duckdb")
  conn = duckdb.connect(dbFilename)
  cursor = conn.cursor()

  print("loading movies")
  cursor.execute("DROP TABLE IF EXISTS movies");
  cursor.execute("""
        CREATE TABLE if not exists movies (
            IMDB_Rating DOUBLE,
            Production_Budget DOUBLE,
            Release_Date DOUBLE,
            Rotten_Tomatoes_Rating DOUBLE,
            Running_Time_min DOUBLE,
            US_DVD_Sales DOUBLE,
            US_Gross DOUBLE,
            Worldwide_Gross DOUBLE)
        """)
  data_file = str(os.path.join(os.path.dirname(__file__),'..','..','dataset_movies_1M_fixed.csv'))
  cursor.execute("copy movies from '"+data_file+"' header ")

  print("loading weather")
  cursor.execute("DROP TABLE IF EXISTS weather");
  cursor.execute("""
        CREATE TABLE if not exists weather(
        ELEVATION DOUBLE,
        LATITUDE DOUBLE,
        LONGITUDE DOUBLE,
        PRECIPITATION DOUBLE,
        RECORD_DATE DOUBLE,
        SNOW DOUBLE,
        TEMP_MAX DOUBLE,
        TEMP_MIN DOUBLE,
        WIND DOUBLE)
        """)
  data_file = str(os.path.join(os.path.dirname(__file__),'..','..','dataset_weather_1M_fixed.csv'))
  cursor.execute("copy weather from '"+data_file+"' header ")

  print("loading flights")
  cursor.execute("DROP TABLE IF EXISTS flights");
  cursor.execute("""
        CREATE TABLE if not exists flights(
            AIR_TIME DOUBLE,
            ARR_DELAY DOUBLE,
            ARR_TIME DOUBLE,
            DEP_DELAY DOUBLE,
            DEP_TIME DOUBLE,
            DISTANCE DOUBLE,
            FL_DATE TEXT)
        """)
  data_file = str(os.path.join(os.path.dirname(__file__),'..','..','dataset_flights_1M.csv'))
  cursor.execute("copy flights from '"+data_file+"' header ")
  #conn.close()

if __name__ == "__main__":
  try:
    duckdbConfig = json.load(open(os.path.join(os.path.dirname(__file__),'..','..','duckdb.config.json')))
    dbFilename = duckdbConfig['dbFilename']
    run(dbFilename)
  except Exception as e:
    print(e)
    print("usage: python",sys.argv[0],"[db filename]")
    sys.exit(0)
