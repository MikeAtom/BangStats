from difflib import SequenceMatcher
import json
import os
import ast
import time
import data._defaults as defaults

songsData = dict()
storedData = dict()
dataPath = ""

# Check if backup folder exists, if not, create it
if not os.path.exists(defaults.dbPath + 'backup'):
    os.makedirs(defaults.dbPath + 'backup')

# Initialize songs database and get information about songs and stored images
# Returns amount of songs and stored images
def data_init(_dataPath):
    # Declare global variables
    global songsData, dataPath, storedData

    # Set data path to global variable
    dataPath = _dataPath

    # Load songs data
    try:
        f = open(defaults.songsJson, 'r', encoding='utf-8')
        songsData = json.loads(f.read())
    except:
        print("Songs file not found in " + defaults.songsJson)

    # Read stored data
    read_stored_data()

    print("Songs loaded: " + str(len(songsData)))
    print("Images stored: " + str(len(storedData)))

    return str(len(songsData)), storedData


# Get unix timestamp from image name
# Returns unix timestamp
def get_time_date(imageName):
    # Replace '-' with '_' in image name to make all screenshots the same
    # some old android versions use '-' instead of '_' in screenshot names
    # Screenshot_20230715_190827_BanG Dream!.png

    # Try extracting time from image name
    try:
        imageName = imageName.replace('-', '_')
        imageName = imageName.split('_')[1] + '_' + imageName.split('_')[2]
        # Convert to unix timestamp
        fileTime = time.mktime(time.strptime(imageName, "%Y%m%d_%H%M%S"))
    # If it fails, get time from file creation time
    except:
        # Get file creation time
        fileTime = os.path.getctime(defaults.imagesPath + imageName)

    return round(fileTime)


# Calculate similarity between two strings
# Returns similarity ratio
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# Approximate song name and return song data
# Returns song data
def aprox_song(name, difficulty):
    global songsData

    # Initialize variables
    maxSimilarity = 0
    results = dict()

    # For each song name in songs database
    for song in songsData:
        # If song name is the same as name, return song data
        if name == song:
            results["name"] = song
            results["level"] = songsData[song]['levels'][difficulty]
            return results
        else:
            # Calculate similarity
            similarity = similar(name, song)

            # If similarity is higher than previous, replace it
            if similarity > maxSimilarity:
                # Set new max similarity
                maxSimilarity = similarity
                try:
                    results["name"] = song
                    results["level"] = songsData[song]['levels'][difficulty]
                except:
                    results["name"] = 'Unknown'
                    results["level"] = 0

    return results


# Find song in song database
# Returns song data
def find_song(name, difficulty="none"):
    global songsData

    # Initialize variables
    difficulty = difficulty.lower()
    results = dict()

    # Get song data from database
    results["name"] = songsData[name]
    results["artist"] = songsData[name]['artist']
    if difficulty != "none":
        results["level"] = songsData[name]['levels'][difficulty]
        results["notes"] = songsData[name]['noteCount'][difficulty]
    results["bpm"] = songsData[name]['bpm']
    results["time"] = songsData[name]['time']

    return results

# Get all songs names
# Returns list of songs names
def get_all_songs_names():
    global songsData

    # Initialize variables
    names = []

    # For each song name in songs database
    for name in songsData.keys():
        # Add song name to list
        names.append(name)

    return names

# Get all screenshots names
# Returns list of screenshots names
def get_screenshots_names():
    global screenshotsData

    # Initialize variables
    names = []

    # For each screenshot name in screenshots database
    for name in screenshotsData.keys():
        # Add screenshot name to list
        names.append(name)

    return names


# Save session data
def save_session(dataJson, imagesFolderPath, language):
    with open(defaults.sessionJson, 'w', encoding='utf8') as f:
        json.dump({
            "dataPath": dataJson,
            "imagesFolderPath": imagesFolderPath,
            "language": language
        }, f, ensure_ascii=False, indent=4)


# Read session data
def read_session():
    sessionData = dict()

    if os.path.isfile(defaults.sessionJson):
        with open(defaults.sessionJson, 'r', encoding='utf8') as f:
            sessionData = json.load(f)

    return sessionData


# Write scanned data to temporary file
def write_temp_data(data):
    with open(defaults.tempDataFile, 'a', encoding='UTF-8') as file:
        file.write(str(data) + '\n')


# Write error data to temporary file
def write_temp_error(data):
    with open(defaults.tempErrorFile, 'a', encoding='UTF-8') as file:
        file.write(str(data) + '\n')


# Read temporary data
def read_temp_data():
    imagesScanned = []

    if os.path.isfile(defaults.tempDataFile):
        with open(defaults.tempDataFile, 'r', encoding='utf8') as f:
            imagesScanned = f.read().splitlines()

    return imagesScanned


# Read temp file with errors
def read_temp_errors():
    imagesErrors = []

    if os.path.isfile(defaults.tempErrorFile):
        with open(defaults.tempErrorFile, 'r', encoding='utf8') as f:
            imagesErrors = f.read().splitlines()

    return imagesErrors

# Move temp data to backup folder
def move_temp_error():
    os.rename(defaults.tempErrorFile, defaults.dbPath + 'backup/' + str(int(time.time())) + '_errors.backup')


