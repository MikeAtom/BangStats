import os
import PySimpleGUI as sg
import data._defaults as defaults
from data.scan import create_preview
import data.scripts.db_handler as dbh
import data.scripts.lang_handler as lang

sg.theme('Purple')  # Add a touch of color


def enter_name():
    allSongs = dbh.get_all_songs_names()

    layout = [
        [sg.Text(lang.post__enter_name_listbox)],
        [sg.Input(size=(65, 1), enable_events=True, key='-INPUT-')],
        [sg.Listbox(allSongs, size=(65, 8), enable_events=True, key='-LIST-')],
        [sg.Button(lang.global__apply, enable_events=True, key='Ok', size=(10, 1))]
    ]

    window = sg.Window('Bloody La Vie En Rose! ', layout, size=(480, 240), icon=defaults.icoMashiro)

    while True:
        event, values = window.read()


        if values['-INPUT-'] != '':  # if a keystroke entered in search field
            search = values['-INPUT-']
            new_values = [x for x in allSongs if search.lower() in x.lower()]  # do the filtering
            window['-LIST-'].update(new_values)  # display in the listbox
        else:
            # display original unfiltered list
            window['-LIST-'].update(allSongs)
            # if a list item is chosen

        if event == 'Ok':
            window.close()
            return values["-INPUT-"]

        elif event == '-LIST-' and len(values['-LIST-']):
            window['-INPUT-'].update(values['-LIST-'][0])
            search = values['-LIST-'][0]
            new_values = [x for x in allSongs if search.lower() in x.lower()]  # do the filtering
            window['-LIST-'].update(new_values)  # display in the listbox

        elif event == sg.WIN_CLOSED or event == '-BACK-':
            break


def enter_song_data(imageName):
    global window, event, values

    if event == '-FASTSLOW-':
        if values['-FASTSLOW-']:
            window['-FAST-'].update(disabled=False)
            window['-FAST-'].update('0000')
            window['-SLOW-'].update(disabled=False)
            window['-SLOW-'].update('0000')
        else:
            window['-FAST-'].update(disabled=True)
            window['-FAST-'].update('NONE')
            window['-SLOW-'].update(disabled=True)
            window['-SLOW-'].update('NONE')

    # Set level when song name is entered and difficulty has been selected
    try:
        if event == '-SEARCH-':
            songName = enter_name()
            window['-NAME-'].update(songName)
            if songName != '':
                if values['-DIFF-'] != '':
                    window['-LEVEL-'].update(dbh.find_song(songName, values['-DIFF-'])["level"])

        # Set level when song difficulty is selected and song name has been entered
        if event == '-DIFF-':
            if values['-NAME-'] != '':
                window['-LEVEL-'].update(dbh.find_song(values['-NAME-'], values['-DIFF-'])["level"])
    except:
        pass

    if event == '-DELETE-':
        dbh.delete_from_stored_data(imageName)
        window['-CUR_IMAGE-'].update(lang.post__enter_song_data_deleted_message)
        window['-NEXT-'].update(lang.post__main_action_next)

    if event == '-SAVE-':
        tempSongData = dict()
        try:
            tempSongData['perfect'] = int(values['-PERFECT-'])
            tempSongData['great'] = int(values['-GREAT-'])
            tempSongData['good'] = int(values['-GOOD-'])
            tempSongData['bad'] = int(values['-BAD-'])
            tempSongData['miss'] = int(values['-MISS-'])

            noteSum = tempSongData['perfect'] + tempSongData['great'] + tempSongData['good'] + tempSongData['bad']\
                      + tempSongData['miss']

            if noteSum != dbh.songsData[values['-NAME-']]['noteCount'][values['-DIFF-'].lower()]:
                print(noteSum)
                print(dbh.songsData[values['-NAME-']]['noteCount'][values['-DIFF-'].lower()])
                raise Exception

            if values['-FASTSLOW-']:
                tempSongData['fast'] = int(values['-FAST-'])
                tempSongData['slow'] = int(values['-SLOW-'])

                _check = 1 / bool(tempSongData['fast'] + tempSongData['slow'] ==
                                  tempSongData['great'] + tempSongData['good'] + tempSongData['bad'])

            tempSongData['combo'] = int(values['-COMBO-'])
            tempSongData['difficulty'] = values['-DIFF-'].lower()
            tempSongData['name'] = values['-NAME-']
            tempSongData['level'] = int(values['-LEVEL-'])

            # Add date and time to dict
            tempSongData['timestamp'] = dbh.get_time_date(imageName)

            _check = 1 / len(tempSongData['name']) + 1 / len(tempSongData['difficulty']) + 1 / tempSongData['combo']

            print("Saving data for " + imageName)

            dbh.write_stored_data({imageName: tempSongData})
            window['-CUR_IMAGE-'].update(lang.post__enter_song_data_saved_message)

            window['-NEXT-'].update(lang.post__main_action_next)
            check_inconsistencies()

            return 0
        except:
            sg.Window('Fuee...', [[sg.Text(
                lang.post__enter_song_data_invalid_message)],
                [sg.Push(), sg.OK(s=10), sg.Push()]], disable_close=True, icon=defaults.icoKanon).read(close=True)


