from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import urllib.request
import urllib.parse
import json
import pandas as pd
import io
import uvicorn

app = FastAPI(title="Global Meteorological Analysis REST API")

class WeatherRequest(BaseModel):
    location: str
    start_date: str
    end_date: str

def geocode_location(name: str):
    encoded_name = urllib.parse.quote(name)
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_name}&count=1&language=en&format=json"
    try:
        with urllib.request.urlopen(geo_url, timeout=10) as response:
            data = json.loads(response.read().decode())
        if not data.get("results"):
            return None
        result = data["results"][0]
        return result["latitude"], result["longitude"], f"{result['name']}, {result.get('admin1', '')} ({result.get('country', '')})"
    except Exception as e:
        print(f"Geocoding Error: {e}")
        return None

@app.post("/api/weather")
def analyze_weather_data(request: WeatherRequest):
    print(f"Received request for: {request.location} ({request.start_date} to {request.end_date})")
    
    coordinates = geocode_location(request.location)
    if not coordinates:
        raise HTTPException(status_code=404, detail=f"'{request.location}' coordinates not found.")
    
    lat, lon, full_name = coordinates
    
    api_url = (
        f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
        f"&start_date={request.start_date}&end_date={request.end_date}"
        f"&daily=temperature_2m_max,precipitation_sum&timezone=auto&format=csv"
    )
    
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            csv_data = response.read().decode('utf-8')
        
        lines = csv_data.splitlines()
        
        if lines and (lines[0].startswith("{") or "error" in csv_data.lower()):
            error_details = json.loads(csv_data)
            raise ValueError(error_details.get("reason", "API returned an error wrapper."))

        header_row = -1
        for idx, line in enumerate(lines):
            if 'time' in line.lower() and 'temperature' in line.lower():
                header_row = idx
                break
        
        if header_row == -1:
            raise ValueError("Could not find the data header row in the API response.")
                
        df = pd.read_csv(io.StringIO(csv_data), skiprows=header_row)
        df.columns = ['Date', 'Max_Temp', 'Rainfall']
        
        # Standardize formats
        df = df.dropna(subset=['Date'])
        df['Date'] = df['Date'].astype(str)
        df['Max_Temp'] = pd.to_numeric(df['Max_Temp'], errors='coerce')
        df['Rainfall'] = pd.to_numeric(df['Rainfall'], errors='coerce').clip(lower=0)
        
        if len(df) == 0:
            raise ValueError("No valid data rows found for these dates.")
            
        df[['Max_Temp', 'Rainfall']] = df[['Max_Temp', 'Rainfall']].interpolate(method='linear').bfill().ffill()
        
        return {
            "status": "success",
            "full_name": full_name,
            "mean_max_temp": float(df['Max_Temp'].mean()) if not pd.isna(df['Max_Temp'].mean()) else 0.0,
            "total_precipitation": float(df['Rainfall'].sum()) if not pd.isna(df['Rainfall'].sum()) else 0.0,
            "chart_data": {
                "dates": df['Date'].tolist(),
                "max_temps": [float(x) for x in df['Max_Temp'].tolist()],
                "rainfall": [float(x) for x in df['Rainfall'].tolist()]
            }
        }
    except Exception as e:
        print(f"CRITICAL SERVER ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Backend Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)