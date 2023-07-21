# Module description:
# This module is used to read score from the image and save it to a file.
# output: data.txt

import math

debug = 0

dataFolder = ""

image_folder = dataFolder + "images/todo/"
processed_folder = dataFolder + "images/processed/"
error_folder = dataFolder + "images/error/"


# Read score
def read_counters(top_left, bottom_right, text, rect):
    # Initialize temporary list
    tempList = []

    for i in range(len(text)):
        # Check if the text is inside the given rectangle
        if rect[i][0][0] >= top_left[0] and rect[i][0][1] >= top_left[1] and rect[i][1][0] <= bottom_right[0] and \
                rect[i][1][1] <= bottom_right[1]:
            # Assign the text to a temporary variable
            tempValue = text[i]

            # Check if the text is a number
            # If not, try to convert it to a number using the known mistakes
            if not tempValue.isdigit():
                tempValue = tempValue.replace('O', '0')
                tempValue = tempValue.replace('o', '0')
                tempValue = tempValue.replace('C', '0')
                tempValue = tempValue.replace('u', '0')
                tempValue = tempValue.replace('U', '0')
                tempValue = tempValue.replace('D', '0')
                tempValue = tempValue.replace('d', '0')
                tempValue = tempValue.replace('T', '1')
                tempValue = tempValue.replace('z', '2')
                tempValue = tempValue.replace('s', '5')
                tempValue = tempValue.replace('t', '1')
                tempValue = tempValue.replace('I', '1')
                tempValue = tempValue.replace('g', '9')
                tempValue = tempValue.replace('J', '0')
                tempValue = tempValue.replace('"', '1')
                tempValue = tempValue.replace(' ', '')

            # Add the number to the temporary list
            tempList.append(int(tempValue))

            if debug:
                print(text[i] + ' -> ' + tempValue)

    return tempList


# Bandori
def scan_score(imageData):
    # Define lists
    text = list()
    rect = list()
    results = dict()

    fast_slow = False

    # Format data for easier use
    for b in imageData:
        # text = ['text1', 'text2', ...]
        text.append(b[1])

        # rect = [([x1, y1], [x2, y2]), ...]
        templist = ([int(b[0][0][0]), int(b[0][0][1])], [int(b[0][2][0]), int(b[0][2][1])])
        rect.append(templist)

    # Text search
    for i in range(len(text)):
        # "Perfect" boundary
        if text[i].lower() == 'perfect':
            perfect = i

        # Check if Fast/Slow is present
        if text[i].lower() == 'fast':
            fast_slow = True

    # Calculate scale using "Perfect" boundary
    scale = (rect[perfect][1][0] - rect[perfect][0][0]) / 120

    # Main score boundaries
    top_left = [rect[perfect][0][0] + math.floor(145 * scale), rect[perfect][0][1] - math.floor(8 * scale)]
    bottom_right = [top_left[0] + math.floor(140 * scale), top_left[1] + math.floor(190 * scale)]
    # Read score from image data
    tempList = read_counters(top_left, bottom_right, text, rect)

    if debug:
        print(text)
        print('scale: ', scale)
        print('fast_slow: ', fast_slow)
        print(top_left)
        print(bottom_right)

    # Add to results
    results['perfect'] = tempList[0]
    results['great'] = tempList[1]
    results['good'] = tempList[2]
    results['bad'] = tempList[3]
    results['miss'] = tempList[4]

    # Secondary score boundaries
    if fast_slow:
        # Define boundaries of Fast/Slow counters
        top_left = [top_left[0] + math.floor(180 * scale), top_left[1]]
        bottom_right = [top_left[0] + math.floor(120 * scale), top_left[1] + math.floor(74 * scale)]
        # Read score from image data
        tempList = read_counters(top_left, bottom_right, text, rect)

        if debug:
            print(top_left)
            print(bottom_right)

        # Add to results
        results['fast'] = tempList[0]
        results['slow'] = tempList[1]

        # Define boundaries of max combo counter
        top_left = [top_left[0] - math.floor(55 * scale), top_left[1] + math.floor(95 * scale)]
        bottom_right = [top_left[0] + math.floor(140 * scale), top_left[1] + math.floor(60 * scale)]
        # Read score from image data
        tempList = read_counters(top_left, bottom_right, text, rect)

        if debug:
            print(top_left)
            print(bottom_right)

        # Add to results
        results['combo'] = tempList[0]

    # If no fast/slow
    else:
        # Define boundaries of max combo counter
        top_left = [top_left[0] + math.floor(125 * scale), top_left[1] + math.floor(92 * scale)]
        bottom_right = [top_left[0] + math.floor(125 * scale), top_left[1] + math.floor(48 * scale)]
        # Read score from image data
        tempList = read_counters(top_left, bottom_right, text, rect)

        if debug:
            print(top_left)
            print(bottom_right)

        # Add to results
        results['combo'] = tempList[0]

    # Check if first text is a "Challenge Song", if so, skip it
    j = 0
    if text[0].replace(' ', '').lower() in ['challengesong', 'challenge', 'challange', 'challange', 'challangesong',
                                            'challemce']:
        j = 1

    # Remove all spaces from text
    name = text[j].replace(' ', '').lower()

    # Check if name is difficulty
    if name in ['expert', 'hard', 'normal', 'easy', 'special']:
        # If so, set difficulty and get name as next text
        results['difficulty'] = name
        name = text[1 + j]
    else:
        # If not, get difficulty and name as from current text
        name = text[j]
        name = name.split(' ')  # split string into list
        results['difficulty'] = name.pop(0)  # remove first element from list and assign to difficulty
        name = ' '.join(name)  # join list back into string

    # Check if name text is too short, if so, get name from next text
    if len(name) < 3:
        name = text[2 + j]

    for i in [')', "}", "]", '>']:
        results['difficulty'] = results['difficulty'].replace(i, '')

    # # Replace difficulty with corresponding number
    # results['difficulty'] = results['difficulty'].lower()
    # if results['difficulty'] == 'special':
    #     results['difficulty'] = 4
    # elif results['difficulty'] == 'expert':
    #     results['difficulty'] = 3
    # elif results['difficulty'] == 'hard':
    #     results['difficulty'] = 2
    # elif results['difficulty'] == 'normal':
    #     results['difficulty'] = 1
    # elif results['difficulty'] == 'easy':
    #     results['difficulty'] = 0

    results['name'] = name
    results['level'] = results['difficulty']

    return results