def update_song_data(songData):
    window['-NAME-'].update(songData['name'])
    window['-LEVEL-'].update(songData['level'])
    window['-DIFF-'].update(songData['difficulty'].upper())
    window['-COMBO-'].update(songData['combo'])
    window['-PERFECT-'].update(songData['perfect'])
    window['-GREAT-'].update(songData['great'])
    window['-GOOD-'].update(songData['good'])
    window['-BAD-'].update(songData['bad'])
    window['-MISS-'].update(songData['miss'])
    if 'fast' in songData.keys():
        window['-FASTSLOW-'].update(True)
        window['-FAST-'].update(songData['fast'])
        window['-SLOW-'].update(songData['slow'])
    else:
        window['-FASTSLOW-'].update(False)
        window['-FAST-'].update('NONE')
        window['-SLOW-'].update('NONE')


def abort():
    global window, imagesErrors

    window['-PREVIEW-'].update(filename=defaults.imagePreview)
    window['-CUR_IMAGE-'].update('┐(￣ヘ￣;)┌')

    for key in ['-NAME-', '-SEARCH-',
                '-LEVEL-', '-DIFF-', '-FASTSLOW-', '-COMBO-',
                '-PERFECT-', '-GREAT-', '-GOOD-', '-BAD-', '-MISS-', '-FAST-', '-SLOW-']:
        window[key].update(disabled=True)
    window['-NAME-'].update('')
    window['-LEVEL-'].update('')
    window['-DIFF-'].update('')
    window['-COMBO-'].update('0000')
    window['-PERFECT-'].update('0000')
    window['-GREAT-'].update('0000')
    window['-GOOD-'].update('0000')
    window['-BAD-'].update('0000')
    window['-MISS-'].update('0000')
    window['-FAST-'].update('NONE')
    window['-SLOW-'].update('NONE')
    window['-FASTSLOW-'].update(False)

    window['-START-'].update(disabled=False)
    window['-FIX_ERRORS-'].update(disabled=True if len(imagesErrors) == 0 else False)
    window['-FIX_UNKNOWN-'].update(disabled=False)
    window['-FIX_NOTES-'].update(disabled=False)
    window['-FIX_FAST-'].update(disabled=False)


