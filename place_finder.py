


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd

# data = pd.read_csv("Hotel_data Bahirdar.csv")
# Hotel_names = data['Hotel Name'] + " " + data['City Location']


# for Hotel_name in Hotel_names:

def location(Hotel_name):   

    chrome_options = webdriver.ChromeOptions()

    # Set the window size (replace width and height with your desired values)
    chrome_options.add_argument('--window-size=600,400')

    # Initialize the Chrome WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    # Open Google Maps
    driver.get("https://www.google.com/maps")

    # Replace 'Your_Location' with the location you want to search
    location_to_search = Hotel_name
    


    # Wait for the search input field to be ready
    search_box = driver.find_element("name", "q")
    search_box.send_keys(location_to_search)

    # Press Enter to initiate the search
    search_box.send_keys(Keys.RETURN)

    # Wait for a few seconds to let the results load
    time.sleep(5)
    current_url = driver.current_url
    #print("\n Current URL:", current_url)

    # Use regular expressions to extract latitude and longitude
    match = re.search( r'@(-?\d+\.\d+),(-?\d+\.\d+)', current_url )

    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        #print(f"Latitude: {latitude}, Longitude: {longitude}")

        # Latitude.append(latitude)
        # Longitude.append(longitude)
    else:
        print("Latitude and longitude not found in the URL.")
        latitude = 'Null'
        longitude = 'Null'

    # Close the browser window
    driver.quit()

    return  {'Hotel_name': Hotel_name,
                'Latitude': latitude,
                'Longitude': longitude,
                                }

    #return locations    
        

    # Create a DataFrame

    # df = pd.DataFrame([locations])
    # # # Save the DataFrame to a CSV file
    # df.to_csv('Bahirdar_location.csv',  mode='a', header=False, index=False)
    # print("CSV file saved successfully.")