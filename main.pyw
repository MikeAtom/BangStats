import os, sys, locale
import PySimpleGUI as sg
import data._defaults as defaults
import data.scripts.db_handler as dbh
import data.scripts.lang_handler as lang

def load_data():
    layout = [
        [sg.Push(), sg.Text(lang.main_load_data__welcome, font=("", 15)), sg.Push()],
        [sg.Text(lang.main_load_data__first), sg.Push()],
        [sg.InputText('', size=35, key='-SCREEN_FOLDER-', justification='left', enable_events=True),
         sg.FolderBrowse(button_text=lang.main__browse_button)],
        [sg.Text(lang.main_load_data__then)],
        [sg.Push(),
         sg.InputText('', visible=False, key='-DATA_PATH-', justification='left', enable_events=True),
         sg.FileSaveAs(lang.main_load_data__new, enable_events=True, key='-CREATE-', size=(15, 1),
                       default_extension=".bangstats",
                       file_types=((lang.main_load_data__files, '*.bangstats'),), disabled=True),
         sg.FileBrowse(lang.main_load_data__load, enable_events=True, key='-LOAD-', size=(15, 1), target=('-DATA_PATH-'),
                       file_types=((lang.main_load_data__files, '*.bangstats'),), disabled=True), sg.Push()],
        [sg.Push(), sg.Text("", key="-STATUS-"), sg.Push()],
    ]

    window = sg.Window('BanG Stats!', layout, icon=defaults.icoKasumi)

    while True:
        event, values = window.read()

        if event == '-SCREEN_FOLDER-':
            if os.path.exists(values['-SCREEN_FOLDER-']):
                screenDirList = [f for f in os.listdir(values['-SCREEN_FOLDER-']) if
                                 f.endswith('.png') or f.endswith('.jpg')]
                if len(screenDirList) > 0:
                    window['-CREATE-'].update(disabled=False)
                    window['-LOAD-'].update(disabled=False)
                    window['-STATUS-'].update(f"{len(screenDirList)} {lang.main_load_data__info_images_found}")
                else:
                    window['-STATUS-'].update(lang.main_load_data__error_no_images)
                    window['-CREATE-'].update(disabled=True)
                    window['-LOAD-'].update(disabled=True)
            else:
                window['-STATUS-'].update(lang.main_load_data__error_no_directory)
                window['-CREATE-'].update(disabled=True)
                window['-LOAD-'].update(disabled=True)

        if event == '-DATA_PATH-':
            if not os.path.isfile(values['-DATA_PATH-']):
                with open(values['-DATA_PATH-'], 'w') as f:
                    f.write('{}')

            dbh.save_session(values['-DATA_PATH-'], values['-SCREEN_FOLDER-'], defaults.language)

            window.close()

            return values['-DATA_PATH-'], values['-SCREEN_FOLDER-']

        if event == sg.WIN_CLOSED:
            exit(0)


def update_data():
    global imagesStored, imagesScanned, imagesErrors, screenDirList, newImages, window

    # Initialize songs database and get information about songs and stored images
    songsAmount, imagesStored = dbh.data_init(dataJson)

    imagesScanned = dbh.read_temp_data()
    imagesErrors = dbh.read_temp_errors()

    imagesScannedFileNames = []
    for image in imagesScanned:
        imagesScannedFileNames.append(image.split("'")[-2])

    screenDirList = [f for f in os.listdir(imagesFolderPath) if f.endswith('.png') or f.endswith('.jpg')]
    newImages = set(screenDirList) - set(imagesStored.keys()) - set(imagesScannedFileNames) - set(imagesErrors)

    window['-STAT_SAVED-'].update(len(imagesStored))
    window['-STAT_SCANNED-'].update(len(imagesScanned))
    window['-STAT_UNSCANNED-'].update(len(newImages))
    window['-STAT_ERRORS-'].update(len(imagesErrors))
    window['-SONGS-'].update(songsAmount)


sg.theme('Purple')  # Add a touch of color

# Get current locale 2-letter code
userLanguage = lang.getISO(locale.getlocale()[0].split('_')[0])

# Check if user already has a session with data file and images path
if os.path.isfile(defaults.sessionJson):
    session = dbh.read_session()

    dataJson = session["dataPath"]
    imagesFolderPath = session["imagesFolderPath"]
    currentLanguage = session["language"]

    lang.set_language(currentLanguage)

else:
    # Check if user language is supported, if not, set default language
    if userLanguage in lang.langList:
        currentLanguage = userLanguage
    else:
        currentLanguage = defaults.language

    lang.set_language(currentLanguage)

    dataJson, imagesFolderPath = load_data()



