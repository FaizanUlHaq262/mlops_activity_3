# Faizans WebApp

A simple containerized application for tracking income, built with Flask, SQLite, and Docker.

## Features

- Track your income
- Simple and intuitive UI

## Architecture

This application is built with a three-tier architecture:

1. **Frontend**: Flask-based web interface
2. **Backend**: RESTful API built with Flask
3. **Database**: SQLite database for data persistence

Each component runs in its own Docker container, orchestrated with Docker Compose.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system

### Running the Application

1. Clone this repository
2. Navigate to the project directory
3. Run the following command:

```bash
docker-compose up
```

4. Access the application at http://localhost:5000

## Development

The application is configured with volume mounts for real-time code updates during development. Any changes made to the code will be reflected immediately without requiring a container rebuild.

## Container Structure

- **Frontend Container**: Serves the Flask web interface on port 5000
- **Backend Container**: Provides the RESTful API on port 5001
- **Database Initialization Container**: Sets up the SQLite database with initial sample data

## API Endpoints

### Income
- `GET /api/income` - Get all income entries
- `POST /api/income` - Add a new income entry 