#Task: Scraping data from the ikman.lk's vehicle section and retrieving data inside the ads also
#Contributor's Name: Ranmal Mendis

from bs4 import BeautifulSoup
import json

import requests

#The URL which was going to be used for data scraping
html_text=requests.get('https://ikman.lk/en/ads/sri-lanka/vehicles').text

soup =BeautifulSoup(html_text,'lxml')

#There are two types of ads. Top ads and normal ads. Here one fuction was defined for data
#scraping from ikman.lk's vehicle section.For that function the class id of the list element was passed as the parameter.
#Class ids of those two's list element were 'top-ads-container--1Jeoq gtm-top-ad'
#and 'normal--2QYVk gtm-normal-ad' and 'top-ads-container--1Jeoq gtm-top-ad'

def ikman_vehicle_details(ad_list_type):

    normal_ads=soup.find_all('li', class_=ad_list_type)

    for ad in normal_ads:
        #Some ads were related are about spare parts and auto services. Those ads do not
        #have the attributes like mileage. By default the value of mileage is ''
        mileage = ''
        last_update=''
        #mileage_and_year
        mileage_year= ad.find('div',class_='').text

        #To get the miliage from mileage from the vehicle ads
        if 'km' in mileage_year:
            mileage=mileage_year.split('km')[0]
        #Assigning the retrieved values to the variables
        name= ad.find('h2',class_='heading--2eONR').text
        price= ad.find('div',class_='price--3SnqI color--t0tGX').text
        location= ad.find('div',class_='description--2-ez3').text.split(',')[0].replace(' ','')
        category= ad.find('div',class_='description--2-ez3').text.split(',')[1].replace(' ','')
        last_update= ad.find('div',class_='updated-time--1DbCk')


        #Finding the new url to retrieve the data inside the add (the data we see after clicking on the ad)
        link1=ad.find('a', href=True)
        link2='https://ikman.lk'+link1['href']

        #Getting the description from that new url
        new_html_text = requests.get(link2).text
        new_soup = BeautifulSoup(new_html_text, 'lxml')
        description = new_soup.find('div', class_='description--1nRbz').text

        print('Name :'+name)
        print('Price :'+price)
        print('Location :'+location)
        print('Category :'+category)

        if mileage!="":
            print('miledge :'+ mileage)

        print('description:'+description)

        if last_update != None:
            print('Last Update :' + last_update.text)

        print('\n')
#Calling the fuction to print the Top Ads
ikman_vehicle_details('top-ads-container--1Jeoq gtm-top-ad')

#Calling the fuction to print the Normal Ads
ikman_vehicle_details('normal--2QYVk gtm-normal-ad')
