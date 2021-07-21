from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import lxml

# Paths for data
zillow_url = "https://www.zillow.com/houston-tx/rentals/1-_beds/1.0-_baths/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Houston%2C%20TX%22%2C%22mapBounds%22%3A%7B%22west%22%3A-96.22772274414064%2C%22east%22%3A-94.62097225585939%2C%22south%22%3A29.31952945558563%2C%22north%22%3A30.313219325039206%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A39051%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22ldog%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A1400%7D%2C%22price%22%3A%7B%22max%22%3A428168%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%2C%22lau%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D"
google_forms_link = "https://docs.google.com/forms/d/e/1FAIpQLScF6dxrEU4fzC9xuzzN-afGOL9Jbs_2Cn9i59PeuUoKIsNu5w/viewform?usp=sf_link"

# Set up selenium
chrome_driver_path = "C:\Development\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)
driver.get(google_forms_link)

# BeautifulSoup setup
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
response = requests.get(zillow_url, headers=headers)
soup = BeautifulSoup(response.content, 'lxml')

# Grab address data for each listing
address_data = [address.text for address in soup.find_all(name='address', class_='list-card-addr')]

# Grab price data for each listing
price_data = [price.text.split('+')[0] for price in soup.find_all(name='div', class_='list-card-price')]

# Grab links to go to the zillow webpage for each apartment
zillow_link_data = ['zillow.com'+link['href'] for link in soup.find_all(name='a', class_='list-card-link', href=True)]

# Fill in google forms data
for i in range(len(address_data)):
    address_answer = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_answer.send_keys(address_data[i])

    price_answer= driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_answer.send_keys(price_data[i])

    link_answer = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_answer.send_keys(zillow_link_data[i])

    submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    submit.click()

    next_entry = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_entry.click()