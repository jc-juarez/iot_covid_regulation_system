-- -------------------------------------
-- IoT Covid-19 Regulation System
-- Back-end Service - Database 
-- 'db.sql'
-- Author: Juan Carlos Juárez
-- Contact: jc.juarezgarcia@outlook.com
-- -------------------------------------

-- IMPORTANT: Execute this .sql file before starting up the Back-end Service and Front-end App

CREATE TABLE entrance (
    datetime TEXT NOT NULL
);

CREATE TABLE exit (
    datetime TEXT NOT NULL
);

CREATE TABLE capacity (
    main_id TEXT NOT NULL,
    max_capacity INTEGER NOT NULL
);

CREATE TABLE temperature (
    main_id TEXT NOT NULL,
    current_temperature INTEGER NOT NULL
);

INSERT INTO capacity (main_id, max_capacity)
VALUES("main", 3);

INSERT INTO temperature (main_id, current_temperature)
VALUES("main", 0);