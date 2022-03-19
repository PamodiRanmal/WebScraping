#Task: Scraping data from the ikman.lk's vehicle section and retrieving data inside the ads also
#Contributor's Name: Ranmal Mendis

from bs4 import BeautifulSoup
import json
import requests
import time

start_time = time.time()

def ikman_vehicle_details(ad_list_type,NumberofPages):

    # The URLs which are going to be used for data scraping

    main_url = 'https://ikman.lk'
    page_url = 'https://ikman.lk/en/ads/sri-lanka/vehicles?sort=date&order=desc&buy_now=0&urgent=0&page='
    vehicle_section_url='https://ikman.lk/en/ads/sri-lanka/vehicles'


    def get_data(url):

        html_text = requests.get(vehicle_section_url).text

        soup = BeautifulSoup(html_text, 'lxml')

        # There are two types of ads. Top ads and normal ads. Here one fuction was defined for data
        # scraping from ikman.lk's vehicle section.For that function the class id of the list element was passed as the parameter.
        # Class ids of those two's list element were 'top-ads-container--1Jeoq gtm-top-ad'
        # and 'normal--2QYVk gtm-normal-ad' and 'top-ads-container--1Jeoq gtm-top-ad'

        # created a dictionary to store data

        vehicle = {}

        normal_ads=soup.find_all('li', class_=ad_list_type)

        for ad in normal_ads:

            #Assigning the retrieved values to the variables
            name= ad.find('h2',class_='heading--2eONR').text
            price= ad.find('div',class_='price--3SnqI color--t0tGX').text
            location= ad.find('div',class_='description--2-ez3').text.split(',')[0].replace(' ','')
            category= ad.find('div',class_='description--2-ez3').text.split(',')[1].replace(' ','')


            #Finding the new url to retrieve the data inside the add (the data we see after clicking on the ad)
            url_part=ad.find('a', href=True)
            url2=main_url+url_part['href']

            #Getting the description and posted date and time from that new url
            new_html_text = requests.get(url2).text
            new_soup = BeautifulSoup(new_html_text, 'lxml')
            #description = new_soup.find('div', class_='description--1nRbz').text
            posted_on= new_soup.find('span',class_='sub-title--37mkY').text.split(',')[0].split('Posted on ')[1]

            # posted_on='Not available'

            #Adding new data
            #with description
            #vehicle.update({'Name': name,'Price': price,'Description': description,'Location': location,'Category':category,'Mileage':'Not available','Posted on':posted_on})

            #without the description
            vehicle.update({'Name': name,'Price': price,'Location': location,'Category':category,'Mileage':'Not available','Posted on':posted_on})

            # Some ads are about spare parts and auto services. Those ads do not
            # have the attributes like mileage. By default the value of mileage is ''
            # mileage_and_year
            mileage_year = ad.find('div', class_='').text

            # To get the miliage from mileage from the vehicle ads
            if 'km' in mileage_year:
                vehicle['Mileage'] = mileage_year.split('km')[0]

            # if last_update != None and last_update!="":
            #     vehicle['Last update'] = last_update

            # print(vehicle)
            print(json.dumps(vehicle, indent=4))

            print('\n')


    if NumberofPages>=1:

        print("######### Ads from Page 1 ###########")
        get_data(main_url)

        count=2
        while count<=NumberofPages:
            print("######### Ads from Page "+str(count)+ " ###########")

            get_data(page_url+str(NumberofPages))
            count=count+1



#Calling the fuction to print the Top Ads
print("######### Top Ads ###########")
ikman_vehicle_details('top-ads-container--1Jeoq gtm-top-ad',1)

#Calling the fuction to print the Normal Ads
print("######### Normal Ads ############")
ikman_vehicle_details('normal--2QYVk gtm-normal-ad',1)

print("--- The total time for printing all the ads was %s seconds ---" % (time.time() - start_time))
