#Web Scraping with Selenium
Overview
This Python script is used to scrape data from online room booking websites in different cities of Ethiopia. The script extracts information such as hotel names, room types, room prices, and pictures of each room in each city. The extracted data is then saved into two Excel files: one for hotel information and another for room information.

![Capture](https://github.com/atnatiyos/Web-scrapping-with-selenium/assets/39485678/db5f51a9-79b0-4075-ad7d-01634670892e)

selenium extract hotel coordinate by searching on google map in prder to get latitude and logitude
![image](https://github.com/atnatiyos/Web-scrapping-with-selenium/assets/39485678/6f0ace41-4a2d-4ee5-a107-af67ad1648cb)

##Prerequisites
Python 3.x or 2.x
Selenium
Chrome WebDriver (for Chrome browser)
Install the required Python packages using pip:


pip install selenium
Download the Chrome WebDriver from here and place it in the same directory as your script.

##Usage
Run the Python script (webscraper.py) using the command:


python webscraper.py
The script will launch a Chrome browser and start scraping the websites for hotel and room information.

Once the scraping is complete, two Excel files (hotels.xlsx and rooms.xlsx) will be generated with the extracted data.

Notes
The script uses Selenium to search for hotels on Google Maps and extract their latitude and longitude coordinates since the Google Location Finder API is a paid service.
Ensure that you have a stable internet connection while running the script, as it relies on real-time data from the websites.
