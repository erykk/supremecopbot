from selenium import webdriver
from bs4 import BeautifulSoup
import pycurl
import requests
import time
from io import BytesIO


keys = {
    "fullName" : "test test",
    "email" : "email@gmail.com",
    "tel" : "0000000",
    "address" : "1 Main st",
    "city": "here",
    "postcode" : "1234",
    "visanum" : "0101010",
    "cvv": "009"
}

what_sizes = {
    "small": False,
    "medium" : True,
    "large": True,
    "xlarge": False
}

FIND_HATS = False

urlStem="https://www.supremenewyork.com"

#Add size selection
#Add threading

def check_available_sizes(elements):

    sizes = {
    "small": False,
    "medium" : False,
    "large": False,
    "xlarge": False
}
    i = 1
    for element in elements:
        sizes[str(element.text).lower()] = i
        i += 1
    return sizes
    


def shop(url):
    browser = webdriver.Chrome("./chromedriver")
    browser.get(urlStem + url)
    #size
    size_dropdown = browser.find_element_by_id("size")
    size_elements = size_dropdown.find_elements_by_css_selector("*")

    available_sizes = check_available_sizes(size_elements)

    #ascending order of preference

    if what_sizes.get("medium") != False and available_sizes.get("medium") != False:
        browser.find_element_by_xpath('//*[@id="size"]/option[' + str(available_sizes.get('medium')) + ']').click()

    if what_sizes.get("large") != False and available_sizes.get("large") != False:
        browser.find_element_by_xpath('//*[@id="size"]/option[' + str(available_sizes.get('large')) + ']').click()

    if what_sizes.get("xlarge") != False and available_sizes.get("xlarge") != False:
        browser.find_element_by_xpath('//*[@id="size"]/option[' + str(available_sizes.get('xlarge')) + ']').click()
    
    if what_sizes.get("small") != False and available_sizes.get("small") != False:
        browser.find_element_by_xpath('//*[@id="size"]/option[' + str(available_sizes.get('small')) + ']').click()    

    browser.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()
    time.sleep(0.3)
    
    browser.find_element_by_xpath('//*[@id="cart"]/a[2]').click()
    browser.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(keys["fullName"])
    browser.find_element_by_xpath('//*[@id="order_email"]').send_keys(keys["email"])
    browser.find_element_by_xpath('//*[@id="order_tel"]').send_keys(keys["tel"])
    browser.find_element_by_xpath('//*[@id="bo"]').send_keys(keys["address"])
    browser.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(keys["city"])
    browser.find_element_by_xpath('//*[@id="order_billing_country"]/option[18]').click()
    browser.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(keys["postcode"])
    browser.find_element_by_xpath('//*[@id="credit_card_type"]/option[1]').click()
    browser.find_element_by_xpath('//*[@id="cnb"]').send_keys(keys["visanum"])
    # May = 5
    browser.find_element_by_xpath('//*[@id="credit_card_month"]/option[5]').click()
    #2020 = 0, 2025 = 6
    browser.find_element_by_xpath('//*[@id="credit_card_year"]/option[6]').click()
    browser.find_element_by_xpath('//*[@id="vval"]').send_keys(keys["cvv"])
    browser.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p/label/div/ins').click()
    # PAY
    #browser.find_element_by_xpath('//*[@id="pay"]/input').click()
    time.sleep(10)
    

def scrape(url):
    articles = {}
    #request = requests.get(url,timeout=5)
    b_obj = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, b_obj)
    c.perform() 
    c.close()
    get_body = b_obj.getvalue()
    pageContent = BeautifulSoup(get_body.decode('utf-8'),"html.parser")
    mainContainer = pageContent.find(id="container")
    for article in mainContainer:
        link = article.find('a',href=True)['href']
        articleDetails = find_article_details(article,link)
        articles[articleDetails["name"]] = {"colour" : articleDetails["colour"], "url" : articleDetails["url"]}
        if FIND_HATS == False and is_hat(link):
            break
    for name, details in articles.items():
        print(name, details["colour"], details["url"])

    return articles

def is_hat(link):
    if "/hats/" in link:
        return True
    else:
        return False

        
def find_article_details(article,link):
    articleDetails = {}
    request = requests.get(urlStem+link)
    pageContent = BeautifulSoup(request.content,"html.parser")
    articleName = pageContent.find(attrs={"itemprop": "name"}).text.strip()
    print(articleName)
    articleStyle = pageContent.find('ul',{"class":"styles"})
    selectedArticle = articleStyle.find('a', {"class": "selected"})
    articleColour = selectedArticle['data-style-name'] 
    articleUrl = selectedArticle['href']
    articleDetails["name"] = articleName + '(' + articleColour + ')'
    articleDetails["colour"] = articleColour
    articleDetails["url"] = articleUrl
    return articleDetails

def find(url,string):
    articles = scrape(url)
    return articles.get(string)["url"]
    


if __name__ == "__main__":
    url = "https://www.supremenewyork.com/shop/all"
    string="Wool Suit(Black Pinstripe)"
    itemUrl = find(url,string)
    #itemUrl = "/shop/shirts/s3o9qd7fz/suabzps94"
    shop(itemUrl)


