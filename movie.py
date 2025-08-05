import requests
from bs4 import BeautifulSoup

def fetch_movies(url, headers):
    # Send a GET request to the URL with the specified headers
    response = requests.get(url, headers=headers)

    # Parse the response content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def extract_movie_data(soup):
    movie_data = []
    # Find all movie containers in order to avoid IMDb Charts title which has same class as movie titles
    movie_containers = soup.find_all('div', class_ = 'ipc-metadata-list-summary-item__tc')

    # Loop through each container, extract, and store the name and rating of each movie
    for container in movie_containers:
        movie_name = container.find('h3', class_ = 'ipc-title__text ipc-title__text--reduced').text.split(". ")[1]
        movie_rating = container.find('span', class_ = 'ipc-rating-star--rating').text

        # Convert movie rating to a float value and add to movie list; handle conversion errors
        try:
            movie_rating = float(movie_rating)
            movie_data.append((movie_name, movie_rating))

        except ValueError:
            print(f"The rating '{movie_rating}' for '{movie_name}' could not be converted to a float.")

    return movie_data

def print_sorted_movies(movies, min_rating):
    # Sort the movies by rating (ascending order)
    sorted_movies = sorted(movies, key=lambda x: x[1])

    # Filter and print the movies that meet or exceed the min_rating
    for movie in sorted_movies:
        if movie[1] >= min_rating:
            print(f"Movie Name: {movie[0]}, Rating: {movie[1]}")

# Main program
url = "https://www.imdb.com/chart/top"
# Headers to mimic a browser request for bypassing potential access restrictions
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

soup = fetch_movies(url, headers)
movies = extract_movie_data(soup)

while True:
    try:
        min_rating = float(input("Please provide the minimum rating threshold for your movie recommendation list: "))
        print()
        break
    
    except ValueError:
        print(f"The value you provided could not be converted into a float value. Please try again.")
        print()

print_sorted_movies(movies, min_rating)
