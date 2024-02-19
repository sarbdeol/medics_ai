from bs4 import BeautifulSoup
from selenium import webdriver
def google_search(find):
    url = f"https://www.google.com/search?q={find}"

    # Set up the browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode, without opening a browser window
    driver = webdriver.Chrome(options=options)

    # Fetch the page
    driver.get(url)

    # Wait for the page to load completely (you may need to adjust the sleep time based on your internet speed)
    import time
    time.sleep(2)  # Wait for 2 seconds, adjust if necessary

    # Extract the HTML content after JavaScript execution
    html = driver.page_source

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find the price span
    data_div = soup.find("div", class_="wGt0Bc")
    data = data_div.text if data_div else "data not found"

    print("data:", data)

    # Close the browser
    driver.quit()
    return data
