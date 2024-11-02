## A simple python script to retreive album art from iTunes

I have been building up my CD collection again and ripping them straight to FLAC. But I do not have a scanner to scan in the album art to add to the metadata and searching the web was slow and generally hard to find good quality images.

So I discovered iTunes had an API where you just grab alabum art from. This led to this little script.

**Usage**

Download script and make execuable:
`./getart.py`

Or if you are on a system without Python in /usr/bin:
`python get_album_art.py`

The script does the rest asking for artist, album, and allowing you to choose from a list of results.