# Close program if user language is russian
if userLanguage == "ru":
    sg.Window('Fuee...', [[sg.Text(
        'Пользователи стран террористов не допускаются.')],
        [sg.Push(),sg.Text("Слава Україні!"),sg.Push()],
        [sg.Push(), sg.Button("Я поддерживаю войну.", enable_events=True, key='-OK-', size=(25, 1))
            , sg.Push()]], icon=defaults.icoKanon).read(close=True)
    exit(0)

firstDataLayout = [
    [sg.Text(lang.main__scan_info)],
    [sg.Button(lang.main__scan_button, enable_events=True, key='-SCAN-', size=(20, 2))],
    [sg.Text(lang.main__post_info)],
    [sg.Button(lang.main__post_button, enable_events=True, key='-POST-', size=(20, 2))],
]

secondDataLayout = [
    [sg.Text(lang.main__profile_info)],
    [sg.Button(lang.main__profile_button, enable_events=True, key='-PROF-', size=(20, 2))],
    [sg.Text(lang.main__browse_info)],
    [sg.Button(lang.main__browse_button, enable_events=True, key='-BROWSE-', size=(20, 2))],
]

infoLayout = [
    [sg.Text(lang.main__info_stored), sg.Push(), sg.Text("", key="-STAT_SAVED-")],
    [sg.Text(lang.main__info_scanned), sg.Push(), sg.Text("", key="-STAT_SCANNED-")],
    [sg.Text(lang.main__info_unscanned), sg.Push(), sg.Text("", key="-STAT_UNSCANNED-")],
    [sg.Text(lang.main__info_errors), sg.Push(), sg.Text("", key="-STAT_ERRORS-")],
    [sg.Text(lang.main__info_songsdb), sg.Push(), sg.Text("", key='-SONGS-')],
    [sg.Push(), sg.Button(lang.main__info_change, enable_events=True, key='-CHANGE-', size=(15, 1)), sg.Push()]
]

layout = [
    [sg.Frame(lang.main__layout_info, infoLayout, font=("", 12), size=(200, 180)),
     sg.Push(), sg.Image(defaults.logoPath, size=(960, 200))],
    [sg.Frame(lang.main__layout_creation, firstDataLayout, font=("", 12), size=(412, 180)),
     sg.Frame(lang.main__layout_visual, secondDataLayout, font=("", 12), size=(412, 180))],
    [sg.Text(lang.main__layout_created, key="-M-", enable_events=True,tooltip=lang.main__tooltip_clickme), sg.Push(),
     sg.Combo(lang.langList, default_value=currentLanguage, enable_events=True, key='-LANG-'),
     sg.Text(f"{lang.main__layout_version} {defaults.version}")]
]

window = sg.Window('BanG Stats!', layout, size=(864, 430), icon=defaults.icoKasumi, finalize=True)

update_data()

while True:
    event, values = window.read()

    if event == '-SCAN-':
        import data.scan as scan

        scan.main(imagesFolderPath, newImages)

        imagesScanned = dbh.read_temp_data()
        imagesErrors = dbh.read_temp_errors()

        window['-STAT_UNSCANNED-'].update(len(newImages) - len(imagesScanned))

    elif event == '-POST-':
        if os.path.isfile(defaults.tempDataFile) or os.path.isfile(dataJson):
            import data.post as post

            post.main(imagesStored, imagesScanned, imagesErrors, imagesFolderPath)
        else:
            sg.Window('Fuee...', [[sg.Text(
                'No data to process. Start by scanning your screenshots.'
            )], [sg.Push(), sg.OK(s=10), sg.Push()]], icon=defaults.icoKanon).read(close=True)

    elif event == '-CHANGE-':
        # Delete session file
        os.remove(defaults.sessionJson)
        # Load new data
        dataJson, imagesFolderPath = load_data()

    elif event == '-PROF-':
        import data.profile as profile
        profile.main()

    elif event == '-LANG-':
        dbh.save_session(dataJson, imagesFolderPath, values['-LANG-'])

        window.close()
        os.execl(sys.executable, sys.executable, *sys.argv)


    elif event == '-BROWSE-':
        sg.Window('Doki... Doki... ', [[sg.Text(
            'This part is not ready yet. Please wait for the next update.\n\n'
            'If you really curious, you can browse your data manually by opening the data file.'
        )], [sg.Push(), sg.OK(s=10), sg.Push()]], icon=defaults.icoArisa).read(close=True)


    elif event == '-M-':
        import webbrowser
        webbrowser.open('https://linktr.ee/MikeAtom')


    elif event == sg.WIN_CLOSED or event == 'Exit':
        break

    update_data()

window.close()
