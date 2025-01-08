#!/bin/bash

# Exit script on any error
set -e

# Update package list and install dependencies
echo "Updating package list and installing dependencies..."
sudo apt update
sudo apt install build-essential
sudo apt install libstdc++6
sudo apt install -y python3 python3-venv python3-pip mysql-server

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install required Python libraries
pip install flask
pip install sqlalchemy
pip install sqlalchemy_utils
pip install pymysql
pip install cryptography

# Opening mysql
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

MYSQL_USER_EXISTS=$(sudo mysql -u root -sse "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = 'ahmedandamin' AND host = 'localhost');")
if [ "$MYSQL_USER_EXISTS" == 0 ]; then
    echo "User 'ahmedandamin' does not exist. Creating user..."
    sudo mysql -u root -e "
    CREATE USER 'ahmedandamin'@'localhost' IDENTIFIED BY 'ahmedandamin';
    GRANT ALL PRIVILEGES ON *.* TO 'ahmedandamin'@'localhost';
    FLUSH PRIVILEGES;
    "
else
    echo "User 'ahmedandamin' already exists. Skipping user creation."
fi


# Notify completion
echo "Installation completed successfully! To start the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the Flask application."
