# NHS-Blood_Donor_Stats
 Parses the [NHS blood donation website](https://my.blood.co.uk/) for your donation information and then presents it to you.
 This repository contains both a python script and a folder with an exe which was made using cx_Freeze. The exe requires the whole folder be downloaded to work. These both work in exactly the same way, but the exe allows this to be used without installing python or any of the modules used making it.
 
 The output produced is a map of your donation locations, the time you will achieve your next donation milestone (eg. bronze, silver etc.), your top 3 donation locations and basic information such as number of donations and blood type.

This script asks the following questions:
1. Do you have a google maps API key (y/n):
   - This does not prevent a map from being produced. If you say 'y', then it will prompt you for your key. If you say 'n' then the map produced will be watermarked.
2. Please enter your email:
   - This is the email you use for your NHS blood donor account.
3. Please enter your password:
   - This is the password you use for your NHS blood donor account. This field is invisible, so you get no feedback on inputted characters.
4. Press 'y' if you want this information to be saved as a .txt file to your desktop. Otherwise press any key to exit:
   - Saves a text file to the desktop with all the information displayed in the terminal if the user sends 'y'.
