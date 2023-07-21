import json
import os
import data._defaults as defaults


def set_language(lang):
    global langData

    # open lang file
    with open(defaults.langPath + f'{lang}.json', encoding='utf-8') as f:
        langData = json.load(f)

    global__button_back = langData["global__button_back"]

    main_load_data__welcome = langData["main_load_data__welcome"]
    main_load_data__first = langData["main_load_data__first"]
    main_load_data__then = langData["main_load_data__then"]
    main_load_data__new = langData["main_load_data__new"]
    main_load_data__load = langData["main_load_data__load"]
    main_load_data__files = langData["main_load_data__files"]
    main_load_data__info_images_found = langData["main_load_data__info_images_found"]
    main_load_data__error_no_images = langData["main_load_data__error_no_images"]
    main_load_data__error_no_directory = langData["main_load_data__error_no_directory"]
    main__scan_info = langData["main__scan_info"]
    main__scan_button = langData["main__scan_button"]
    main__post_info = langData["main__post_info"]
    main__post_button = langData["main__post_button"]
    main__profile_info = langData["main__profile_info"]
    main__profile_button = langData["main__profile_button"]
    main__browse_info = langData["main__browse_info"]
    main__browse_button = langData["main__browse_button"]
    main__info_stored = langData["main__info_stored"]
    main__info_scanned = langData["main__info_scanned"]
    main__info_unscanned = langData["main__info_unscanned"]
    main__info_errors = langData["main__info_errors"]
    main__info_songsdb = langData["main__info_songsdb"]
    main__info_change = langData["main__info_change"]
    main__layout_info = langData["main__layout_info"]
    main__layout_creation = langData["main__layout_creation"]
    main__layout_visual = langData["main__layout_visual"]
    main__layout_created = langData["main__layout_created"]
    main__tooltip_clickme = langData["main__tooltip_clickme"]
    main__layout_version = langData["main__layout_version"]

    scan__options_usegpu = langData["scan__options_usegpu"]
    scan__options_usegpu_tooltip = langData["scan__options_usegpu_tooltip"]
    scan__options_onerror = langData["scan__options_onerror"]
    scan__options_onerror_tooltip = langData["scan__options_onerror_tooltip"]
    scan__options_onerror_skip = langData["scan__options_onerror_skip"]
    scan__options_onerror_pause = langData["scan__options_onerror_pause"]
    scan__options_onerror_selfdestruct = langData["scan__options_onerror_selfdestruct"]
    scan__button_start_scan = langData["scan__button_start_scan"]
    scan__button_continue = langData["scan__button_continue"]
    scan__button_in_progress = langData["scan__button_in_progress"]
    scan__button_completed = langData["scan__button_completed"]
    scan__guide_first = langData["scan__guide_first"]
    scan__guide_second = langData["scan__guide_second"]
    scan__guide_third = langData["scan__guide_third"]
    scan__guide_fourth = langData["scan__guide_fourth"]
    scan__info_first = langData["scan__info_first"]
    scan__info_second = langData["scan__info_second"]
    scan__info_third = langData["scan__info_third"]
    scan__info_fourth = langData["scan__info_fourth"]
    scan__options = langData["scan__options"]
    scan__how_to = langData["scan__how_to"]
    scan__info = langData["scan__info"]
    scan__layout_title = langData["scan__layout_title"]
    scan__layout_image_folder = langData["scan__layout_image_folder"]
    scan__layout_errors = langData["scan__layout_errors"]
    scan__complete_window_text = langData["scan__complete_window_text"]
    scan__prev_scan_window_text = langData["scan__prev_scan_window_text"]
    scan__error_window_text = langData["scan__error_window_text"]
    scan__complete_window_title = langData["scan__complete_window_title"]

    post__enter_name_listbox = langData["post__enter_name_listbox"]
    post__enter_song_data_deleted_message = langData["post__enter_song_data_deleted_message"]
    post__enter_song_data_saved_message = langData["post__enter_song_data_saved_message"]
    post__enter_song_data_invalid_message = langData["post__enter_song_data_invalid_message"]
    post__check_inconsistencies_no_inconsistencies = langData["post__check_inconsistencies_no_inconsistencies"]
    post__main_songdata_name = langData["post__main_songdata_name"]
    post__main_songdata_name_tooltip = langData["post__main_songdata_name_tooltip"]
    post__main_songdata_search = langData["post__main_songdata_search"]
    post__main_songdata_search_tooltip = langData["post__main_songdata_search_tooltip"]
    post__main_songdata_difficulty = langData["post__main_songdata_difficulty"]
    post__main_songdata_difficulty_tooltip = langData["post__main_songdata_difficulty_tooltip"]
    post__main_songdata_level = langData["post__main_songdata_level"]
    post__main_songdata_level_tooltip = langData["post__main_songdata_level_tooltip"]
    post__main_action_start = langData["post__main_action_start"]
    post__main_action_start_tooltip = langData["post__main_action_start_tooltip"]
    post__main_action_save = langData["post__main_action_save"]
    post__main_action_save_tooltip = langData["post__main_action_save_tooltip"]
    post__main_action_skip = langData["post__main_action_skip"]
    post__main_action_skip_tooltip = langData["post__main_action_skip_tooltip"]
    post__main_action_next = langData["post__main_action_next"]
    post__main_action_reset = langData["post__main_action_reset"]
    post__main_action_reset_tooltip = langData["post__main_action_reset_tooltip"]
    post__main_action_delete = langData["post__main_action_delete"]
    post__main_action_delete_tooltip = langData["post__main_action_delete_tooltip"]
    post__main_action_abort = langData["post__main_action_abort"]
    post__main_action_abort_tooltip = langData["post__main_action_abort_tooltip"]
    post__main_fix_scan_errors = langData["post__main_fix_scan_errors"]
    post__main_fix_scan_errors_tooltip = langData["post__main_fix_scan_errors_tooltip"]
    post__main_fix_unknown_songs = langData["post__main_fix_unknown_songs"]
    post__main_fix_unknown_songs_tooltip = langData["post__main_fix_unknown_songs_tooltip"]
    post__main_fix_notes_missmatch = langData["post__main_fix_notes_missmatch"]
    post__main_fix_notes_missmatch_tooltip = langData["post__main_fix_notes_missmatch_tooltip"]
    post__main_fix_fastslow_tooltip = langData["post__main_fix_fastslow_tooltip"]
    post__main_data_store_scanned = langData["post__main_data_store_scanned"]
    post__main_data_store_scanned_tooltip = langData["post__main_data_store_scanned_tooltip"]
    post__main_data_stored = langData["post__main_data_stored"]
    post__main_data_stored_tooltip = langData["post__main_data_stored_tooltip"]
    post__main_data_scanned = langData["post__main_data_scanned"]
    post__main_data_scanned_tooltip = langData["post__main_data_scanned_tooltip"]
    post__main_guide_first = langData["post__main_guide_first"]
    post__main_guide_second = langData["post__main_guide_second"]
    post__main_guide_third = langData["post__main_guide_third"]
    post__main_guide_fourth = langData["post__main_guide_fourth"]
    post__main_guide_filth = langData["post__main_guide_filth"]
    post__main_layout_fix_type = langData["post__main_layout_fix_type"]
    post__main_layout_song_data = langData["post__main_layout_song_data"]
    post__main_layout_actions = langData["post__main_layout_actions"]
    post__main_layout_how_to = langData["post__main_layout_how_to"]
    post__main_layout_title = langData["post__main_layout_title"]
    post__all_type_fixed_window_text = langData["post__all_type_fixed_window_text"]

    profile__display_table_difficulty = langData["profile__display_table_difficulty"]
    profile__display_table_name = langData["profile__display_table_name"]
    profile__display_table_playcount = langData["profile__display_table_playcount"]
    profile__display_table_accuracy = langData["profile__display_table_accuracy"]
    profile__display_table_playedmorethan = langData["profile__display_table_playedmorethan"]
    profile__main_songs = langData["profile__main_songs"]
    profile__main_charts = langData["profile__main_charts"]
    profile__main_time = langData["profile__main_time"]
    profile__main_notes = langData["profile__main_notes"]
    profile__main_accuracy = langData["profile__main_accuracy"]
    profile__main_layout_title = langData["profile__main_layout_title"]
    profile__main_layout_alltime = langData["profile__main_layout_alltime"]
    profile__main_layout_last30days = langData["profile__main_layout_last30days"]
    profile__main_layout_topchart = langData["profile__main_layout_topchart"]
    profile__main_layout_times = langData["profile__main_layout_times"]

    globals().update(locals())


