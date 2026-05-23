# Global Weather Analysis Dashboard (Python & Tkinter)

An interactive desktop GUI weather analysis application written in Python. This project shows the usage of **Pandas, Matplotlib, multi-threaded networking, and automated API parsing**.

- **Dynamic Search**: Instantly coordinates and pulls weather data for any global city using integrated Geocoding.
- **Cleans & Calculates**: Smooths over missing data gaps and instantly highlights core climate statistics.
- **Embedded Charts**: Renders custom hardware-accelerated dual-axis visualizations directly inside the application frame.
- **Responsive Threading**: Keeps the window fully interactive and lag-free during background internet downloads.

---

## Features
* **Automated Data Acquisition** – Translates city names to coordinates and pulls historical metrics via Open-Meteo APIs.
* **Asynchronous Networking** – Implements Python threading to isolate API requests from the main interface loop.
* **Data Resiliency & Cleaning** – Dynamically detects shifting API headers, handles anomalies, and fills missing values using linear interpolation.
* **Dual-Axis Visualization** – Generates a high-contrast dark dashboard comparing Max Temperature (Line) vs. Rainfall (Bar).
* **Local Persistence** – Provisions data locally into a background working file (`downloaded_data.csv`).

---

## Concepts Used
* **Tkinter & TTK** – For building a modern card-based desktop layout environment.
* **Pandas** – For robust data restructuring, time-series operations, and CSV tracking.
* **Matplotlib (`backend_tkagg`)** – For drawing dark-themed canvas visualizations embedded inside native OS windows.
* **Multi-threading** – For separating network latency blocks from UI drawing operations.
* **Urllib & JSON Parsing** – For handling structural web requests and payload extraction.

---

## Program Workflow
1. **Geocode**: Converts free-text location entry queries into spatial coordinate points.
2. **Download**: Pulls structured weather archives matching selected coordinate bounds.
3. **Analyze**: Parses file indices dynamically and displays summary data fields.
4. **Plot**: Refreshes an embedded Matplotlib canvas using an optimized layout.

---

## How to Use
1. Enter a city name
2. Specify the desired date range for historical weather analysis
3. Start the download process
4. Review generated climate statistics and embedded visualizations