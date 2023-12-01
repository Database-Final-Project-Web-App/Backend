#!/bin/bash

# Connect to the MySQL server, replace user and pass with your MySQL username and password
mysql -u root <<EOF

-- Step 1: Drop the "atrs" database
DROP DATABASE IF EXISTS atrs;

-- Step 2: Create a new database with the same name
CREATE DATABASE atrs;

-- Select the newly created database
USE atrs;

-- Step 3: Execute the "atrs_create.sql" file
source ./atrs_create.sql;

-- Step 4: Execute the "atrs_insert.sql" file
source ./atrs_insert.sql;

EOF