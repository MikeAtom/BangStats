from time import time
import PySimpleGUI as sg
import data._defaults as defaults
import data.scripts.db_handler as dbh
import data.scripts.lang_handler as lang

sg.theme('Purple')  # Add a touch of color


def calculate_stats(timeTrim=0):
    global accuracyList, totalTimePlaying, totalSongPlayed, chartPlayedList, diffPlayedList, totalNotes, totalFC, totalAP

    # Get formatted data from user's data file
    topSongs = dbh.format_data(timeTrim)

    # Initialize variables and lists
    accuracyList = []
    chartPlayedList = []
    diffPlayedList = {'easy': 0, 'normal': 0, 'hard': 0, 'expert': 0, 'special': 0}
    totalNotes = {'perfect': 0, 'great': 0, 'good': 0, 'bad': 0, 'miss': 0, 'fast': 0, 'slow': 0}

    totalFC = 0
    totalAP = 0
    totalSongPlayed = 0
    totalTimePlaying = 0

    # Get data that will be used
    for key in topSongs.keys():
        totalSongPlayed += 1

        for diff in ['easy', 'normal', 'hard', 'expert', 'special']:
            diffPlayedList[diff] += topSongs[key][diff]['count']

            totalTimePlaying += topSongs[key][diff]['count'] * dbh.songsData[key]['time']
            totalFC += topSongs[key][diff]['fc']
            totalAP += topSongs[key][diff]['ap']

            totalNotes['perfect'] += topSongs[key][diff]['perfect']
            totalNotes['great'] += topSongs[key][diff]['great']
            totalNotes['good'] += topSongs[key][diff]['good']
            totalNotes['bad'] += topSongs[key][diff]['bad']
            totalNotes['miss'] += topSongs[key][diff]['miss']
            totalNotes['fast'] += topSongs[key][diff]['fast']
            totalNotes['slow'] += topSongs[key][diff]['slow']

            if topSongs[key][diff]['count'] > 0:
                accuracyList += topSongs[key][diff]['accuracy']

                chartPlayedList.append({
                    "difficulty": diff,
                    "name": key,
                    "count": topSongs[key][diff]['count'],
                    "accuracy": topSongs[key][diff]['accuracy'],
                    "fc": topSongs[key][diff]['fc'],
                    "ap": topSongs[key][diff]['ap']
                })

    # sort list by count
    chartPlayedList.sort(key=lambda x: x['count'], reverse=True)

    # convert totalTimePlaying to hours from milliseconds and round it to 2 decimals
    totalTimePlaying = round(totalTimePlaying / 3600000, 1)


