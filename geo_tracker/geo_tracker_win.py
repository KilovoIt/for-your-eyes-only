import sys, webbrowser, exifread, os, easygui

# it's known that Windows (as many other OS) allows you to see EXIF data
# that is written at the moment of picture creation or artificially
# changed later. However, many OS do not have the convenience of showing
# user the exact spot on the map where the picture was taken.

# this is a small script that does it for you. 

#
# Description of all necessary functions:
#
def framing(func):
    """a framing function

    embraces output into ***
    lines for a better readability
    """
    def wrapper(*args, **kwargs):
        print(48 * '*')
        func(*args, **kwargs)
        print(48 * '*')

    return wrapper


@framing
def printOutput(text):
    if isinstance(text, str):
        print(text)
    elif isinstance(text, list):
        for item in text:
            print(item)


def coordinatesPrint(tags):
    """
    Function reformats GPS data to a 
    DEG° MIN' SEC\" format
    """
    assert isinstance(tags, dict)
    assert all([
        isinstance(tags[x], exifread.classes.IfdTag)
        for x in ['GPS GPSLatitude', 'GPS GPSLongitude']
    ]) == True
    try:
        print_lat = str(tags['GPS GPSLatitude'].values[0]) + '° ' + str(
            tags['GPS GPSLatitude'].values[1]) + "' " + str(
                tags['GPS GPSLatitude'].values[2]) + '"' + str(
                    tags['GPS GPSLatitudeRef'].values)
        print_lon = str(tags['GPS GPSLongitude'].values[0]) + '° ' + str(
            tags['GPS GPSLongitude'].values[1]) + "' " + str(
                tags['GPS GPSLongitude'].values[2]) + '"' + str(
                    tags['GPS GPSLongitudeRef'].values)
        return (print_lat, print_lon)
    except KeyError:
        print_lat = str(tags['GPS GPSLatitude'].values[0]) + '° ' + str(
            tags['GPS GPSLatitude'].values[1]) + "' " + str(
                tags['GPS GPSLatitude'].values[2]) + '"'
        print_lon = str(tags['GPS GPSLongitude'].values[0]) + '° ' + str(
            tags['GPS GPSLongitude'].values[1]) + "' " + str(
                tags['GPS GPSLongitude'].values[2]) + '"'
        return (print_lat, print_lon)


def coordinatesReformatting(tags):
    """
    Takes standard tags from exifread
    and returns back a tuple of Latitude and Longitude 
    in float format with consideration of the hemisphere, 
    ('Latitude, Longitude')
    """
    #asserting if tags is the object that can be processed
    assert isinstance(tags, dict)
    assert all([
        isinstance(tags[x], exifread.classes.IfdTag) for x in [
            'GPS GPSLatitude', 'GPS GPSLongitude', 'GPS GPSLatitudeRef',
            'GPS GPSLongitudeRef'
        ]
    ]) == True

    string_lat = float(tags['GPS GPSLatitude'].values[0]) + float(
        tags['GPS GPSLatitude'].values[1]) / 60 + float(
            tags['GPS GPSLatitude'].values[2]) / 3600
    string_lon = float(tags['GPS GPSLongitude'].values[0]) + float(
        tags['GPS GPSLongitude'].values[1]) / 60 + float(
            tags['GPS GPSLongitude'].values[2]) / 3600

    hemi_lat = tags['GPS GPSLatitudeRef']
    hemi_lon = tags['GPS GPSLongitudeRef']

    if str(hemi_lat.values) == "S":
        string_lat *= (-1)
    if str(hemi_lon.values) == 'W':
        string_lon *= (-1)

    return (f'{string_lat:.7f}', f'{string_lon:.7f}')

#
# EXECUTABLE SECTION
#

file = open(easygui.fileopenbox(), 'r')
path = file.name

assert os.path.exists(path), "This file doesn't exists"
#Reading the file
f = open(path, 'rb')
gps_avail = False

# Return Exif tags
tags = exifread.process_file(f)
data_of_interest = {
    'Date': 'Image DateTime',
    'Make': 'Image Make',
    'Model': 'Image Model'
}

if not tags.values():  # Case when there is no EXIF data is present
    printOutput("No EXIF data detected")

else:  # Checking how many metadata parameters are available
    output = []
    for param in set(tags.keys()) & set(data_of_interest.values()):
        output.append(
            str(
                list(data_of_interest.keys())[list(
                    data_of_interest.values()).index(param)]) + ': ' +
            str(tags[param]))

    #Dealing with geodata format
    try:
        if all([
                tags[tag] for tag in [
                    'GPS GPSLatitude', 'GPS GPSLongitude',
                    'GPS GPSLatitudeRef', 'GPS GPSLongitudeRef'
                ]
        ]) == True:
            gps_avail = True
            Lat_print, Lon_print = coordinatesPrint(tags)
            output.extend([
                'Latitude:  ' + str(Lat_print), 'Longitude:  ' + str(Lon_print)
            ])

        elif all([
                tags[tag] for tag in ['GPS GPSLatitude', 'GPS GPSLongitude']
        ]) == True:
            print('Part of GPS data is missing, map reference is unavailable')
            Lat_print, Lon_print = coordinatesPrint(tags)
            output.extend([
                'Latitude:  ' + str(Lat_print), 'Longitude:  ' + str(Lon_print)
            ])
    except KeyError:
        print('GPS data is corrupted or stripped')

    output.sort()
    printOutput([x for x in output])  #print result

    if gps_avail:
        place_string = coordinatesReformatting(tags)
        value = input("Show the place it was taken on Google Maps? [Y/N]\n")
        if value == 'Y' or value == 'y':
            webbrowser.open('https://www.google.com/maps/place/' +
                            place_string[0] + ' ' + place_string[1])

# waiting for the Enter key pressed to quit
input("Press Enter key to exit") 
