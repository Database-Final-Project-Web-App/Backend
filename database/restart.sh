#!/bin/bash
# if first argument is more, use atrs_insert_more.sql instead of atrs_insert.sql

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

EOF

# If the first argument is "more", insert more data
if [ "$1" == "more" ]; then
	mysql -u root <<EOF

	-- Select the newly created database
	USE atrs;

	-- Step 4: Execute the "atrs_insert_more.sql" file
	source ./atrs_insert_more.sql;

EOF

# Otherwise, insert the default data
else
	mysql -u root <<EOF

	-- Select the newly created database
	USE atrs;

	-- Step 4: Execute the "atrs_insert.sql" file
	source ./atrs_insert.sql;

EOF
fi

# Print a message
echo "Restarted the database"