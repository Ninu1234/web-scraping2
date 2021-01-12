from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
starturl = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome('/Users/Poonam/OneDrive/Desktop/My Python/chromedriver')
browser.get(starturl)
time.sleep(10)
headers = ['name','light_years_from_earth','planet_mass','stellar_magnitude','discovery_date','hyperlink','planet_type','planet_radius','orbital_radius','orbital_period','eccentricity']
planetdata = []
newplanetdata = []
def scrape():
    for i in range(1,433):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,'html.parser')
            currentpagenumber = int(soup.find_all('input',attrs = ['class','page_num'])[0].get('value'))
            if currentpagenumber<i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentpagenumber>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        for ul_tag in soup.find_all('ul',attrs = {'class','exoplanet'}):
            li_tags = ul_tag.find_all('li')
            templist = []
            for index,li_tag in enumerate(li_tags):
                if index == 0:
                    templist.append(li_tag.find_all('a')[0].contents[0])
                else:
                    try:
                        templist.append(li_tag.contents[0])
                    except:
                        templist.append('')
            hyperlinktag = li_tags[0]
            templist.append('https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'+hyperlinktag.find_all('a',href = True)[0]['href'])
            planetdata.append(templist)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f'{i}pagedone')
def scrapemoredata(hyperlink):
    try:
        page = request.get(hyperlink)
        soup = BeautifulSoup(page.content,'html.parser')
        templist = []
        for tr_tag in soup.find_all('tr',attrs = {'class':'fact_row'}):
            td_tags = tr_tag.find_all('td')
            for td_tag in td_tags:
                try:
                    templist.append(td_tag.find_all('div',attrs = {'class':'value'})[0].contents[0])
                except:
                    templist.append('')
        newplanetdata.append(templist)
    except:
        time.sleep(1)
        scrapemoredata(hyperlink)
scrape()
for index,data in enumerate(planetdata):
    scrapemoredata(data[5])
    print(f'{index+1}pagedone2')
finalplanetdata = []
for index,data in enumerate(planetdata):
    newplanetdataelement = newplanetdata[index]
    newplanetdataelement = [elem.replace('\n','')for elem in newplanetdataelement]
    newplanetdataelement = newplanetdataelement[:7]
    finalplanetdata.append(data+newplanetdataelement)
with open('final2.csv','w') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(finalplanetdata)