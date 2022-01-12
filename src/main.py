from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os

url = "https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php"

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path="/Users/bhagat/Downloads/chromedriver", options=options)

driver.get(url)
driver.get_screenshot_as_file("test.png")

html = driver.page_source

print(driver.title)

soup = BeautifulSoup(html);

alltables = soup('table');

maintable = alltables[1]

for mainbody in maintable.find_all('tbody'):
    trs = mainbody.find_all('tr');
    for tr in trs:
        tds = tr.find_all('td');
        for td in tds:
            print(td.text)
