import os
import sys
import sqlite3
import pandas
import json

def loadData(tableName,conn,csvfile):
  print("loading",tableName)
  df = pandas.read_csv(csvfile)
  df.to_sql(tableName, conn, if_exists='append', index=False)
  print("done loading",tableName)

def run(dbFilename):
  conn = sqlite3.connect(dbFilename)
  cursor = conn.cursor()

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
  loadData("movies",conn,os.path.join(os.path.dirname(__file__),'..','..','dataset_movies_1M_fixed.csv'))

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
  loadData("weather",conn,os.path.join(os.path.dirname(__file__),'..','..',"dataset_weather_1M_fixed.csv"))

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
  loadData("flights",conn,os.path.join(os.path.dirname(__file__),'..','..',"dataset_flights_1M.csv"))
  conn.commit()
  conn.close()

if __name__ == "__main__":
  try:
    sqliteConfig = json.load(open(os.path.join(os.path.dirname(__file__),'..','..','sqlite.config.json')))
    dbFilename = sqliteConfig['dbFilename']
    run(dbFilename)
  except Exception as e:
    print(e)
    print("usage: python",sys.argv[0],"[db filename]")
    sys.exit(0)
