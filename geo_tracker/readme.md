This is a utility that takes EXIF data from a photo and returns all the main data in console, 
also asking to open Google Maps page with exact location where this picture was taken, whenever it is possible.
While standard Windows 'properties' option is capable of displaying EXIF data, it displays GPS data in format that is hard to read
and does not show the exact location on the map. This small utility solves the problem.

Installation:

for .py file:
- Python 3.8 and above
- easygui
- exifread

for .exe file:
- no requirements

Usage:

Launch the utility. It will open a file browser, choose a picture. If EXIF data is present, 
it will return it in console. Otherwise, it will return 'No EXIF data found'. If full GPS data is present, the utility will display the prompt:
Would you like to be taken to Google Maps page? [Y/n]. Based on your input, it will either open Google Maps or will take no action. Please, note
that you will need an internet connection for this feature to work. Lastly, Enter key will exit the utility. 

