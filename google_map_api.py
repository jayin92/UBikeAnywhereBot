import requests

#info from https://developers.google.com/places/web-service/search

def google_map_api:

    api_key = "AIzaSyD57zm-VEPud6YTbl6XKpu7kZIdlHxHZIQ"

    input_type = "textquery"

    my_params = {
        "address" : search_place,
        "key" : api_key,
    }

    request_url = "https://maps.googleapis.com/maps/api/geocode/json"

    result = requests.get(request_url, params = my_params)

    if result.status_code == 200:
        json = result.json()
        lat = json["results"][0]["geometry"]["location"]["lat"]
        lng = json["results"][0]["geometry"]["location"]["lng"]
        output = (lat, lng)
        return output
    else:
        return None