def check_inconsistencies():
    global window, imagesStored, imagesUnknown, imagesNotSum, imagesWrongFastSlow, imagesErrors, imagesScanned

    imagesErrors = dbh.read_temp_errors()

    imagesUnknown = []
    imagesNotSum = []
    imagesWrongFastSlow = []

    if len(dbh.storedData) != 0:
        for image in dbh.storedData.keys():
            try:
                if dbh.storedData[image]['name'] == 'Unknown' or dbh.storedData[image]['difficulty'] == 'Unknown':
                    imagesUnknown.append(image)

                if dbh.storedData[image]['name'] == '' or dbh.storedData[image]['difficulty'] == '':
                    imagesUnknown.append(image)

                noteSum = dbh.storedData[image]['perfect'] + dbh.storedData[image]['great'] \
                          + dbh.storedData[image]['good'] \
                          + dbh.storedData[image]['bad'] + dbh.storedData[image]['miss']

                if noteSum != dbh.songsData[dbh.storedData[image]['name']]['noteCount'][
                    dbh.storedData[image]['difficulty']]:
                    imagesNotSum.append(image)

                fastSlowSum = dbh.storedData[image]['fast'] + dbh.storedData[image]['slow']
                notPerfectNotes = dbh.storedData[image]['great'] + dbh.storedData[image]['good'] + \
                                  dbh.storedData[image]['bad']

                if fastSlowSum != notPerfectNotes:
                    imagesWrongFastSlow.append(image)
            except:
                pass

    window['-ERRORS_COUNT-'].update(len(imagesErrors))
    window['-UNKNOWN_COUNT-'].update(len(imagesUnknown))
    window['-NOTES_COUNT-'].update(len(imagesNotSum))
    window['-FASTSLOW_COUNT-'].update(len(imagesWrongFastSlow))

    window['-FIX_FAST-'].update(disabled=True if len(imagesWrongFastSlow) == 0 else False)
    window['-FIX_NOTES-'].update(disabled=True if len(imagesNotSum) == 0 else False)
    window['-FIX_UNKNOWN-'].update(disabled=True if len(imagesUnknown) == 0 else False)
    window['-FIX_ERRORS-'].update(disabled=True if len(imagesErrors) == 0 else False)

    if len(imagesWrongFastSlow) + len(imagesNotSum) + len(imagesUnknown) + len(imagesErrors) == 0\
            and len(imagesScanned) == 0:
        window['-START-'].update(disabled=True)

        sg.Window('You did it~', [[sg.Text(
            lang.post__check_inconsistencies_no_inconsistencies
        )],
            [sg.Push(), sg.OK(s=10), sg.Push()]], disable_close=True, icon=defaults.icoMoca
                  ).read(close=True)


