#!/bin/bash
# Update package lists and install PostgreSQL headers for psycopg2 compilation
apt-get update
apt-get install -y libpq-dev

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
