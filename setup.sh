#!/bin/bash

echo "Starting Camera Alert System setup..."

# Check if containers are running
if ! docker-compose ps | grep -q "Up"; then
    echo "Starting containers..."
    docker-compose up -d
else
    echo "Containers are already running"
fi

# Wait for containers to be ready
echo "Waiting for containers to be ready..."
sleep 10

# Run the setup script
echo "Running setup script..."
docker-compose exec web python scripts/setup.py

# Install requests package if not already installed
echo "Checking required packages..."
docker-compose exec web pip install requests

echo "Setup complete! You can now:"
echo "1. Access the API at http://localhost:7001"
echo "2. Access the frontend at http://localhost:5173"
echo "3. Login with:"
echo "   Email: test@example.com"
echo "   Password: testpassword" 