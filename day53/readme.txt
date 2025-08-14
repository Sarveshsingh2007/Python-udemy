1. Scraping of Data

----Sends an HTTP GET request to the rental listings page (https://appbrewery.github.io/Zillow-Clone/).

----Uses BeautifulSoup to parse the HTML and extract:

----Property links

----Property addresses

----Prices

2. Clean Data

----Removes extra symbols and spaces from addresses.

----Cleans up price strings by removing /mo and any additional charges.

3. Fill Google Form

----Opens the Google Form using Selenium WebDriver.

----Automatically fills in:

----Address

----Price

----Property link

----Submits the form.