#!/usr/bin/python
import requests
import json
import sys
import re


confirmation = None
data = None

def user_search_query():
    artist_name = input("What artist are you searching for?: ")
    album_name = input("Which album are you searching for (leave blank to get all results?: ")
    return artist_name, album_name

def itunes_api_call(artist_name, album_name):
    # Take the two input arguments and constructs the request URL
    search_term = f"{artist_name} {album_name}"
    url = f"https://itunes.apple.com/search?term={search_term}&entity=album&limit=50"
    response = requests.get(url)
    return json.loads(response.text)

def graceful_exit():
    print("Good bye!")
    exit()

def get_album_art(artist_name, album_name):
    global confirmation, data

    data = itunes_api_call(artist_name, album_name)

    # List the album results returned from the iTunes API, if none ask if you want to try another search:
    while data['resultCount'] == 0:
        #try_again = input("No results found sorry. Do you wnat to try another search (Y/N)?")
        #if try_again.lower() == 'y':
        if input("No results found sorry. Do you wnat to try another search (Y/N)?") in ("y","Y"):
            user_input = user_search_query()
            data = itunes_api_call(user_input[0], user_input[1])
        else:
            print("Good bye.")
            exit()
    else:
        print(f"\nAlbums matching your search:\n")
        i = 0
        while i < data['resultCount']:
            print(f"{str(i)} {data['results'][i]['artistName']} - {data['results'][i]['collectionName']}")
            i += 1

    # Getting the album art
    while confirmation not in ("y", "Y"):
        # Ask the user to select the appropraite albums and checks selection is correct
        user_album_selection = input("\nWhich album(s) to you want to retreive (provide a comma seperated list of number(s): ")
        selection = user_album_selection.split(',')
        print("\nPlease confirm these are the album covers you want to download:")
        for number in selection:
            release_year = re.search('[0-9]{4}', data['results'][int(number)]['releaseDate']).group(0)
            print(f"{number} - {data['results'][int(number)]['artistName']} - {data['results'][int(number)]['collectionName']} - ({release_year})")
        confirmation = input("\nIs this correct (Y/N)? ")
    else:
        # Loops through the list of selected albums and downloads the artwork
        for number in selection:
            # Retrieve the formatted artist name and album name to create a filename (replacing any '/' thanks AC/DC)
            real_artist = re.sub('[/]', '-', data['results'][int(number)]['artistName'])
            real_album = re.sub('[/]', '-', data['results'][int(number)]['collectionName'])
            release_year = re.search('[0-9]{4}', data['results'][int(number)]['releaseDate']).group(0)
            # Retrieve the low resolutaion artwork url
            album_art_url = data['results'][int(number)]['artworkUrl100']
            # Replace '100x100' with a higher resolution like '2000x2000' will grab higherst available resolution
            high_res_url = album_art_url.replace('100x100', '2000x2000')
            # Create a filename using album and artist names, returned from api
            filename = f"{release_year} - {real_artist} - {real_album}.jpg"
            # Request the image from the URL and check for valid response before downloading to file
            image_response = requests.get(high_res_url, stream=True)
            if image_response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in image_response.iter_content(1024):
                        f.write(chunk)
                print(f"\nAlbum art {number} downloaded successfully!")
                print(f"File name: {filename}")
            else:
                print(f"Failed to download artwork {number} please try again.")


user_input = user_search_query()
print(user_input)
get_album_art(user_input[0], user_input[1])