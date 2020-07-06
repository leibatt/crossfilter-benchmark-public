drop table if exists sys.movies;
create table sys.movies(
  IMDB_Rating DOUBLE PRECISION,
  Production_Budget DOUBLE PRECISION,
  Release_Date DOUBLE PRECISION,
  Rotten_Tomatoes_Rating DOUBLE PRECISION,
  Running_Time_min DOUBLE PRECISION,
  US_DVD_Sales DOUBLE PRECISION,
  US_Gross DOUBLE PRECISION,
  Worldwide_Gross DOUBLE PRECISION
);
