#!/usr/bin/python
import requests
import json
import sys

artist_name = input("What artis are you searching for?: ")
album_name = input("Which album are you searching for?: ")

#def confirm_choice():
#    print(f"\nYou selected: {data['results'][int(selection)]['artistName']} - {data['results'][int(selection)]['collectionName']}")
#    confirm = input("\n Is this correct (Y/N)? ")
#    return confirm

def get_album_art(album_name, artist_name):
    """
    Fetches album art URL from the iTunes Search API and downloads it.

    Args:
        album_name (str): The name of the album.
        artist_name (str): The name of the artist.

    Returns:
        A jpg file of the desired album art.
    """

    # Take the two input arguments and constructs the request URL
    search_term = f"{album_name} {artist_name}"
    url = f"https://itunes.apple.com/search?term={search_term}&entity=album&limit=100"

    # Collects the jsonb response and stores it in a variable
    response = requests.get(url)
    data = json.loads(response.text)
    
    print(f"\nAlbums matching your search:\n")
    
    # List the album match results returned from the iTunes API, or advise none available and exit:
    if data['resultCount'] > 0:
        i = 0
        while i < data['resultCount']:
            print(f"Result: {str(i)} {data['results'][i]['artistName']} - {data['results'][i]['collectionName']}")
            i += 1
    else:
        print("No results found sorry.")
        exit()

    confirm = ""
    # Function to check for valid results and download the art


    while confirm.lower() != "y":
        # Ask the user to select the appropraite album and check selection is correct
        selection = int(input("\nWhich album to you want to retreive (provide the number): "))
        print(f"\nYou selected: {data['results'][int(selection)]['artistName']} - {data['results'][int(selection)]['collectionName']}")
        confirm = input("\n Is this correct (Y/N)? ")
    else:
        # Retrieve the formatted artist name and album name to create a filename
        real_artist = data['results'][selection]['artistName']
        real_album = data['results'][selection]['collectionName']
        # Retrieve the low resolutaion artwork url
        album_art_url = data['results'][selection]['artworkUrl100']
        # Replace '100x100' with a higher resolution like '2000x2000' will grab higherst available resolution
        high_res_url = album_art_url.replace('100x100', '2000x2000')
        
        # Create a filename using album and artist names, returned from api
        filename = f"{real_artist} - {real_album}.jpg"

        # Request the image from the URL and check for valid response before downloading to file
        image_response = requests.get(high_res_url, stream=True)
        if image_response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in image_response.iter_content(1024):
                    f.write(chunk)
            print("Album art downloaded successfully!")
            print("File name: " + filename)
        else:
            print("Failed to download album art.")
#    else:
#        print("Album not found.")

get_album_art(album_name, artist_name)