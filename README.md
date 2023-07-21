## BanG Dream! Girls Band Party statistics scanner and manager.

Українська версія цього файлу знаходиться [тут](README_uk.md).

Tool for scanning and analyzing screenshots of the game's live results screen. Functionality would be welcome in the base game, but here we are.

![image](https://cdn.discordapp.com/attachments/882697945772855337/1132066295270080623/image.png)

## Features
- [x] Scan screenshots of the live results screen and extract the results
- [x] Fix them manually if errors occur during scanning
- [x] View statistics your global and per-song statistics
- [x] Localization support

## Installation
1. Download the latest release from the [releases page](https://github.com/MikeAtom/BangStats/releases)
2. Extract the archive to a folder of your choice
3. Install the dependencies by running `pip install -r requirements.txt` in the folder you extracted the archive to
4. Run the program by running `main.pyw` in the folder you extracted the archive to

Side note: If you intend to use GPU acceleration, you will need to have an NVIDIA GPU and install the pytorch with CUDA support. See [here](https://pytorch.org/get-started/locally/) for instructions.

## Usage
First of all, the program cannot get data out of thin air. You will need to provide it with screenshots of the in-game live results screen. The more screenshots you provide, the more accurate the statistics will be.


1. Take all of your screenshots and put them in a single folder of your choice.
2. Open the program and locate the folder with the screenshots.
3. Create a new profile and give it a name.
4. Click the "Scan" button.
5. Follow the instructions on the screen. Keep in mind that the scanning process may take a while, depending on the number of screenshots you provided.
6. When the scanning process is complete, you have to manually fix any errors that may have occurred during the scanning process. Click the "Post-process" button on the main screen to do so.
7. Once again, follow the instructions on the screen.
8. After that, you can view your statistics by clicking the "Profile" button on the main screen.

## Known issues and limitations
- Tested only on Windows, cannot guarantee that it will work on other platforms
- Also tested only on Android screenshots, cannot guarantee that it will work on iOS ones
- The program is made with Endori in mind, so it may not work correctly with screenshots from other servers

## Custom localizations
The program supports custom localizations. To create one, you will need to create a new file in the `data/lang` folder and name it according to the language you want to translate the program to. For example, if you're going to translate the program to German, you will need to create a file named `de.json`. The file must be in JSON format. Use provided localizations as a reference.

## Feedback
If you have any questions, suggestions, or bug reports, feel free to contact me [anywhere](https://linktr.ee/MikeAtom) 
