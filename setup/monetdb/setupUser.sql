CREATE USER "crossfilter" WITH PASSWORD 'XA*yiTx_8Hko' NAME 'crossfilter' SCHEMA "sys";
grant all privileges on sys.flights to crossfilter;
grant all privileges on sys.movies to crossfilter;
grant all privileges on sys.weather to crossfilter;

/*
CREATE ROLE "crossfilterrole" WITH ADMIN CURRENT_USER;
GRANT COPY FROM TO "crossfilterrole";
GRANT COPY INTO TO "crossfilterrole";
CREATE SCHEMA "cfschema" AUTHORIZATION "crossfilterrole";
GRANT "crossfilterrole" TO "crossfilter" WITH ADMIN OPTION;
ALTER USER "crossfilter" SET SCHEMA "cfschema";
*/
