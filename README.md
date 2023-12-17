# PixelPioneer

Discover the ease of image management with this innovative program! With the user-friendly interface, you can effortlessly browse through your images, sort them quickly and add individual keywords. Finding the perfect snap has never been easier - just enter the keyword you want and voilà! Experience the freedom to organize your photos in seconds and navigate your visual memories with ease. Managing your image collection has never been easier - try it now and discover the world of effortless image organization! 

## Currently working on

MacOS: ✓
Windows: x
Linux: Testing

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

You need to install Python 3 on your device.

Install the dependencies using ```pip install -r requirements.txt``` or ```pip3 install -r requirements.txt```.
After you install the dependencies, run the set_path.sh file. Please provide the complete path to your unsorted images.
e.g.: ```/Users/user/Pictures/```.

To check which path is set, option 2 is suitable. Run the set_path.sh file and enter 2. Then you will get the full path to your pictures.

## Usage

When you start the server, all images that are not sorted are automatically organized into a folder structure. If you want to sort images after starting the server, you can do this by calling the URL ```/sort```.

To see the images on a specific date, you can do this via the calendar. The year, associated months and days in which there are images are highlighted in dark. The years are always displayed starting from the earliest available image. e.g. 2007-2023 or 2021-2023.

If you have tagged your images, you can search for them using the search bar. Simply enter your desired search term or search terms in the search bar and press Enter.

## License

This project is licensed under the [Apache License] - see the [LICENSE.md](LICENSE.md) file for details.
