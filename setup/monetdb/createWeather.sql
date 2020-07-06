drop table if exists sys.weather;
create table sys.weather(
  ELEVATION DOUBLE PRECISION,
  LATITUDE DOUBLE PRECISION,
  LONGITUDE DOUBLE PRECISION,
  PRECIPITATION DOUBLE PRECISION,
  RECORD_DATE DOUBLE PRECISION,
  SNOW DOUBLE PRECISION,
  TEMP_MAX DOUBLE PRECISION,
  TEMP_MIN DOUBLE PRECISION,
  WIND DOUBLE PRECISION
);