def main(_imagesStored, _imagesScanned, _imagesErrors, imagesFolderPath):
    global window, imagesErrors, imagesStored, event, values, imagesScanned

    imagesScanned = _imagesScanned
    imagesErrors = _imagesErrors
    imagesStored = _imagesStored
    songDataLayout = [
        [sg.Text(lang.post__main_songdata_name), sg.InputText('', size=25, key='-NAME-', justification='left', readonly=True, disabled=True,
                                        tooltip=lang.post__main_songdata_name_tooltip),
         sg.Button(lang.post__main_songdata_search, enable_events=True, key='-SEARCH-', size=(6, 1), disabled=True,
                   tooltip=lang.post__main_songdata_search_tooltip),
         sg.Text(lang.post__main_songdata_difficulty),
         sg.Combo(['EASY', 'NORMAL', 'HARD', 'EXPERT', 'SPECIAL'], size=(7, 1), readonly=True, key='-DIFF-',
                  disabled=True, enable_events=True,
                  tooltip=lang.post__main_songdata_difficulty_tooltip),
         sg.Text(lang.post__main_songdata_level),
         sg.InputText(0, size=3, justification='center', readonly=True, key='-LEVEL-', disabled=True,
                      tooltip=lang.post__main_songdata_level_tooltip)],
        [sg.Text("Perfect:"), sg.InputText('0000', size=7, justification='center', key='-PERFECT-', disabled=True),
         sg.Text("Great:"), sg.InputText('0000', size=7, justification='center', key='-GREAT-', disabled=True),
         sg.Text("Good:"), sg.InputText('0000', size=7, justification='center', key='-GOOD-', disabled=True),
         sg.Text("Bad:"), sg.InputText('0000', size=7, justification='center', key='-BAD-', disabled=True),
         sg.Text("Miss:"), sg.InputText('0000', size=7, justification='center', key='-MISS-', disabled=True)],
        [
            sg.Text("Fast:"), sg.InputText('NONE', size=7, justification='center', key='-FAST-', disabled=True),
            sg.Text("Slow:"), sg.InputText('NONE', size=7, justification='center', key='-SLOW-', disabled=True),
            sg.Text("Max Combo:"),
            sg.InputText('0000', size=7, justification='center', key='-COMBO-', disabled=True),
            sg.Checkbox('Fast/Slow', key='-FASTSLOW-', enable_events=True, disabled=True)
        ]
    ]
    actionLayout = [
        [sg.Button(lang.post__main_action_start, enable_events=True, key='-START-', size=(10, 1),
                   disabled=True if len(imagesScanned) != 0 else False,
                   tooltip=lang.post__main_action_start_tooltip
                   )],
        [sg.Button(lang.post__main_action_save, enable_events=True, key='-SAVE-', size=(10, 1),
                   tooltip=lang.post__main_action_save_tooltip)],
        [sg.Button(lang.post__main_action_skip, enable_events=True, key='-NEXT-', size=(10, 1),
                   tooltip=lang.post__main_action_skip_tooltip)],
        [sg.Button(lang.post__main_action_reset, enable_events=True, key='-RESET-', size=(10, 1),
                   tooltip=lang.post__main_action_reset_tooltip)],
        [sg.Button(lang.post__main_action_delete, enable_events=True, key='-DELETE-', size=(10, 1),
                   tooltip=lang.post__main_action_delete_tooltip)],
        [sg.Button(lang.post__main_action_abort, enable_events=True, key='-ABORT-', size=(10, 1),
                   tooltip=lang.post__main_action_abort_tooltip)],

    ]
    fixTypeLayout = [
        [
            sg.Column([
                [sg.Radio(lang.post__main_fix_scan_errors, "fixType", default=True, key='-FIX_ERRORS-', disabled=True,
                          tooltip=lang.post__main_fix_scan_errors_tooltip)],
                [sg.Text("0", key='-ERRORS_COUNT-', size=(10, 1), justification='center')]
            ]),
            sg.Column([
                [sg.Radio(lang.post__main_fix_unknown_songs, "fixType", default=False, key='-FIX_UNKNOWN-',
                          tooltip=lang.post__main_fix_unknown_songs_tooltip)],
                [sg.Text("0", key='-UNKNOWN_COUNT-', size=(10, 1), justification='center')]
            ]),
            sg.Column([
                [sg.Radio(lang.post__main_fix_notes_missmatch, "fixType", default=False, key='-FIX_NOTES-',
                          tooltip=lang.post__main_fix_notes_missmatch_tooltip)],
                [sg.Text("0", key='-NOTES_COUNT-', size=(10, 1), justification='center')]
            ]),
            sg.Column([
                [sg.Radio("Fast/Slow", "fixType", default=False, key='-FIX_FAST-', tooltip=
                lang.post__main_fix_fastslow_tooltip)],
                [sg.Text("0", key='-FASTSLOW_COUNT-', size=(10, 1), justification='center')]
            ])
        ]
    ]
    dataLayout = [
        [sg.Button(lang.post__main_data_store_scanned, enable_events=True, key='-STORE-', size=(15, 1),
                   disabled=True if len(imagesScanned) == 0 else False,
                   tooltip=lang.post__main_data_store_scanned_tooltip
                   ),
         sg.Text(f"{lang.post__main_data_stored} {len(imagesStored)}", key='-STORED-',
                 tooltip=lang.post__main_data_stored_tooltip
                 ),
         sg.Text(f"{lang.post__main_data_scanned} {len(imagesScanned)}", key='-SCANNED-',
                 tooltip=lang.post__main_data_scanned_tooltip
                 )
         ]
    ]
    guideLayout = [
        [sg.Text(lang.post__main_guide_first)],
        [sg.Text(lang.post__main_guide_second)],
        [sg.Text(lang.post__main_guide_third)],
        [sg.Text(lang.post__main_guide_fourth)],
        [sg.Text(lang.post__main_guide_filth)]
    ]

    col1 = sg.Column([
        [sg.Frame(lang.post__main_layout_fix_type, fixTypeLayout, font=("", 12), size=(580, 90))],
        [sg.Frame(lang.post__main_layout_song_data, songDataLayout, font=("", 12), size=(580, 150))]
    ])
    col2 = sg.Column([
        [sg.Frame(lang.post__main_layout_actions, actionLayout, font=("", 12), size=(98, 216)),
         sg.Frame(lang.post__main_layout_how_to, guideLayout, font=("", 12), size=(560, 216))]
    ])

    layout = [
        [sg.Text(lang.post__main_layout_title, font=("", 16)), sg.Push(), sg.Button(lang.global__button_back, key="-BACK-", size=(5, 1))],
        [sg.HSeparator()],
        [dataLayout],
        [sg.Push(), sg.Image(filename=defaults.imagePreview, size=(640, 360), key="-PREVIEW-"), sg.Push()],
        [sg.Push(), sg.Text("┐(￣ヘ￣;)┌", key='-CUR_IMAGE-'), sg.Push()],
        [sg.HSeparator()],
        [col1, col2]
    ]

    window = sg.Window(f"BanG Stats! // {lang.post__main_layout_title}", layout, size=(1080, 720), icon=defaults.icoKasumi,
                       finalize=True)

    check_inconsistencies()

    while True:
        event, values = window.read()

        if event == '-STORE-':
            print("Storing scanned data")
            dbh.store_scanned(imagesScanned)
            window['-STORED-'].update(f"{lang.post__main_data_stored}: {str(len(imagesScanned) + len(imagesStored))}")
            window['-STORE-'].update(disabled=True)
            window['-SCANNED-'].update(f"{lang.post__main_data_scanned}: 0")
            window['-START-'].update(disabled=False)

            check_inconsistencies()

        elif event == '-START-':
            window['-START-'].update("In progress", disabled=True)
            window['-FIX_ERRORS-'].update(disabled=True)
            window['-FIX_UNKNOWN-'].update(disabled=True)
            window['-FIX_NOTES-'].update(disabled=True)
            window['-FIX_FAST-'].update(disabled=True)

            for key in ['-NAME-', '-SEARCH-',
                        '-LEVEL-', '-DIFF-', '-FASTSLOW-', '-COMBO-',
                        '-PERFECT-', '-GREAT-', '-GOOD-', '-BAD-', '-MISS-', '-FAST-', '-SLOW-']:
                window[key].update(disabled=False)

            fixList = []
            if values['-FIX_ERRORS-'] and len(imagesErrors) != 0:
                fixList = imagesErrors
                window['-DELETE-'].update(disabled=True)
            elif values['-FIX_UNKNOWN-']:
                fixList = imagesUnknown
            elif values['-FIX_NOTES-']:
                fixList = imagesNotSum
            elif values['-FIX_FAST-']:
                fixList = imagesWrongFastSlow

            for imageFix in fixList:
                window['-NEXT-'].update(lang.post__main_action_skip)
                imagePath = os.path.join(imagesFolderPath, imageFix)

                print("Fixing errors in " + imagePath)
                window['-PREVIEW-'].update(filename=create_preview(imagePath, 360))
                window['-CUR_IMAGE-'].update(imagePath.replace("/", "\\"))

                try:
                    storedImageData = dbh.get_stored_image_data(imageFix)

                    if not storedImageData['difficulty'] in ['easy', 'normal', 'hard', 'expert', 'special']:
                        storedImageData['difficulty'] = ''

                    elif not storedImageData['name'] in dbh.get_all_songs_names():
                        storedImageData['name'] = ''

                except:
                    storedImageData = {'name': '', 'level': 0, 'difficulty': '', 'combo': '0000', 'perfect': '0000',
                                       'great': '0000', 'good': '0000', 'bad': '0000', 'miss': '0000'}

                update_song_data(storedImageData)

                while event != '-NEXT-':
                    enter_song_data(imageFix)

                    event, values = window.read()

                    if event == '-ABORT-':
                        break

                    elif event == sg.WIN_CLOSED or event == '-BACK-':
                        break

                if event == '-ABORT-':
                    break

                event = None

            if not event == '-ABORT-':
                sg.Window('Nice Fever!', [[sg.Text(
                    lang.post__all_type_fixed_window_text
                )], [sg.Push(), sg.OK(s=10), sg.Push()]], icon=defaults.icoAya).read(close=True)

                if values['-FIX_ERRORS-']:
                    try:
                        dbh.move_temp_error()
                    except:
                        pass

            window['-START-'].update(lang.post__main_action_start, disabled=False)
            window['-DELETE-'].update(disabled=False)

            event = "Fix ended"
            abort()

        elif event == sg.WIN_CLOSED or event == '-BACK-':
            break

    window.close()
