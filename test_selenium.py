#http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://www.nytimes.com")
headlines = driver.find_elements_by_class_name("story-heading")
for headline in headlines:
    print(headline.text.strip())
