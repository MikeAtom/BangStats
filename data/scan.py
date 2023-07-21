import os
import cv2
import shutil
import timeit
import PySimpleGUI as sg
from datetime import timedelta
import data._defaults as defaults
import data.scripts.db_handler as dbh
import data.scripts.lang_handler as lang
from data.scripts.score_extractor import scan_score


def create_preview(imagePath, targetHeight):

    # copy image to temp folder
    shutil.copy(imagePath, defaults.tempImagePreview)


    # Read image
    image = cv2.imread(defaults.tempImagePreview)
    # Resize image height
    height, width, channels = image.shape
    ratio = targetHeight / height
    image = cv2.resize(image, (int(width * ratio), targetHeight))
    # Save preview
    cv2.imwrite(defaults.tempImagePreview, image)

    return defaults.tempImagePreview


def main(imagesFolderPath, imageList):

    # Define variables
    isCudaAvailable = True
    imageCount = 0
    errorCount = 0
    processCount = 0
    elapsedTime = 0


    # Layout with options
    setOptionsLayout = [
        [sg.Checkbox(lang.scan__options_usegpu, default=isCudaAvailable, key='-GPU-', disabled=not isCudaAvailable,
                     tooltip=lang.scan__options_usegpu_tooltip)],
        [sg.Text(lang.scan__options_onerror), sg.Combo([lang.scan__options_onerror_skip,
                                                        lang.scan__options_onerror_pause,
                                                        lang.scan__options_onerror_selfdestruct],
                                       tooltip = lang.scan__options_onerror_tooltip,
                                       default_value=lang.scan__options_onerror_skip,
                                       key='-ON_ERROR-',
                                       enable_events=True,
                                       readonly=True)]
    ]

    # Button to start scan
    buttonsLayout = sg.Button(lang.scan__button_start_scan, enable_events=True, key='-START-', size=(22, 2))

    # Layout with instructions how to use the scanner
    guideLayout = [
        [sg.Text(lang.scan__guide_first)],
        [sg.Text(lang.scan__guide_second)],
        [sg.Text(lang.scan__guide_third)],
        [sg.Text()],
        [sg.Text(lang.scan__guide_fourth)]
    ]

    # Layout with useful information
    infoLayout = [
        [sg.Text(lang.scan__info_first)],
        [sg.Text(lang.scan__info_second)],
        [sg.Text(lang.scan__info_third)],
        [sg.Text(lang.scan__info_fourth)],
    ]

    col1 = sg.Column([
        [sg.Push(), buttonsLayout, sg.Push()],
        [sg.Frame(lang.scan__options, setOptionsLayout, font=("", 12))]
    ])

    col2 = sg.Column([
        [sg.Frame(lang.scan__how_to, guideLayout, font=("", 12), size=(240,158)),
         sg.Frame(lang.scan__info, infoLayout, font=("", 12), size=(480,158))]
    ])

    # Define main layout
    layout = [
        [sg.Text(lang.scan__layout_title, font=("", 16)), sg.Push(),
         sg.Button(lang.global__button_back, size=(5, 1))],
        [sg.HSeparator()],
        [sg.Text(lang.scan__layout_image_folder + " " + imagesFolderPath)],
        # [sg.HSeparator()],
        [sg.Push(), sg.Image(filename=defaults.previewImage, size=(640, 360), key="-PREVIEW-"), sg.Push()],
        [sg.Push(), sg.Text("┐(￣ヘ￣;)┌", key='-CUR_IMAGE-'), sg.Push()],
        [sg.HSeparator()],
        [sg.Push(), sg.ProgressBar(40, size=(45, 20), key='-PROGRESS-'), sg.Push()],
        [sg.Push(), sg.Text(lang.scan__layout_errors), sg.Text("0", key="-ERRORS-"), sg.Push(),
         sg.Text(imageCount, key='-IMAGE_COMP-'), sg.Text("/"), sg.Text(len(imageList), key='-IMAGE_COUNT-'),
         sg.Push(), sg.Text("~0:00:00", key='-ETA-'),
         sg.Push()],
        [sg.HSeparator()],
        [col1, col2]
    ]

    if len(imageList) == 0:
        sg.Window('Excellent!', [[sg.Text(
            lang.scan__complete_window_text
        )],
            [sg.Push(), sg.OK(s=10), sg.Push()]], disable_close=True, icon=defaults.icoChu2
                  ).read(close=True)
        return

    # Create the window
    window = sg.Window(f'BanG Stats! // {lang.scan__layout_title}', layout, size=(960, 720), finalize=True,
                       icon=defaults.icoKasumi)

    # Show warning if temporary data file exists, which can happen only if the process was interrupted
    if os.path.exists(defaults.tempDataFile):
        sg.Window('Fuee...?', [[sg.Text(
            lang.scan__prev_scan_window_text + defaults.tempDataFile
        )], [sg.Push(), sg.OK(s=10), sg.Push()]], disable_close=True, icon=defaults.icoKanon).read(close=True)

        # Update GUI
        # Change button text from "Start scan" to "Continue" to indicate that the scan can be continued
        window['-START-'].update(lang.scan__button_continue, disabled=False)


    while True:
        # Read window events
        event, values = window.read()

        # Get number of images
        imageCount = len(imageList)


        # If user starts scan and there are images in the target folder
        if event == '-START-' and imageCount > 0:
            # Import ocr handler
            from data.scripts.ocr_handler import ocr

            # Disable start button and change text to "In progress..."
            window['-START-'].update(lang.scan__button_in_progress, disabled=True)

            # For all images that are scheduled for scan, excluding images that are already have been scanned
            for imageName in imageList:
                # Start timer
                start = timeit.default_timer()

                # Get image path
                imagePath = os.path.join(imagesFolderPath, imageName)

                # Image preview creation
                # Update preview in GUI
                window['-CUR_IMAGE-'].update(imageName)
                window['-PREVIEW-'].update(filename=create_preview(imagePath, 360))
                window.refresh()

                # Read image using OCR
                imageData = ocr(imagePath, values['-GPU-'])

                # Scan score from image
                try:
                    score = scan_score(imageData)
                    score['image'] = imageName

                    dbh.write_temp_data(score)

                # If error occurs
                except:
                    errorCount += 1

                    # Check user error handling desired behavior
                    if values['-ON_ERROR-'] == "Pause":
                        # Pause scan with error message
                        sg.Window('ERRORtional!', [[sg.Text(
                            lang.scan__error_window_text + imageName + '\n')],
                            [sg.Push(), sg.OK(s=10), sg.Push()]], disable_close=True, icon=defaults.icoTsugi
                                  ).read(close=True)
                    elif values['-ON_ERROR-'] == "Self-destruct":
                        # F*cking annihilate the program XD
                        exit()  # Not so epic for now

                    dbh.write_temp_error(imageName)

                # Stop timer
                stop = timeit.default_timer()

                # Update counter
                processCount += 1

                # Update time and eta
                time = stop - start
                elapsedTime += time
                eta = (imageCount - processCount) * (elapsedTime / processCount)
                # Show eta in hh:mm:ss format
                eta = str(timedelta(seconds=eta))

                # Update preview
                window['-IMAGE_COMP-'].update(processCount)
                window['-ERRORS-'].update(errorCount)
                window['-PROGRESS-'].update_bar(processCount, imageCount)
                window['-ETA-'].update("~" + str(eta).split(".")[0])

            # When scan is completed change button text to "Completed"
            sg.Window('Hope you enjoy it!', [[sg.Text(
                lang.scan__complete_window_title)],
                [sg.Push(), sg.OK(s=10), sg.Push()]], disable_close=True, icon=defaults.icoRokka
                      ).read(close=True)
            window['-START-'].update(lang.scan__button_completed, disabled=True)

        # If user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == lang.global__button_back:
            break

    window.close()
