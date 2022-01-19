from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from os.path import exists
import pandas as pd
import os
import csv
import shutil

def scrapeStocks(targetUrl,screenshotName):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.headless = True
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
    driver = webdriver.Chrome(service=Service('/Users/bhagat/Downloads/chromedriver'), options=options)

    print("==================Requested target URL "+targetUrl+" ==================")
    print("==================Waiting For Response==================")
    driver.get(targetUrl)
    print("==================Taking Screenshot For "+screenshotName+" ==================")
    driver.get_screenshot_as_file(screenshotName + ".png")

    html = driver.page_source

    soup = BeautifulSoup(html);

    alltables = soup('table');

    maintable = alltables[1]
    
    row = []

    print("==================Scraping Table For "+screenshotName+" ==================")
    for mainbody in maintable.find_all('tbody'):
        trs = mainbody.find_all('tr');
        for tr in trs:
            tds = tr.find_all('td');
            row.clear()
            for td in tds:
                if td.find("a") is not None and 'title' in td.find("a").attrs:
                    row.append(td.find("a").string)
                    #print(td.find("a").string)
                elif td.has_attr('width') is True and td.has_attr('align') is True and td.div is None and td.has_attr('class') is False:
                    row.append(td.text)
                    #print(td.text)
                elif td.has_attr('width') is True and td.has_attr('align') is True and td.div is None and td.has_attr('style') is False:
                    #num = td.text
                    #print(num.replace(",",""))
                    row.append(float(td.text))
                    #print(td.text)
            if row:
                writer.writerow(row)
                #print(row)
    
print("==================Started==================")

currentStocksListFilePath = "currentStocksList.csv"

previousStocksListFilePath = "previousStocksList.csv"

isFileExists = exists(currentStocksListFilePath)

if isFileExists is True:
    try:
        #shutil.copyfile(currentStocksListFilePath,previousStocksListFilePath)
        print("==================File copied successfully==================")
 
    except shutil.SameFileError:
        print("==================Source and destination represents the same file==================")

    except IsADirectoryError:
        print("==================Destination is a directory.")

    except PermissionError:
        print("==================Permission denied==================")

    except:
        print("==================Error occurred while copying file==================")

file = open(currentStocksListFilePath, 'w')

writer = csv.writer(file)

header = ['Company Name','High','Low','Last Price','Prev Close','Change','% Gain']

writer.writerow(header)

scrapeStocks('https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php','nsegainer')

scrapeStocks('https://www.moneycontrol.com/stocks/marketstats/nseloser/index.php','nseloser')

file.close()

if isFileExists is False:
    print("\n\n================================ No Previous Stock List present (Run again)================================\n\n")
else:  
    dfCurrentStocksList = pd.read_csv(currentStocksListFilePath)
    dfPreviousStocksList = pd.read_csv(previousStocksListFilePath)
    gainLostSinceLastRun = []
    for index, row in dfCurrentStocksList.iterrows():
        oldStockInfo = dfPreviousStocksList[dfPreviousStocksList['Company Name'] == row['Company Name']]
        if oldStockInfo.empty:
            gainLostSinceLastRun.append('New Entrant')
        else:
            for element in oldStockInfo['Last Price']:
                gainLostSinceLastRun.append( ( ( float(row['Last Price'].replace(',','')) - float(element.replace(',','')) ) / float(row['Last Price'].replace(',','')) ) * 100  )
    dfCurrentStocksList['% Gain/lost since last run'] = gainLostSinceLastRun
    print("\n\n==================Previous Stock List==================")
    previousStocksList = dfPreviousStocksList.style.set_caption("Previous stocks list")\
    .set_table_styles([{
         'selector': 'caption',
         'props': 'caption-side: bottom; font-size:1.25em;'
     }], overwrite=False)
    display(previousStocksList)
    print("\n\n==================Current Stock List==================")
    currentStocksList = dfCurrentStocksList.style.set_caption("Present stocks list")\
    .set_table_styles([{
         'selector': 'caption',
         'props': 'caption-side: bottom; font-size:1.25em;'
     }], overwrite=False)\
    .applymap(lambda x: "background-color:cyan;" if type(x) == str and x == "New Entrant" else "background-color:red;" if float(x) < 0.0 else "background-color:white;" if float(x) == 0.0 else "background-color:green;",subset=["% Gain/lost since last run"])
    display(currentStocksList)
    
print("==================Ended==================")   
    
