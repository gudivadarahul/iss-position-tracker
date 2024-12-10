# ISS Position Tracker

Tracks the International Space Station position and stores the data using Redis.

## Features

- Polls ISS Position API every 5 seconds
- Stores and updates position in Redis database
- Includes error handling for API and database operations

## Requirements

- Python 3
- Redis
- Python packages: `redis`, `requests`

## Setup

```bash
pip3 install redis requests
```

## Running

1. Start Redis server
2. Run the script:

```bash
python3 iss_tracker.py
```

## Usage

The script will automatically:

- Fetch ISS position every 5 seconds
- Store position in Redis
- Display current position data
- Run until interrupted (Ctrl+C)