def display_table(tableData):
    headings = [lang.profile__display_table_difficulty, lang.profile__display_table_name,
                lang.profile__display_table_playcount, lang.profile__display_table_accuracy
                , " FC ", " AP "]

    # convert tableData to list of lists
    tableData = [list(tableData[i].values()) for i in range(len(tableData))]
    for i in tableData:
        i[3] = f"{round(sum(i[3]) / len(i[3]), 2)}%"
        tableData[tableData.index(i)] = i

    showTableData = tableData

    prevEvent = None
    isReverse = False

    layout = [
        [sg.Table(values=showTableData, headings=headings, max_col_width=25,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='center',
                  num_rows=20,
                  alternating_row_color='lightblue',
                  key='-TABLE-',
                  enable_events=True,
                  expand_x=True,
                  expand_y=True,
                  vertical_scroll_only=False,
                  enable_click_events=True,  # Comment out to not enable header and other clicks
                  tooltip='This is a table')],
        # Checkbox for each difficulty
        [sg.Checkbox("Easy", default=True, key='-EASY-', enable_events=True),
         sg.Checkbox("Normal", default=True, key='-NORMAL-', enable_events=True),
         sg.Checkbox("Hard", default=True, key='-HARD-', enable_events=True),
         sg.Checkbox("Expert", default=True, key='-EXPERT-', enable_events=True),
         sg.Checkbox("Special", default=True, key='-SPECIAL-', enable_events=True)],
        # Played more than x {lang.profile__main_layout_times} textbox
        [sg.Text(lang.profile__display_table_playedmorethan), sg.InputText("0", size=(5, 1), key='-PLAYED_MORE_THAN-', enable_events=True),
        sg.Push(), sg.Button(lang.global__button_back, key="-BACK-"), sg.Sizegrip()]
    ]

    windowTable = sg.Window('Bushido!', layout, resizable=True, icon="data/icons/eve.ico")

    while True:
        event, values = windowTable.read()

        if type(event) == tuple and event[2][0] == -1:
            isReverse = not isReverse if prevEvent == event else False

            showTableData.sort(key=lambda x: x[event[2][1]], reverse=isReverse)
            tableData.sort(key=lambda x: x[event[2][1]], reverse=isReverse)

            windowTable['-TABLE-'].update(values=showTableData)

            prevEvent = event

        # Filter table data by difficulty and played more than x {lang.profile__main_layout_times} if any of the checkboxes or textbox is changed
        elif event == '-EASY-' or event == '-NORMAL-' or event == '-HARD-' or event == '-EXPERT-' or event == '-SPECIAL-' \
                or event == '-PLAYED_MORE_THAN-':
            # Initialize filterDiff list
            filterDiff = [
                'easy' if values['-EASY-'] else '',
                'normal' if values['-NORMAL-'] else '',
                'hard' if values['-HARD-'] else '',
                'expert' if values['-EXPERT-'] else '',
                'special' if values['-SPECIAL-'] else ''
            ]
            # get filterCount from textbox
            try:
                filterCount = int(values['-PLAYED_MORE_THAN-'])
            except ValueError:
                filterCount = 0

            # Filter table data by difficulty and played more than x {lang.profile__main_layout_times}
            showTableData = [i for i in tableData if i[0] in filterDiff and i[2] >= filterCount]

            windowTable['-TABLE-'].update(values=showTableData)

        elif event == sg.WIN_CLOSED or event == '-BACK-':
            break

    windowTable.close()


