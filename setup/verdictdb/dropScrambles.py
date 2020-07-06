import os
import pyverdict,json

verdictdbConfig = json.load(open(os.path.join(os.path.dirname(__file__),'..','..','verdictdb.config.json')))
port=verdictdbConfig['port']
password=verdictdbConfig['password']
conn=pyverdict.postgres(host='localhost',user='crossfilter',password=password,port=port,dbname='crossfilter-eval-db')
conn.set_loglevel("ERROR")
df=conn.sql('DROP SCRAMBLE "public"."movies_scrambled_10_percent" on "public"."movies" SIZE 0.1')
df=conn.sql('DROP SCRAMBLE "public"."movies_scrambled_50_percent" on "public"."movies" SIZE 0.5')
df=conn.sql('DROP SCRAMBLE "public"."flights_scrambled_10_percent" on "public"."flights" SIZE 0.1')
df=conn.sql('DROP SCRAMBLE "public"."flights_scrambled_50_percent" on "public"."flights" SIZE 0.5')
df=conn.sql('DROP SCRAMBLE "public"."weather_scrambled_10_percent" on "public"."weather" SIZE 0.1')
df=conn.sql('DROP SCRAMBLE "public"."weather_scrambled_50_percent" on "public"."weather" SIZE 0.5')


