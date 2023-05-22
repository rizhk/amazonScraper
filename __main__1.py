from bs4 import BeautifulSoup
import requests
from selenium import webdriver
# Set path to chromedriver executable
chromedriver_path = '/usr/local/bin/chromedriver'
# driver = webdriver.Chrome(executable_path=chromedriver_path)
from webdriver_manager.chrome import ChromeDriverManager

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install())
from selenium.webdriver.chrome.options import Options

NOT_FOUND = 'NOT FOUND'
LINK = 'https://www.amazon.com/Android-Tablet-Keyboard-Processor-Version/dp/B09SHJLMTD/ref=sr_1_1_sspa?qid=1684408490&s=computers-intl-ship&sr=1-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyS1ZKSlEyRFhBUURHJmVuY3J5cHRlZElkPUEwNzU2MTU1M1lTN0ZDVURCSU1VJmVuY3J5cHRlZEFkSWQ9QTA2NTc2OTcyWTVUNUU0QlFMTkdTJndpZGdldE5hbWU9c3BfYXRmX2Jyb3dzZSZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1'
# Headers for request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
}

attributeList = {
    # 'title': [
    #     {'id': 'productTitle'}
    # ],
    'price': [
        {'class': 'a-section a-spacing-none aok-align-center'},
        {'class': 'a-offscreen'}
    ],
    'customerReview': [
        {'id': 'averageCustomerReviews'}, 
        {'class': 'a-size-base a-color-base'}
    ],
}


def get_html_element_value(attributeName, classes, beautifulSoap):
    try:
        # Find the initial element based on the first class or id
        if 'class' in classes[0]:
            html_element = beautifulSoap.find(class_="a-section a-spacing-none aok-align-center")
        else:
            html_element = beautifulSoap.find(id=classes[0]['id'])

        html_element_value = html_element if len(classes) > 1 else html_element.get_text().strip()

        # Check if a second class or id is provided
        if len(classes) > 1:
            field_accessor = 'class' if 'class' in classes[1] else 'id'
            if (field_accessor == id):
                nested_elements = html_element.find_all(id=classes[1]['id'], recursive=True)
            else:
                nested_elements = html_element.find_all(class_=classes[1]['class'], recursive=True)
            
            for nested_element in nested_elements:
                if classes[1][field_accessor] in nested_element.get(field_accessor, []):
                    html_element_value = nested_element.get_text().strip()
                    break
    except Exception as e:
        html_element_value = attributeName + ' ' + 'NOT_FOUND'
    
    return html_element_value


def getTitle(beautifulSoap):
    try:
        title = beautifulSoap.find(id="productTitle").get_text().strip()
    except:
        title = NOT_FOUND
    return title

def getPrice(beautifulSoap):
    try:
        price = beautifulSoap.find(class_="a-section a-spacing-none aok-align-center").get_text().strip()
    except:
        price = NOT_FOUND
    return price

def getCustomerReview(beautifulSoap):
    try:
        customerReview = beautifulSoap.find(id="averageCustomerReviews").get_text().strip()
    except:
        customerReview = NOT_FOUND
    return customerReview





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
    title_element = driver.find_element_by_id("productTitle")
    price_element = driver.find_element_by_class_name("a-offscreen")

    title = title_element.text.strip()
    price = price_element.text.strip()

    # Print the scraped data
    print("Title:", title)
    print("Price:", price)

    # Close the browser
    driver.quit()


