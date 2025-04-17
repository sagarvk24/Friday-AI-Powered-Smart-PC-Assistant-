import requests
import wikipedia
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Read keys
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
NEWS_URL = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"

def get_weather(city):
    try:
        params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
        response = requests.get(WEATHER_URL, params=params).json()
        
        if response.get("cod") != 200:
            return f"Weather error: {response.get('message', 'Unknown issue.')}"
        
        temp = response.get("main", {}).get("temp", "N/A")
        weather_desc = response.get("weather", [{}])[0].get("description", "N/A").capitalize()
        return f"The current temperature in {city} is {temp}°C with {weather_desc}."
    except Exception as e:
        return f"Error fetching weather: {e}"

def get_wikipedia_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return "No Wikipedia page found for this topic."

def get_news():
    try:
        response = requests.get(NEWS_URL).json()
        if response.get("status") != "ok":
            return "Sorry, I couldn't fetch the latest news."
        
        articles = response["articles"][:5]
        headlines = [
            f"{i+1}. {article['title']} ({article['source']['name']})"
            for i, article in enumerate(articles)
        ]
        return "\n".join(headlines)
    except Exception as e:
        return f"Error fetching news: {e}"

if __name__ == "__main__":
    print(get_weather("Dehradun"))
    print(get_wikipedia_summary("Virat Kohli"))
    print(get_news())
