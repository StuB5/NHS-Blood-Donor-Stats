# NHS Blood Donor Stats
The code in this project parses the [NHS blood donation website](https://my.blood.co.uk/) for your donor information and then presents it to you in an easy to understand format.

## Getting Started 
This repository contains both a python script and a folder with an exe, which was made using cx_Freeze. The exe requires the whole folder be downloaded to work. These both work in exactly the same way, but the exe allows this to be used without installing python or any of the modules used.

The output produced is a map of your donation locations, the time you will achieve your next donation milestone (eg. bronze, silver etc.), your top 3 donation locations and basic information such as number of donations and blood type.

### User Inputs
This script asks the following questions:
1. Do you have a google maps API key (y/n):
   - This does not prevent a map from being produced. If you say 'y', then it will prompt you for your key. If you say 'n' then the map produced will be watermarked. ([With API key](Example-Output/Map_API.png)/[Without API key](Example-Output/Map_Watermark.png))
2. Please enter your email:
   - This is the email you use for your NHS blood donor account.
3. Please enter your password:
   - This is the password you use for your NHS blood donor account. This field is invisible, so you get no feedback on inputted characters.
4. Press 'y' if you want this information to be saved as a .txt file to your desktop. Otherwise press any key to exit:
   - Saves a [text file](Example-Output/DonationStats.txt) to the desktop with all the information displayed in the terminal if the user sends 'y'.

## Licensing
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