def main():
    global accuracyList, totalTimePlaying, totalSongPlayed, chartPlayedList, diffPlayedList, totalNotes, window, \
        totalFC, totalAP

    calculate_stats(round(time() - 2592000))
    recentCol1a = sg.Column([
        [sg.Text(lang.profile__main_songs, font=("", 10))],
        [sg.Text(lang.profile__main_charts, font=("", 10))],
        [sg.Text(lang.profile__main_time, font=("", 10))],
        [sg.Text(lang.profile__main_notes, font=("", 10))],
        [sg.Text(lang.profile__main_accuracy, font=("", 10))],
    ])
    recentCol1b = sg.Column([
        [sg.Text(totalSongPlayed, font=("", 10))],
        [sg.Text(len(chartPlayedList), font=("", 10))],
        [sg.Text(f"{totalTimePlaying}h", font=("", 10))],
        [sg.Text(totalNotes['perfect'] + totalNotes['great'] + totalNotes['good'] + totalNotes['bad'], font=("", 10))],
        [sg.Text(f"{round(sum(accuracyList) / len(accuracyList), 2)}%", font=("", 10))]
    ])
    recentCol2a = sg.Column([
        [sg.Text("Easy", font=("", 10))],
        [sg.Text("Normal", font=("", 10))],
        [sg.Text("Hard", font=("", 10))],
        [sg.Text("Expert", font=("", 10))],
        [sg.Text("Special", font=("", 10))],
    ])
    recentCol2b = sg.Column([
        [sg.Text(diffPlayedList['easy'], font=("", 10))],
        [sg.Text(diffPlayedList['normal'], font=("", 10))],
        [sg.Text(diffPlayedList['hard'], font=("", 10))],
        [sg.Text(diffPlayedList['expert'], font=("", 10))],
        [sg.Text(diffPlayedList['special'], font=("", 10))],
    ])
    recentCol3a = sg.Column([
        [sg.Text("Perfect", font=("", 10))],
        [sg.Text("Great", font=("", 10))],
        [sg.Text("Good", font=("", 10))],
        [sg.Text("Bad", font=("", 10))],
        [sg.Text("Miss", font=("", 10))],
    ])
    recentCol3b = sg.Column([
        [sg.Text(totalNotes['perfect'], font=("", 10))],
        [sg.Text(totalNotes['great'], font=("", 10))],
        [sg.Text(totalNotes['good'], font=("", 10))],
        [sg.Text(totalNotes['bad'], font=("", 10))],
        [sg.Text(totalNotes['miss'], font=("", 10))],
    ])
    recentAdditinonalInfo = [
        sg.Push(),
        sg.Text(f"FC: {totalFC}", font=("", 10)),
        sg.Push(),
        sg.Text(f"AP: {totalAP}", font=("", 10)),
        sg.Push(),
        sg.Text(f"Fast/Slow: {round(100 * totalNotes['fast'] / (totalNotes['fast'] + totalNotes['slow']), 2)}%",
                font=("", 10)),
        sg.Push()
    ]

    recentLayout = [
        [recentCol1a, recentCol1b, sg.VSeparator(),
         recentCol2a, recentCol2b, sg.VSeparator(),
         recentCol3a, recentCol3b],
        recentAdditinonalInfo
    ]

    calculate_stats()
    allTimeCol1a = sg.Column([
        [sg.Text(lang.profile__main_songs, font=("", 10))],
        [sg.Text(lang.profile__main_charts, font=("", 10))],
        [sg.Text(lang.profile__main_time, font=("", 10))],
        [sg.Text(lang.profile__main_notes, font=("", 10))],
        [sg.Text(lang.profile__main_accuracy, font=("", 10))],
    ])
    allTimeCol1b = sg.Column([
        [sg.Text(totalSongPlayed, font=("", 10))],
        [sg.Text(len(chartPlayedList), font=("", 10))],
        [sg.Text(f"{totalTimePlaying}h", font=("", 10))],
        [sg.Text(totalNotes['perfect'] + totalNotes['great'] + totalNotes['good'] + totalNotes['bad'], font=("", 10))],
        [sg.Text(f"{round(sum(accuracyList) / len(accuracyList))}", font=("", 10))]
    ])
    allTimeCol2a = sg.Column([
        [sg.Text("Easy", font=("", 10))],
        [sg.Text("Normal", font=("", 10))],
        [sg.Text("Hard", font=("", 10))],
        [sg.Text("Expert", font=("", 10))],
        [sg.Text("Special", font=("", 10))],
    ])
    allTimeCol2b = sg.Column([
        [sg.Text(diffPlayedList['easy'], font=("", 10))],
        [sg.Text(diffPlayedList['normal'], font=("", 10))],
        [sg.Text(diffPlayedList['hard'], font=("", 10))],
        [sg.Text(diffPlayedList['expert'], font=("", 10))],
        [sg.Text(diffPlayedList['special'], font=("", 10))],
    ])
    allTimeCol3a = sg.Column([
        [sg.Text("Perfect", font=("", 10))],
        [sg.Text("Great", font=("", 10))],
        [sg.Text("Good", font=("", 10))],
        [sg.Text("Bad", font=("", 10))],
        [sg.Text("Miss", font=("", 10))],
    ])
    allTimeCol3b = sg.Column([
        [sg.Text(totalNotes['perfect'], font=("", 10))],
        [sg.Text(totalNotes['great'], font=("", 10))],
        [sg.Text(totalNotes['good'], font=("", 10))],
        [sg.Text(totalNotes['bad'], font=("", 10))],
        [sg.Text(totalNotes['miss'], font=("", 10))],
    ])
    allTimeAdditinonalInfo = [
        sg.Push(),
        sg.Text(f"FC: {totalFC}", font=("", 10)),
        sg.Push(),
        sg.Text(f"AP: {totalAP}", font=("", 10)),
        sg.Push(),
        sg.Text(f"Fast/Slow: {round(100 * totalNotes['fast'] / (totalNotes['fast'] + totalNotes['slow']), 2)}%",
                font=("", 10)),
        sg.Push()
    ]

    allTimeLayout = [
        [allTimeCol1a, allTimeCol1b, sg.VSeparator(),
         allTimeCol2a, allTimeCol2b, sg.VSeparator(),
         allTimeCol3a, allTimeCol3b],
        allTimeAdditinonalInfo
    ]

    top1ChartLayout = [
        [sg.VPush()],
        [sg.Text(chartPlayedList[0]['name'], font=("", 10))],
        [sg.Text(f"{chartPlayedList[0]['difficulty']}", font=("", 8)), sg.Push(),
         sg.Text(f"{chartPlayedList[0]['count']} {lang.profile__main_layout_times} / {chartPlayedList[0]['fc']} FCs", font=("", 8))],
        [sg.VPush()]
    ]
    top2ChartLayout = [
        [sg.VPush()],
        [sg.Text(chartPlayedList[1]['name'], font=("", 10))],
        [sg.Text(f"{chartPlayedList[1]['difficulty']}", font=("", 8)), sg.Push(),
         sg.Text(f"{chartPlayedList[1]['count']} {lang.profile__main_layout_times} / {chartPlayedList[1]['fc']} FCs", font=("", 8))],
        [sg.VPush()]
    ]
    top3ChartLayout = [
        [sg.VPush()],
        [sg.Text(chartPlayedList[2]['name'], font=("", 10))],
        [sg.Text(f"{chartPlayedList[2]['difficulty']}", font=("", 8)), sg.Push(),
         sg.Text(f"{chartPlayedList[2]['count']} {lang.profile__main_layout_times} / {chartPlayedList[2]['fc']} FCs", font=("", 8))],
        [sg.VPush()]
    ]
    top4ChartLayout = [
        [sg.VPush()],
        [sg.Text(chartPlayedList[3]['name'], font=("", 10))],
        [sg.Text(f"{chartPlayedList[3]['difficulty']}", font=("", 8)), sg.Push(),
         sg.Text(f"{chartPlayedList[3]['count']} {lang.profile__main_layout_times} / {chartPlayedList[3]['fc']} FCs", font=("", 8))],
        [sg.VPush()]
    ]
    top5ChartLayout = [
        [sg.VPush()],
        [sg.Text(chartPlayedList[4]['name'], font=("", 10))],
        [sg.Text(f"{chartPlayedList[4]['difficulty']}", font=("", 8)), sg.Push(),
         sg.Text(f"{chartPlayedList[4]['count']} {lang.profile__main_layout_times} / {chartPlayedList[4]['fc']} FCs", font=("", 8))],
        [sg.VPush()]
    ]

    layout = [
        [sg.Text(lang.profile__main_layout_title, font=("", 16)), sg.Push(), sg.Button(lang.global__button_back, key="-BACK-", size=(5, 1))],
        [sg.HSeparator()],
        [sg.Frame(lang.profile__main_layout_alltime, allTimeLayout, font=("", 12), size=(458, 190)),
         sg.Frame(lang.profile__main_layout_last30days, recentLayout, font=("", 12), size=(458, 190)), ],
        [sg.Frame(lang.profile__main_layout_topchart, top1ChartLayout, font=("", 12), size=(232, 86)),
         sg.Frame('#2', top2ChartLayout, font=("", 12), size=(159, 86)),
         sg.Frame('#3', top3ChartLayout, font=("", 12), size=(159, 86)),
         sg.Frame('#4', top4ChartLayout, font=("", 12), size=(159, 86)),
         sg.Frame('#5', top5ChartLayout, font=("", 12), size=(159, 86)),
         sg.Button('>', size=(2, 3), key='-MORE_CHART-')]
    ]

    window = sg.Window(f'BanG Stats! // {lang.profile__main_layout_title}', layout, size=(960, 360), icon=defaults.icoKasumi, finalize=True)

    while True:
        event, values = window.read()

        if event == '-MORE_SONG-':
            display_table(totalSongPlayed)
        elif event == '-MORE_CHART-':
            display_table(chartPlayedList)
        elif event == sg.WIN_CLOSED or event == '-BACK-':
            break

    window.close()
