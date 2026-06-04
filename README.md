# Global Weather Analysis Dashboard (FastAPI & Tkinter)

An interactive desktop application to search and analyze historical weather data. The project uses a **FastAPI backend** to handle data and a **Tkinter frontend** to show the dashboard.

- **FastAPI Powered**: The backend server manages all API requests and data processing.
- **Asynchronous Threading**: The desktop window stays smooth and responsive during data downloads.
- **Data Cleaning**: The app automatically fixes missing data gaps using linear interpolation.
- **Embedded Charts**: Custom dual-axis charts display inside the application frame using Matplotlib.

---

## Application Preview

![Global Weather Analysis Dashboard Interface](/images/image.png)

---

## Technical Features
* **REST API Architecture** – Separates the backend server (`server.py`) from the frontend GUI (`main.py`).
* **Pydantic Validation** – Checks the input data structure (location and dates) before processing.
* **Geocoding API** – Converts city names into precise latitude and longitude coordinates.
* **Pandas Data Processing** – Cleans CSV files, manages time-series data, and calculates climate statistics.
* **Dual-Axis Visualization** – Draws a high-contrast dark chart comparing Max Temperature (Line) and Rainfall (Bar).

---

## Core Technologies
* **Python 3.9+** – The primary programming language.
* **FastAPI & Uvicorn** – The REST API framework and the ASGI server.
* **Pydantic** – For data validation.
* **Tkinter & TTK** – For building the desktop user interface.
* **Pandas** – For data manipulation.
* **Matplotlib** – For rendering the data charts.
* **Multi-threading** – For managing background network requests.

---

## Program Workflow
1. **User Input**: The user enters a location and selects a date range on the Tkinter GUI.
2. **HTTP POST Request**: The frontend sends a JSON payload to the FastAPI backend.
3. **Data Fetching & Cleaning**: The backend contacts the Open-Meteo API, processes the CSV data with Pandas, and calculates metrics.
4. **JSON Response**: The backend sends the structured data back to the frontend.
5. **UI Update**: The frontend receives the data, updates the KPI cards, and redraws the Matplotlib canvas.
