# Django Weather API

This project is a simple, robust weather API built with Django. It acts as a proxy, fetching data from the [Visual Crossing weather API](https://www.visualcrossing.com/weather-api), caching the results with Redis for high performance, and protecting the endpoint with rate limiting.

This project serves as a practical example of how to integrate 3rd-party services, manage secure environment variables, implement caching, and secure an API in a Django application.

Project idea from: [roadmap.sh/projects/weather-api-wrapper-service](https://roadmap.sh/projects/weather-api-wrapper-service)

## 🚀 Features

- **3rd Party API Integration:** Fetches live weather data from the Visual Crossing API.
- **High-Speed Caching:** Uses **Redis** and `django-redis` to cache API responses for 12 hours, ensuring instant responses for repeated requests.
- **Rate Limiting:** Uses `django-ratelimit` to protect the API from abuse, limiting requests to 5 per minute per IP.
- **Secure Configuration:** All secret keys and API keys are stored securely in a `.env` file, not in the code.
- **Clean API Response:** Parses the full 3rd-party response and returns a simple, clean JSON object.

## 🛠️ Technology Stack

- **Backend:** Python, Django
- **Cache:** Redis
- **Python Packages:**
  - `django`
  - `django-redis` (For Redis caching)
  - `django-ratelimit` (For IP-based rate limiting)
  - `python-dotenv` (For managing environment variables)
  - `redis` (Redis Python client)

---

## 🏁 Getting Started

Follow these instructions to get a local copy of the project up and running on your machine.

### 1. Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Redis Server](https://redis.io/docs/latest/operate/oss_and_stack/install/).
  - _On macOS (Homebrew):_ `brew install redis && brew services start redis`
  - _On Linux (Ubuntu):_ `sudo apt install redis-server`
  - _On Windows(WSL):_ Follow Linux instructions within WSL. Alternatively, use the [Redis for Windows installer](https://github.com/tporadowski/redis/releases).

### 2. Setup & Installation

1.  **Clone the repository (or download the files):**

    ```bash
    git clone https://your-repo-url/django-weather-api.git
    cd django-weather-api
    ```

2.  **Create and activate a Python virtual environment:**

    ```bash
    # On macOS/Linux
    python3 -m venv env
    source env/bin/activate

    # On Windows
    python -m venv env
    .\env\Scripts\activate
    ```

3.  **Install the required packages:**
    First, create a `requirements.txt` file by running: `pip freeze > requirements.txt`
    Then, install from the file:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create your `.env` file:**
    In the project's root directory, create a file named `.env`. Copy the contents of `.env.example` (or the block below) into it and add your keys.

    **`.env` file:**

    ```ini
    # --- .env file ---
    # You can generate a new one, or use the one from your settings.py
    SECRET_KEY="your-long-random-django-secret-key"

    # Get your API key from [https://www.visualcrossing.com/weather-api](https://www.visualcrossing.com/weather-api)
    VISUAL_WEATHER_API_KEY="your-visual-crossing-api-key"
    ```

5.  **Run the Django development server:**
    ```bash
    python manage.py runserver
    ```
    The API will now be running at `http://127.0.0.1:8000/`.

---

## Usage

### API Endpoint

Send a `GET` request to the `/weather/<city>/` endpoint to get the current day's forecast.

**URL:** `http://127.0.0.1:8000/weather/<city>/`

**Example (using `london`):**
`http://127.0.0.1:8000/weather/london/`

### Example Success Response

The API returns a clean JSON object with only the essential data.

```json
{
  "location": "London, England, UK",
  "date": "2025-11-17",
  "temp_max": 12.0,
  "temp_min": 7.5,
  "conditions": "Partly cloudy throughout the day."
}
```

## Home Page Frontend

This project includes a simple home page frontend that allows you to enter a country (or city) and view the weather for today plus the next 5 days.

- **Where:** The template is `weather/templates/home.html` (served at the project root/home URL).
- **What it does:** Accepts a country/city input and displays today's weather and a 5-day forecast using the same backend API.
- **How to use:** Run the Django server with `python manage.py runserver` and open `http://127.0.0.1:8000/` in your browser. Enter a country or city and submit to see the current weather and upcoming 5-day forecast.
