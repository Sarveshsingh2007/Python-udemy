from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_optionns = webdriver.ChromeOptions()
chrome_optionns.add_experimental_option("detach", True)

driver = webdriver.Chrome(chrome_optionns)
driver.get("https://secure-retreat-92358.herokuapp.com/")

first_name = driver.find_element(By.NAME, value="fName")
first_name.send_keys("Sarvesh", Keys.ENTER)

last_name = driver.find_element(By.NAME, value="lName")
last_name.send_keys("Adhikari", Keys.ENTER)

email = driver.find_element(By.NAME, value="email")
email.send_keys("sarvehsinghadhikari@gmail.com", Keys.ENTER)


sign_up = driver.find_element(By.CSS_SELECTOR, "form button")
last_name.click()
