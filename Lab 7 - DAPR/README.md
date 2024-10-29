# Lab 7 - DAPR

This project is a simple REST API built with Flask, leveraging DAPR's state management capabilities to store, retrieve, and delete key-value pairs. DAPR is configured with Redis as the default state store.

## Prerequisites

- Python
- DAPR CLI
- Docker Desktop

## Running the application

1. Make sure that Docker Desktop is running as DAPR uses this to self host Redis.
2. Navigate to the correct directory:

    ```bash
    cd flask-dapr-app
    ```

3. Make a virtual environment and install dependencies.

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4. Run the app using DAPR.
        
    ```bash
    dapr run --app-id flask-dapr-app --app-port 5001 --dapr-http-port 3500 -- python server.py
    ```
