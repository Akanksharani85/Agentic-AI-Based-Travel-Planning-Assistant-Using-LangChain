import json
import requests

# --- Helper Function ---
def load_data(filename):
    try:
        with open(f"data/{filename}", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# --- 1. Flight Search Tool (Single Argument wala) ---
def search_flights(query):
    """
    Input: "Source, Destination" (Example: "Delhi, Goa")
    """
    try:
        # Agar agent ne comma nahi lagaya, toh error bhej do
        if "," not in query:
            return "Error: Input must be 'Source, Destination' (e.g. Delhi, Goa)"
        
        # Comma se tod kar Source aur Destination alag karo
        source, destination = query.split(",", 1)
        source = source.strip()
        destination = destination.strip()
        
        flights = load_data("flights.json")
        
        # Match karo
        results = [
            f for f in flights 
            if f["from"].lower() == source.lower() and f["to"].lower() == destination.lower()
        ]
        
        if not results:
            return f"Sorry, {source} se {destination} ke liye koi flight nahi mili."
        
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error in flight search: {str(e)}"

# --- 2. Hotel Search Tool ---
def search_hotels(city):
    hotels = load_data("hotels.json")
    # City ya Location match karo
    results = [h for h in hotels if h.get("city", "").lower() == city.lower() or h.get("location", "").lower() == city.lower()]
    
    if not results:
        return f"Sorry, {city} mein koi hotel nahi mila."
    
    return json.dumps(results, indent=2)

# --- 3. Places Search Tool ---
def search_places(city):
    places = load_data("places.json")
    results = [p for p in places if p.get("city", "").lower() == city.lower()]
    
    if not results:
        return f"Sorry, {city} mein ghumne ki jagah nahi mili."
    
    return json.dumps(results, indent=2)

# --- 4. Weather Tool ---
def get_weather(city):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_response = requests.get(geo_url).json()
        
        if "results" not in geo_response:
            return f"Weather Error: {city} nahi mila."
            
        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_data = requests.get(weather_url).json()
        
        temp = weather_data["current_weather"]["temperature"]
        wind = weather_data["current_weather"]["windspeed"]
        
        return f"Current Weather in {city}: {temp}°C, Wind Speed: {wind} km/h."
    except Exception as e:
        return f"Weather check error: {str(e)}"