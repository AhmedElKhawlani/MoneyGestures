#!/bin/bash

# Exit script on any error
set -e

# Update package list and install dependencies
echo "Updating package list and installing dependencies..."
sudo apt update
sudo apt install -y python3 python3-venv python3-pip mysql-server

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install required Python libraries
pip install flask
pip install sqlalchemy
pip install logging
pip install secrets

# Install and secure MySQL
echo "Setting up MySQL..."
sudo systemctl start mysql
sudo mysql_secure_installation <<EOF

y
ahmedandamin
ahmedandamin
y
y
y
y
EOF

# Log into MySQL and create user and database
echo "Creating MySQL user and database..."
sudo mysql -u root -e "
CREATE USER 'ahmedandamin'@'localhost' IDENTIFIED BY 'ahmedandamin';
GRANT ALL PRIVILEGES ON *.* TO 'ahmedandamin'@'localhost';
FLUSH PRIVILEGES;
CREATE DATABASE money_management;
"

# Notify completion
echo "Installation completed successfully! To start the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the Flask application."
