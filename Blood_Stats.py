import os
import datetime
import statistics
from getpass import getpass
from collections import Counter

import requests
import re
from bs4 import BeautifulSoup
from gmplot import gmplot

# Asks for inputs to get the user's API key if they have one
while True:
    api = input("Do you have a google maps API key (y/n): ")
    if api == 'y':
        api = input("Please input your google maps API key: ")
        api_flag = True
        break
    elif api == 'n':
        print("This just means the map produced will be watermarked.")
        api_flag = False
        break
    else:
        print("Please answer with 'y' or 'n'")

# URLS used for this script
URL = 'https://my.blood.co.uk/'
URL_LOGIN = 'Account/Login'
URL_SIGNIN = 'Account/SignIn'
URL_SCRAPE = 'Home/Landing?load=Yourdonations'

# Creates a session which can be used to get cookies and log in
s = requests.Session()

# Requests the user's email and password.
email = input("Please enter your email: ")
password = getpass("Please enter your password: ")

# Connects to SignIn URL and parses for hidden forms required to login.
r = s.get(URL + URL_SIGNIN)
soup = BeautifulSoup(r.text, 'html.parser')
form = soup.findAll('form')[1]

# Creates a dictionary with the forms which have a value and the inputted email and password.
payload = dict([
                (t['name'], t['value'])
                for t in form.findAll('input')
                if t.has_attr('value')
])
payload['LoginEmailAddress'] = email
payload['LoginPassword'] = password

# Posts the login payload to the login portal and then connects and scrapes your donor homepage.
r = s.post(URL + URL_LOGIN, data=payload)
soup = BeautifulSoup(s.get(URL + URL_SCRAPE).content, 'html.parser')

# Parses for information about you and your donations. Stops the script if login unsuccessful.
try:
    fullname = soup.find('a', class_='title text-full-name').text   # Full name
except AttributeError:
    print("\nSomething went wrong. Please check your email and password are correct.")
    exit()
container = soup.find('div', class_='welcome_container')
welcome = container.h1.text                                     # Welcome 'first name'
info = container.find_all('strong')
donation_num_str = str.strip(info[0].text)                      # Number of donations
donation_num = int(donation_num_str)                            # Number of donations as an integer
group = str.strip(info[1].text)                                 # Blood group

# Script will stop if you haven't donated yet
if donation_num == 0:
    print("Please donate before using this script.")
    exit()

# Parses for the string with all the donation history information in and then splits into a list
History_String = soup.find(text=re.compile('historyData')).strip() + "},{"
History_List = re.findall(r'"Address":(.+?)},{', History_String)

# Initialise lists
Name_List = []
Latitude_List = []
Longitude_List = []
Date_List = []
match = []

# Searches each element for the address. Then searches for data if the element has an address
for element in range(len(History_List)):
    match = re.search(r'"AddressLines":null', History_List[element])
    if match is None:
        Name = re.search(r'"Name":"(.+?)"', History_List[element])
        Name_List.append(Name[1])
        Latitude = re.search(r'"Latitude":"(.+?)"', History_List[element])
        Latitude_List.append(float(Latitude[1]))
        Longitude = re.search(r'"Longitude":"(.+?)"', History_List[element])
        Longitude_List.append(float(Longitude[1]))
        Date = re.search(r'"DonatedOnString":"(.+?)"', History_List[element])
        Date_List.append(datetime.datetime.strptime(Date[1], '%d-%m-%Y').date())

# Blood donor tiers and their required donation number.
tiers_num = [0, 5, 25, 50, 75, 100]
tiers = ["", "bronze", "silver", "gold", "emerald", "ruby"]

# Iterates through the tiers list to find which tier is your next goal using your donation number.
i = 0
diff = 0
for i in range(len(tiers_num)):
    diff = tiers_num[i] - donation_num
    if diff >= 0:
        if diff == 0:
            newTier = True
        else:
            newTier = False
        break

# Calculates time to next tier
RestTime = (Date_List[0] - Date_List[-1]) / (len(Date_List) - 1)    # Average time between donations
TierDate = Date_List[0] + RestTime * diff

# Prints a welcome statement with donation stats. Also, says how many donations required to next tier.
text1 = welcome + ".\nYou have donated " + donation_num_str + " pints of " + group + " blood."

if 0 < donation_num <= tiers_num[-1]:
    text2 = "Your current tier is " + tiers[i-1] + " and you are only " + str(diff) + " donations away from " + \
            tiers[i] + ". At your current rate you should reach this on " + str(TierDate.strftime('%d %B %Y.'))
else:
    text2 = "Congrats. You have achieved the top donor rank of " + tiers[-1] + " with a whopping " + donation_num_str\
            + " donations!"

favourites = Counter(Name_List).most_common(3)
count = len(favourites)
if count == 3:
    text3 = "Also, here are your top three most visited centres: \n" + str(favourites)
elif count == 2:
    text3 = "Also, here are your top two most visited centres: \n" + str(favourites)
else:
    text3 = "Also, here is your most visited centre: \n" + str(favourites)

# Creates a map with a heatmap of donation locations
if api_flag:
    gmap = gmplot.GoogleMapPlotter(statistics.mean(Latitude_List), statistics.mean(Longitude_List), 8,
                                   apikey=api)
else:
    gmap = gmplot.GoogleMapPlotter(statistics.mean(Latitude_List), statistics.mean(Longitude_List), 8,)

gmap.heatmap(Latitude_List, Longitude_List, radius=12)

# Creates markers with the name and then saves the map to the user's desktop
for element in range(len(Name_List)):
    gmap.marker(Latitude_List[element], Longitude_List[element], title=Name_List[element])
gmap.coloricon = 'http://www.googlemapsmarkers.com/v1/%s/'

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
gmap.draw(desktop + '\\DonationMap.html')

text4 = "A map of your donation locations has now been created on your desktop."

print("\n" + text1 + "\n" + text2 + "\n" + text3 + "\n" + text4)

shut_down = input("\nPress 'y' if you want this information to be saved as a .txt file to your desktop. Otherwise press"
                  " any key to exit: ")
if shut_down == 'y':
    with open(desktop + "\\DonationStats.txt", "w") as file:
        file.write(text1 + "\n" + text2 + "\n" + text3 + "\n" + text4)
