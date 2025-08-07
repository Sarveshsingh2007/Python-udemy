from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.amazon.in/dp/B0CS5Z3T4M?pd_rd_w=ibrne&content-id=amzn1.sym.549217d3-6a57-4717-99fc-ebf9174ad2f1&pf_rd_p=549217d3-6a57-4717-99fc-ebf9174ad2f1&pf_rd_r=JCM9D9EENV95E2HADSYR&pd_rd_wg=wqfDy&pd_rd_r=2d3f5348-6ef4-4892-9721-cbed18552296")

product_name = driver.find_element(By.CLASS_NAME, value="a-text-bold")
print(product_name.text)
other_seller_detail = driver.find_element(By.CLASS_NAME, "daodi-header-font")
print(other_seller_detail.text)


driver.quit()
