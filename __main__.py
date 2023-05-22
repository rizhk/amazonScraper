from bs4 import BeautifulSoup
import requests
from selenium import webdriver
# Set path to chromedriver executable
from selenium.webdriver.common.by import By

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = '/usr/local/bin/chromedriver'
# driver = webdriver.Chrome(executable_path=chromedriver_path)
from webdriver_manager.chrome import ChromeDriverManager
LINK = 'https://www.amazon.com/Android-Tablet-Keyboard-Processor-Version/dp/B09SHJLMTD/ref=sr_1_1_sspa?qid=1684408490&s=computers-intl-ship&sr=1-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyS1ZKSlEyRFhBUURHJmVuY3J5cHRlZElkPUEwNzU2MTU1M1lTN0ZDVURCSU1VJmVuY3J5cHRlZEFkSWQ9QTA2NTc2OTcyWTVUNUU0QlFMTkdTJndpZGdldE5hbWU9c3BfYXRmX2Jyb3dzZSZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1'
NOT_FOUND = 'NOT FOUND'
# Create a new instance of the Chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install())
from selenium.webdriver.chrome.options import Options


if __name__ == '__main__':
    # page = requests.get(LINK, headers=HEADERS)
    # beautifulSoap = BeautifulSoup(page.content, 'html.parser')
    #print(page.content)
    # for attributeName in attributeList.keys():
    #     htmlValue = get_html_element_value(attributeName, attributeList[attributeName], beautifulSoap)
    #     print(htmlValue)

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Load the webpage
    url = LINK
    driver.get(url)

    # Perform scraping operations using Selenium
    # For example, extract the product title and price
    title_element = driver.find_element(By.ID, "productTitle")
    title = title_element.text.strip()

    whole_price = driver.find_element(By.CSS_SELECTOR,".a-price-whole")
    decimal_price = driver.find_element(By.CSS_SELECTOR,".a-price-fraction")
    price = whole_price + '.' +  decimal_price

    globalFeatureParent = driver.find_element(By.ID, "amazonGlobal_feature_div")
    freeShipping = globalFeatureParent.find_element(By.CSS_SELECTOR, ".a-size-base.a-color-secondary")
    freeShipping = freeShipping.text.strip() if freeShipping else NOT_FOUND

    whole_price = whole_price.text.strip() if whole_price else NOT_FOUND
    decimal_price = decimal_price.text.strip() if decimal_price else NOT_FOUND


    variation_size_name = driver.find_element(By.ID, "variation_size_name")
    variation_size_name_row = variation_size_name.find_element(By.CSS_SELECTOR,".a-row")
    variation_size_name_row_style = variation_size_name_row.find_element(By.CSS_SELECTOR,".selection")

    variation_color_name = driver.find_element(By.ID, "variation_color_name")
    variation_size_name_row = variation_color_name.find_element(By.CSS_SELECTOR,".a-row")
    variation_color_name_row_color = variation_size_name_row.find_element(By.CSS_SELECTOR,".selection")
    
    # remove all html tags and return text only
    


    # Print the scraped data
    print("Title:", title)
    print("Price:", price)
    print("freeShipping:", freeShipping)
    print("size:", variation_size_name_row_style)
    print("color:", variation_color_name_row_color)
    # Close the browser
    driver.quit()