def getISO(lang):
    iso639 = {'Abkhaz': 'ab', 'Afar': 'aa', 'Afrikaans': 'af', 'Akan': 'ak', 'Albanian': 'sq', 'Amharic': 'am',
              'Arabic': 'ar', 'Aragonese': 'an', 'Armenian': 'hy', 'Assamese': 'as', 'Avaric': 'av',
              'Avestan': 'ae', 'Aymara': 'ay', 'Azerbaijani': 'az', 'Bambara': 'bm', 'Bashkir': 'ba',
              'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bihari': 'bh', 'Bislama': 'bi',
              'Bosnian': 'bs', 'Breton': 'br', 'Bulgarian': 'bg', 'Burmese': 'my', 'Catalan; Valencian': 'ca',
              'Chamorro': 'ch', 'Chechen': 'ce', 'Chichewa; Chewa; Nyanja': 'ny', 'Chinese': 'zh', 'Chuvash': 'cv',
              'Cornish': 'kw', 'Corsican': 'co', 'Cree': 'cr', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da',
              'Divehi; Maldivian;': 'dv', 'Dutch': 'nl', 'Dzongkha': 'dz', 'English': 'en', 'Esperanto': 'eo',
              'Estonian': 'et', 'Ewe': 'ee', 'Faroese': 'fo', 'Fijian': 'fj', 'Finnish': 'fi', 'French': 'fr',
              'Fula': 'ff', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek, Modern': 'el',
              'Guaraní': 'gn', 'Gujarati': 'gu', 'Haitian': 'ht', 'Hausa': 'ha', 'Hebrew (modern)': 'he',
              'Herero': 'hz', 'Hindi': 'hi', 'Hiri Motu': 'ho', 'Hungarian': 'hu', 'Interlingua': 'ia',
              'Indonesian': 'id', 'Interlingue': 'ie', 'Irish': 'ga', 'Igbo': 'ig', 'Inupiaq': 'ik', 'Ido': 'io',
              'Icelandic': 'is', 'Italian': 'it', 'Inuktitut': 'iu', 'Japanese': 'ja', 'Javanese': 'jv',
              'Kalaallisut': 'kl', 'Kannada': 'kn', 'Kanuri': 'kr', 'Kashmiri': 'ks', 'Kazakh': 'kk',
              'Khmer': 'km', 'Kikuyu, Gikuyu': 'ki', 'Kinyarwanda': 'rw', 'Kirghiz, Kyrgyz': 'ky', 'Komi': 'kv',
              'Kongo': 'kg', 'Korean': 'ko', 'Kurdish': 'ku', 'Kwanyama, Kuanyama': 'kj', 'Latin': 'la',
              'Luxembourgish': 'lb', 'Luganda': 'lg', 'Limburgish': 'li', 'Lingala': 'ln', 'Lao': 'lo',
              'Lithuanian': 'lt', 'Luba-Katanga': 'lu', 'Latvian': 'lv', 'Manx': 'gv', 'Macedonian': 'mk',
              'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Māori': 'mi',
              'Marathi (Marāṭhī)': 'mr', 'Marshallese': 'mh', 'Mongolian': 'mn', 'Nauru': 'na',
              'Navajo, Navaho': 'nv', 'Norwegian Bokmål': 'nb', 'North Ndebele': 'nd', 'Nepali': 'ne',
              'Ndonga': 'ng', 'Norwegian Nynorsk': 'nn', 'Norwegian': 'no', 'Nuosu': 'ii', 'South Ndebele': 'nr',
              'Occitan': 'oc', 'Ojibwe, Ojibwa': 'oj', 'Old Church Slavonic': 'cu', 'Oromo': 'om', 'Oriya': 'or',
              'Ossetian, Ossetic': 'os', 'Panjabi, Punjabi': 'pa', 'Pāli': 'pi', 'Persian': 'fa', 'Polish': 'pl',
              'Pashto, Pushto': 'ps', 'Portuguese': 'pt', 'Quechua': 'qu', 'Romansh': 'rm', 'Kirundi': 'rn',
              'Romanian, Moldavan': 'ro', 'Russian': 'ru', 'Sanskrit (Saṁskṛta)': 'sa', 'Sardinian': 'sc',
              'Sindhi': 'sd', 'Northern Sami': 'se', 'Samoan': 'sm', 'Sango': 'sg', 'Serbian': 'sr',
              'Scottish Gaelic': 'gd', 'Shona': 'sn', 'Sinhala, Sinhalese': 'si', 'Slovak': 'sk', 'Slovene': 'sl',
              'Somali': 'so', 'Southern Sotho': 'st', 'Spanish; Castilian': 'es', 'Sundanese': 'su',
              'Swahili': 'sw', 'Swati': 'ss', 'Swedish': 'sv', 'Tamil': 'ta', 'Telugu': 'te', 'Tajik': 'tg',
              'Thai': 'th', 'Tigrinya': 'ti', 'Tibetan': 'bo', 'Turkmen': 'tk', 'Tagalog': 'tl', 'Tswana': 'tn',
              'Tonga': 'to', 'Turkish': 'tr', 'Tsonga': 'ts', 'Tatar': 'tt', 'Twi': 'tw', 'Tahitian': 'ty',
              'Uighur, Uyghur': 'ug', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uzbek': 'uz', 'Venda': 've',
              'Vietnamese': 'vi', 'Volapük': 'vo', 'Walloon': 'wa', 'Welsh': 'cy', 'Wolof': 'wo',
              'Western Frisian': 'fy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zhuang, Chuang': 'za',
              'Zulu': 'zu'}

    return iso639[lang]

# Load available languages
langList = []

for file in os.listdir(defaults.langPath):
    if file.endswith(".json"):
        langList.append(file[:-5])


