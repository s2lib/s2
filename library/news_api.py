import requests

def get_news():
    API_KEY = "bcb6117e036d4840b092bbba67211a97"  # Replace with your News API key
    URL = "https://newsapi.org/v2/everything"
    params = {
        "q": "education",  # Keyword to search
        "pageSize": 20,  # Limit the number of articles
        "apiKey": API_KEY,
    }
    response = requests.get(URL, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response Data: {response.json()}")  # Debug: Print full response
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

if __name__ == "__main__":
    news_articles = get_news()
    print("News Articles Retrieved:")
    for article in news_articles[:5]:  # Limit output to first 5 articles
        print(f"- {article['title'] if 'title' in article else 'No Title'}")