def store_scanned(scannedData):
    global storedData, dataPath

    data = dict()

    # Format data
    for line in scannedData:
        # Convert string to dict
        tempDict = ast.literal_eval(line)

        tempDict['difficulty'] = tempDict['difficulty'].lower()

        # Get song name and chart level from db
        nameAndLevel = aprox_song(tempDict['name'], tempDict['difficulty'])
        # Add song name and level to dict from db
        tempDict['name'] = nameAndLevel['name']
        tempDict['level'] = nameAndLevel['level']

        # Assign image name as key before removing it
        key = tempDict['image']
        # Add unix time to dict
        tempDict['timestamp'] = get_time_date(key)
        # remove the image key
        tempDict.pop('image')
        # Add to the permanent dict
        data[key] = tempDict

    # Write data to file
    write_stored_data(data)

    # Backup temp data
    os.rename(defaults.tempDataFile, defaults.dbPath + 'backup/' + str(int(time.time())) + '_scanned.backup')

    print('Data processed and saved as ' + dataPath + '; ' + str(len(data)) + ' entries')


# Read stored data
# Returns stored data
def read_stored_data():
    global dataPath, storedData

    storedData = dict()

    # Load data
    try:
        f = open(dataPath, 'r', encoding='utf-8')
        storedData = json.loads(f.read())
    except:
        print("Data not found in " + dataPath)

    return storedData


def write_stored_data(data):
    global storedData, dataPath

    # Combine data from temp file and data file
    data = {**storedData, **data}

    # Update stored data
    storedData = data

    # Write data to file
    with open(dataPath, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def delete_from_stored_data(imageName):
    global storedData

    # Remove data from stored data
    storedData.pop(imageName)

    # Write data to file
    with open(dataPath, 'w', encoding='utf8') as f:
        json.dump(storedData, f, ensure_ascii=False, indent=4)


def get_stored_image_data(imageName):
    global storedData

    # Get data from stored data
    data = storedData[imageName]

    return data

def format_data(timeTrim=0):
    formattedData = dict()

    for key in storedData.keys():
        # Get data from storedData using screenshot name as key
        liveScreenshot = storedData[key]
        # Check if screenshot is from selected time period
        if liveScreenshot['timestamp'] > timeTrim:
            # Create temporary formatted dictionary for storing data
            tempDict = {'easy': {'count': 0, 'fc': 0, 'ap': 0, 'combo': 0, 'perfect': 0, 'great': 0, 'good': 0,
                                 'bad': 0, 'miss': 0, 'fast': 0, 'slow': 0, "accuracy": []},
                        'normal': {'count': 0, 'fc': 0, 'ap': 0, 'combo': 0, 'perfect': 0, 'great': 0, 'good': 0,
                                   'bad': 0, 'miss': 0, 'fast': 0, 'slow': 0, "accuracy": []},
                        'hard': {'count': 0, 'fc': 0, 'ap': 0, 'combo': 0, 'perfect': 0, 'great': 0, 'good': 0,
                                 'bad': 0, 'miss': 0, 'fast': 0, 'slow': 0, "accuracy": []},
                        'expert': {'count': 0, 'fc': 0, 'ap': 0, 'combo': 0, 'perfect': 0, 'great': 0, 'good': 0,
                                   'bad': 0, 'miss': 0, 'fast': 0, 'slow': 0, "accuracy": []},
                        'special': {'count': 0, 'fc': 0, 'ap': 0, 'combo': 0, 'perfect': 0, 'great': 0, 'good': 0,
                                    'bad': 0, 'miss': 0, 'fast': 0, 'slow': 0, "accuracy": []},
                        }
            # Add +1 to count for current difficulty
            tempDict[liveScreenshot['difficulty']]['count'] += 1
            # If live is Full Combo, add +1 to FC count
            if liveScreenshot['good'] + liveScreenshot['bad'] + liveScreenshot['miss'] == 0\
                    and liveScreenshot['great'] != 0:
                tempDict[liveScreenshot['difficulty']]['fc'] += 1
            # If live is All Perfect, add +1 to AP count
            if liveScreenshot['great'] + liveScreenshot['good'] + liveScreenshot['bad'] + liveScreenshot['miss'] == 0:
                tempDict[liveScreenshot['difficulty']]['ap'] += 1

            # Add combo, notes and accuracy to current difficulty
            tempDict[liveScreenshot['difficulty']]['perfect'] += liveScreenshot['perfect']
            tempDict[liveScreenshot['difficulty']]['great'] += liveScreenshot['great']
            tempDict[liveScreenshot['difficulty']]['good'] += liveScreenshot['good']
            tempDict[liveScreenshot['difficulty']]['bad'] += liveScreenshot['bad']
            tempDict[liveScreenshot['difficulty']]['miss'] += liveScreenshot['miss']

            if 'fast' in liveScreenshot.keys():
                tempDict[liveScreenshot['difficulty']]['fast'] += liveScreenshot['fast']
                tempDict[liveScreenshot['difficulty']]['slow'] += liveScreenshot['slow']

            tempDict[liveScreenshot['difficulty']]['combo'] += liveScreenshot['combo']

            # Get total notes in song from DB
            songNotes = songsData[liveScreenshot['name']]['noteCount'][liveScreenshot['difficulty']]
            tempDict[liveScreenshot['difficulty']]['accuracy'].append((liveScreenshot['perfect'] / songNotes) * 100)

            # If it's first time we see this song, add it to topSongs
            if not liveScreenshot['name'] in formattedData:
                formattedData[liveScreenshot['name']] = tempDict
            else:
                # If song is already in topSongs, add data from current live to existing data
                for diff in ['easy', 'normal', 'hard', 'expert', 'special']:
                    for key in tempDict[diff].keys():
                            formattedData[liveScreenshot['name']][diff][key] += tempDict[diff][key]

    # write topSongs to file
    if timeTrim == 0:
        timeTrim = "AllTime"
    else:
        timeTrim = "TimeTrim"

    dataFileName = dataPath.split('/')[-1].split('.')[0]

    # File name is formatted_<timeTrim>_.bangstats
    fileName = defaults.dbPath + f"{dataFileName}-formatted_{timeTrim}.json"
    # Write formatted data to file
    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(formattedData, f, indent=4)

    return formattedData