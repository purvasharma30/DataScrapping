from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Initialize Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--incognito')  # Run Chrome in incognito mode

# Initialize the WebDriver with Chrome options
driver = webdriver.Chrome(options=chrome_options)

# Set the base URL of the Shopify App Store search page
base_url = "https://apps.shopify.com/search?q=x&sort_by=newest&page={}"

# Number of pages to scrape
num_pages = 8  # Change this to the number of pages you want to scrape

# Create an empty list to store all the app links
app_links = []

# Loop through the specified number of pages
for page_num in range(1, num_pages + 1):
    # Construct the URL for the current page
    url = base_url.format(page_num)
    
    # Open the URL
    driver.get(url)
    
    # Scroll to the bottom of the page to load more apps, scrolling step by step
    scroll_height = 0
    while True:
        # Scroll down a little bit
        driver.execute_script("window.scrollTo(0, {});".format(scroll_height))
        
        # Wait for a short delay (adjust as needed)
        time.sleep(1)
        
        # Increase the scroll height
        scroll_height += 300  # Adjust the scroll amount as needed
        
        # Check if we have reached the bottom of the page
        if scroll_height >= driver.execute_script("return document.body.scrollHeight;"):
            break
    
    # Find all app links on the page and extract the href attribute
    app_links_on_page = driver.find_elements(By.XPATH, "//div[contains(@class, 'tw-text-heading-6')]//a")
    for link in app_links_on_page:
        app_links.append(link.get_attribute("href"))

# Close the WebDriver
driver.quit()

# Create a pandas DataFrame from the collected links
df = pd.DataFrame({"App Links": app_links})

# Save all the app links to an Excel file
df.to_excel("shopify_app_links1.xlsx", index=False)

print(f"Total {len(app_links)} links saved to 'shopify_app_links1.xlsx'")
