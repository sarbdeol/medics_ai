from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
def get_forex(url):
    # Set up Selenium
    options = Options()
    # options.headless = True
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    # service = Service()  # Replace with the path to your chromedriver executable
    driver = webdriver.Chrome(options=options)

    # URL of the page containing the dynamic content
    # url = "https://www.monito.com/en/compare/transfer/us/india/usd/inr/1"

    # Load the page
    driver.get(url)

    # Wait for the content to load (adjust the sleep time as needed)
    time.sleep(6)

    # Get the page source after content loaded
    html_content = driver.page_source

    # Quit the driver
    driver.quit()

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize an empty list to store the data
    all_data = []

    # Find all relevant elements
    boxes = soup.find_all('div', class_='box-container')
    print(len(boxes))
    # Iterate through each box
    count=1
    for box in boxes:
        print(count)
        if box.find('img'):
            platform_name = box.find('img')['alt']
            print(platform_name)
            exchange_price = box.find('div', class_='mt-1').find('p').text.strip()
            print(exchange_price)
            if box.find('strong', class_='uppercase text-green-800'):
                fee = box.find('strong', class_='uppercase text-green-800').text.strip()
            else:
                fee = box.find('strong', class_='text-gray-700').text.strip()
            print(fee)
            # Create dictionary for the current box
            box_data = {
                'platform_name': platform_name,
                'exchange_price': exchange_price,
                'fee': fee
            }
            
            # Append box data to the list
            all_data.append(box_data)
            count+=1
    # Write the data to a JSON file
    with open('forex.json', 'w') as f:
        json.dump(all_data, f, indent=4)

    print("Data written to data.json")
    return all_data

# get_forex(url = "https://www.monito.com/en/compare/transfer/United-States/India/USD/INR/1")