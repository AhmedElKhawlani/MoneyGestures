#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting the application..."

# Activate the virtual environment
source venv/bin/activate

sudo systemctl start mysql

# Run the application in the background
echo "Running app.py..."
python app.py &

# Capture the process ID of the application
APP_PID=$!

# Wait for the server to start
echo "Waiting for the server to start..."
sleep 3

# Open the browser to the application URL using the system's default browser
echo "Opening browser at http://127.0.0.1:5000/"
if command -v xdg-open &> /dev/null; then
    xdg-open "http://127.0.0.1:5000/"
elif command -v open &> /dev/null; then
    open "http://127.0.0.1:5000/"
elif command -v start &> /dev/null; then
    start "http://127.0.0.1:5000/"
else
    echo "No suitable command found to open the browser. Please open http://127.0.0.1:5000/ manually."
fi

# Wait for the app to terminate (optional)
wait $APP_PID
