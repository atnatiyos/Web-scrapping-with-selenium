from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from pathlib import Path
import os
from PIL import Image
from io import BytesIO
import pandas as pd
import random
from itertools import zip_longest
import place_finder
import math

# Hotel_info = pd.read_csv('Hotel_information.csv')
# Room_info = pd.read_csv('Room_information.csv')
# print(Hotel_info)
# print(Room_info)

url = {'addis ababa':"https://room.et/listing?r=60369c6407e629113f685af0",
       'adama':"https://room.et/listing?r=60369e8207e629113f685af4",
       'gonder':"https://room.et/listing?r=6036a9f507e629113f685b03",
       'bahirdar':"https://room.et/listing?r=6036a62e07e629113f685af9",
       'bishoftu':"https://room.et/listing?r=60369d2c07e629113f685af2",
       'hawassa':"https://room.et/listing?q=hawassa"}

# Set up the WebDriver
driver = webdriver.Chrome()
for key, value in url.items():
    driver.get(value)

    # Use WebDriverWait to wait for dynamic content to be present
    wait = WebDriverWait(driver, 1000)
    dynamic_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sc-jcVebW")))

    # Get the page source after JavaScript execution
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    div_elements = soup.find_all('div', class_='sc-jcVebW dsYtgE')
    location_elements = soup.find_all('div', class_='sc-citwmv')

    # div_elements = soup.find_all('div', class_='sc-jcVebW dsYtgE')
    print(len(div_elements),len(location_elements))
    # Loop through all elements

    count = 0 
    for div_element, location_element in zip_longest(div_elements, location_elements, fillvalue=None):
        # Check if either element is None (e.g., if lists have different lengths)
        if div_element is None or location_element is None:
            continue
        count =  count  + 1
        print(count)
        # Extract the text within the anchor element
        hotel_name = div_element.a.text.strip()

        Hotel_location = location_element.text.strip()
        location_parts = Hotel_location.split("፣")
    

        # Extract the href attribute
        href_attribute = div_element.a['href']

        print("Hotel Name: ", hotel_name)
        print('City: ',key)
        print("Hotel_location: ", location_parts[0][1:])
        print("Href Attribute: ", href_attribute)
       
        location = place_finder.location(hotel_name+" "+key)
        


        directory_name =  "./Images/"+str(hotel_name)+"_"+str(key)        

        # Create the directory to store the images
        if not os.path.exists(directory_name):
            # Create the directory if it doesn't exist
            os.mkdir(directory_name)

   
        Hotel_data = {'Hotel_name': hotel_name,
                    'City_location': key,
                    'Net_point': str(location_parts[0][1:]),
                    'Hotel_image_path': "NA",
                    'Latitude':location["Latitude"],
                    'Longitude':location["Longitude"]
                    }
        
      
        df = pd.DataFrame([Hotel_data])
        # # Save the DataFrame to a CSV file
        df.to_csv('Hotel_data.csv',  mode='a', header=False, index=False)
        print("CSV file saved successfully.")
        
        
    
        #### now scrap room information
        url = "https://room.et" + str(href_attribute)

        # Set up the WebDriver for the detail page
        driver_detail = webdriver.Chrome()
        driver_detail.get(url)

        # Use WebDriverWait to wait for dynamic content to be present
        wait_detail = WebDriverWait(driver_detail, 1000)
        dynamic_element_detail = wait_detail.until(EC.presence_of_element_located((By.CLASS_NAME, "sc-jcVebW")))

        # Get the page source after JavaScript execution
        page_source_detail = driver_detail.page_source

        # Parse the page source with BeautifulSoup for the detail page
        soup_detail = BeautifulSoup(page_source_detail, "html.parser")

        # Find all image elements with class 'absolute'
        image_elements_detail = soup_detail.find_all('img', class_='absolute')

        # Loop through all image elements on the detail page
        for image_element_detail in image_elements_detail:
            # Extract the 'src' attribute of the image
            image_src = image_element_detail.get('src')
            print("Image Source:", image_src)
            response = requests.get(image_src)

            with open(directory_name +'/'+ str(hotel_name)+'.jpg', 'wb') as f:
                f.write(response.content)

        image_elements_room = soup_detail.find_all('div', class_='sc-jJEJSO')
    
        hotel_names = []
        image_url = []
        # room_number = []
        Room_type = []
        room_prices = []
        for element in image_elements_room:
            room_name_element = element.find('a', class_='sc-dlfnbm')
            hotel_names.append(hotel_name)
            image_url.append('Na')
            #room_number.append(random.randint(5, 30))
            print(hotel_names)
        
            try:
            
                Room_type.append(room_name_element.text.strip())
                print("Room Name:", Room_type)
           
            except:
                print("Room Name:", room_name_element)
    
            room_price = element.find_all('div', class_='sc-bZSQDF')
        
        
            try:
                room_price_element = element.find('div', class_='sc-bZSQDF')
                hotel_room_price = room_price_element.text.strip().split()[0] if room_price_element else None
                room_prices.append(abs(int(room_price_element.b.text.strip())))
                print("Room Price:", room_prices)
            except:
                print("Room price:", room_price)
       
            # if folder not existed create one
            Image_download_starts = 1
            if not os.path.exists(directory_name +'/'+ str(room_name_element.text.strip())):
                Image_download_starts = 0
                os.mkdir(directory_name +'/'+ str(room_name_element.text.strip()))

            image_elements = element.find_all('div', class_='react-multi-carousel-list')

            for image_element in image_elements:
                ui_elements = image_element.find_all('ul', class_='react-multi-carousel-track')

                for ui_element in ui_elements:
                    li_elements = ui_element.find_all('li', class_='react-multi-carousel-item')
                
                    image_counter = Image_download_starts
                    for li_element in li_elements:
                        if image_counter == 1:
                            image_counter = image_counter + 1
                            continue

                        print("#####################")

                        #image_src = li_element.get('src')
                        image_src = li_element.find('img')
                        print("Image Source:", image_src['src'])
                        response = requests.get(image_src['src'])

                        with open(directory_name +'/'+ str(room_name_element.text.strip())+ "/" + str(room_name_element.text.strip()) +"_"+ str(image_counter)+'.jpg', 'wb') as f:
                            f.write(response.content)
                        image_counter = image_counter + 1

                    # if image_counter == 4:
                    #     break
    
        data = {'Hotel_name': hotel_names,
                'Room_type': Room_type,
                'Room_price': room_prices,
                'Room_image': image_url,
                #'Room_number': room_number
                }
        
        # Create a DataFrame
        df = pd.DataFrame(data)

        # Save the DataFrame to a CSV file
        df.to_csv('Room_data Adama.csv',  mode='a', header=False, index=False)
        print( "CSV file saved successfully.")

        hotel_names.clear()
        image_url.clear()
        #room_number.clear()
        Room_type.clear()
        room_prices.clear()    


    # Close the browser for the detail page
    driver_detail.quit()
    
    
    

# Close the main browser
driver.quit()
