-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.7.0
-- PostgreSQL version: 9.3
-- Project Site: pgmodeler.com.br
-- Model Author: ---

SET check_function_bodies = false;
-- ddl-end --

-- object: rpotok_cp1 | type: ROLE --
-- DROP ROLE rpotok_cp1;
CREATE ROLE rpotok_cp1 WITH 
	SUPERUSER;
-- ddl-end --


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: oilgas | type: DATABASE --
-- -- DROP DATABASE oilgas;
-- CREATE DATABASE oilgas
-- ;
-- -- ddl-end --
-- 

-- object: nd_production_cp1 | type: SCHEMA --
-- DROP SCHEMA nd_production_cp1;
—-CREATE SCHEMA nd_production_cp1;
—-ALTER SCHEMA nd_production_cp1 OWNER TO rpotok_cp1;
-- ddl-end --

SET search_path TO pg_catalog,public,nd_production —-,nd_production_cp1;
-- ddl-end --

-- object: nd_production.scout | type: TABLE --
-- DROP TABLE nd_production.scout;
CREATE TABLE nd_production.scout(
	uid uuid NOT NULL,
	ndic smallint,
	api text,
	status_date date,
	wellbore_type text,
	pt geometry(POINT),
	total_depth float,
	CONSTRAINT "primary key" PRIMARY KEY (uid)

);
-- ddl-end --
-- object: nd_production.lasfiles | type: TABLE --
-- DROP TABLE nd_production.lasfiles;
CREATE TABLE nd_production.lasfiles(
	id smallint NOT NULL,
	scout_id uuid,
	lasfile text,
	CONSTRAINT id_pk PRIMARY KEY (id)

);
-- ddl-end --
-- object: nd_production.scout_data | type: TABLE --
-- DROP TABLE nd_production.scout_data;
CREATE TABLE nd_production.scout_data(
	id smallint NOT NULL,
	scout_id uuid,
	total_oil float,
	total_gas float,
	total_water float,
	perfs float,
	CONSTRAINT pk PRIMARY KEY (id)

);
-- ddl-end --
-- object: nd_production.scout_weblink | type: TABLE --
-- DROP TABLE nd_production.scout_weblink;
CREATE TABLE nd_production.scout_weblink(
	id smallint NOT NULL,
	scout_id uuid,
	production_link text,
	direction_weblink text,
	CONSTRAINT pk PRIMARY KEY (id)

);
-- ddl-end --
-- object: nd_production.production | type: TABLE --
-- DROP TABLE nd_production.production;
CREATE TABLE nd_production.production(
	id smallint NOT NULL,
	scout_id uuid,
	production_date date,
	oil float,
	water float,
	gas float,
	number_days smallint,
	CONSTRAINT pk PRIMARY KEY (id)

);
-- ddl-end --
-- object: nd_production.direction | type: TABLE --
-- DROP TABLE nd_production.direction;
CREATE TABLE nd_production.direction(
	id smallint,
	scout_id uuid,
	geom geometry(LINESTRING),
	CONSTRAINT pk PRIMARY KEY (id)

);
-- ddl-end --
-- object: nd_production.production_sold | type: TABLE --
-- DROP TABLE nd_production.production_sold;
CREATE TABLE nd_production.production_sold(
	id smallint NOT NULL,
	scout_id uuid,
	production_date date,
	oil float,
	water float,
	gas float,
	number_days smallint,
	CONSTRAINT pk PRIMARY KEY (id)

);
-- ddl-end --
-- object: scout_id_fk | type: CONSTRAINT --
-- ALTER TABLE nd_production.lasfiles DROP CONSTRAINT scout_id_fk;
ALTER TABLE nd_production.lasfiles ADD CONSTRAINT scout_id_fk FOREIGN KEY (scout_id)
REFERENCES nd_production.scout (uid) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


-- object: scout_id_fk | type: CONSTRAINT --
-- ALTER TABLE nd_production.scout_data DROP CONSTRAINT scout_id_fk;
ALTER TABLE nd_production.scout_data ADD CONSTRAINT scout_id_fk FOREIGN KEY (scout_id)
REFERENCES nd_production.scout (uid) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


-- object: scout_id_fk | type: CONSTRAINT --
-- ALTER TABLE nd_production.scout_weblink DROP CONSTRAINT scout_id_fk;
ALTER TABLE nd_production.scout_weblink ADD CONSTRAINT scout_id_fk FOREIGN KEY (scout_id)
REFERENCES nd_production.scout (uid) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


-- object: scout_id_fk | type: CONSTRAINT --
-- ALTER TABLE nd_production.production DROP CONSTRAINT scout_id_fk;
ALTER TABLE nd_production.production ADD CONSTRAINT scout_id_fk FOREIGN KEY (scout_id)
REFERENCES nd_production.scout (uid) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


-- object: scout_id_fk | type: CONSTRAINT --
-- ALTER TABLE nd_production.direction DROP CONSTRAINT scout_id_fk;
ALTER TABLE nd_production.direction ADD CONSTRAINT scout_id_fk FOREIGN KEY (scout_id)
REFERENCES nd_production.scout (uid) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


-- object: scout_id_fk | type: CONSTRAINT --
-- ALTER TABLE nd_production.production_sold DROP CONSTRAINT scout_id_fk;
ALTER TABLE nd_production.production_sold ADD CONSTRAINT scout_id_fk FOREIGN KEY (scout_id)
REFERENCES nd_production.scout (uid) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --



