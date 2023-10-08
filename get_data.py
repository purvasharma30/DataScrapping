from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Replace with the actual Excel file path and column name
excel_file = r'/Users/chiya/Downloads/shopify_app_links.xlsx'
url_column_name = 'WebsiteColumn'

# Read Excel sheet and extract URLs
data = pd.read_excel(excel_file)
urls = data[url_column_name]

# Initialize Chrome options and WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--incognito')  # Run Chrome in incognito mode
driver = webdriver.Chrome(options=chrome_options)

# Initialize lists to store scraped data
categories = []
websites = []

# Loop through the URLs
for url in urls:
    driver.get(url)

    try:
        # Initialize variables for each category of data
        app_category = 'N/A'  # Use a different variable name
        website = url

        # Extract App Name
        categories_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="adp-details-section"]/div/div/div[1]/div[2]/div/div[3]/span/a'))
        )
        app_category = categories_element.text

    except Exception as e:
        print(f"An error occurred while scraping app data {url}: {e}")

    # Append data to lists
    categories.append(app_category)  # Use the correct variable
    websites.append(website)

    # Save scraped data to a new Excel file periodically
    if len(categories) % 3 == 0:  # Save every 10 entries
        scraped_data = pd.DataFrame({
            'Category': categories,
            'Website': websites
        })
        scraped_data.to_excel('scraped_data_partial.xlsx', index=False)

# Save the final scraped data to a new Excel file
scraped_data = pd.DataFrame({
    'Category': categories,
    'Website': websites
})
scraped_data.to_excel('scraped_data_final.xlsx', index=False)

# Close the WebDriver
driver.quit()
