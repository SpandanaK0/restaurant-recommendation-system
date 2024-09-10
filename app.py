import requests

# Set your Yelp API key here
api_key = "YMSQ-Za-PHd7vxw10CXHANqfyfcywjshobT6bMVpQ_wvldX1ztbMFShrVVIGOyPfK_6jUoRzvpPC72remPsCqQ6DWahsRiQo9og-zG9sAPx271hdT_ZmZSfH7TzfZnYx"
api_host = "https://api.yelp.com"
search_path = "/v3/businesses/search"

# Yelp API request headers with the API key
HEADERS = {"Authorization": f"Bearer {api_key}"}


# Function to search for restaurants using Yelp API
def search_restaurants(location, term="restaurants", preference=None, min_rating=0, radius=10000, limit=10):
    url = f"{api_host}{search_path}"

    if preference:
        term += f", {preference}"

    # Set query parameters with radius included
    params = {
        'term': term,
        'location': location,
        'limit': limit,
        'radius': radius  # Radius in meters
    }

    # Make the request
    response = requests.get(url, headers=HEADERS, params=params)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Error making request to Yelp API: {response.status_code}")

    # Parse the JSON response
    data = response.json()

    # Extract restaurant information and filter by minimum rating
    restaurants = []
    for business in data.get('businesses', []):
        name = business['name']
        rating = business['rating']
        address = " ".join(business['location']['display_address'])

        # Only include restaurants with a rating greater than or equal to min_rating
        if rating >= min_rating:
            restaurants.append({'name': name, 'rating': rating, 'address': address})

    # Sort the restaurants by rating in descending order
    restaurants = sorted(restaurants, key=lambda x: x['rating'], reverse=True)

    return restaurants


# Main function to handle user input and display the restaurant information
def main():
    location = input("Enter the location to search for restaurants: ")
    preferences = input("Enter any dietary preferences (e.g., vegetarian, gluten_free) or press enter to use 'None': ")
    min_rating = float(input("Enter the minimum rating (e.g., 4.0): "))

    # Ask the user for the radius in miles
    radius_miles = float(input("Enter the search radius in miles: "))

    # Convert miles to meters (1 mile = 1609.34 meters)
    radius_meters = radius_miles * 1609.34

    # Call search_restaurants with location, preferences, min_rating, and radius in meters
    restaurants = search_restaurants(location, term="restaurants", preference=preferences if preferences else None,
                                     min_rating=min_rating, radius=int(radius_meters))

    if not restaurants:
        print(
            f"No restaurants found in {location} with a rating of {min_rating} or higher within {radius_miles} miles.")
        return

    print(f"Top {len(restaurants)} Restaurants in {location}:")
    for idx, restaurant in enumerate(restaurants):
        print(f"{idx + 1}. {restaurant['name']} - Rating: {restaurant['rating']} - Address: {restaurant['address']}")


# Entry point of the program
if __name__ == "__main__":
    main()
