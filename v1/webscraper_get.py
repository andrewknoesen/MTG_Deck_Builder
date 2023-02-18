# # Import the required libraries
# from selenium import webdriver
# from bs4 import BeautifulSoup

# # Create a new instance of the Chrome web driver
# driver = webdriver.Chrome()

# # Use the web driver to load the webpage
# driver.get("https://moxmonolith.com/?cardId=1968&cardName=Stomping%20Ground")

# # Wait for the JavaScript on the page to load
# driver.implicitly_wait(20)

# # Get the HTML source of the page
# html_source = driver.page_source

# # Use BeautifulSoup to parse the HTML source
# soup = BeautifulSoup(html_source, "html.parser")

# # Find all script tags in the HTML source
# scripts = soup.find_all("script")

# # Loop through the script tags
# for script in scripts:
#     # Get the src attribute of the script tag
#     src = script.get("src")

#     # Check if the src attribute is a GET request
#     if src and src.startswith("http") and src.lower().startswith("get"):
#         # Print the GET request URL
#         print(src)

# # Close the web driver
# driver.close()
from selenium import webdriver
from selenium.webdriver.common.by import By

# Replace with the URL of the webpage you want to analyze
url = "https://moxmonolith.com/?cardId=1968&cardName=Stomping%20Ground"

# Create a new instance of the Chrome web driver
driver = webdriver.Chrome()

# Load the webpage and wait for it to finish loading
driver.get(url)
driver.implicitly_wait(10)

# Find all 'script' elements on the page
scripts = driver.find_elements(By.TAG_NAME, "script")

# Print the URLs that are called by the scripts on the page
for script in scripts:
    if '/js/' in str(script.get_attribute("src")):
        js = script.get_attribute("src")
        print(js)
        # driver.execute_script(js)
