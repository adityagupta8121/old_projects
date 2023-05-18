''''
Anaconda Navigator
- Open Jupyter Notebook
- Run the .ipynb file
- downloads file in the same folder as the .ipynb file

Download Visual Studio Code
- Add Extension - Python from Microsoft
- Change the environment to : 'Python 3.8.3 64-bit ('base' : conda)'
- Run program using play/run button on top right
- ***Downloads file in systems main folder - so have to specify path

Modules to install (run on command line):
pip install BeautifulSoup
pip install requests
pip install pandas

Read:
Block 1: Update existing file
Block 2: Write new file
Block 3: Update existing file w/ range
Block 4: Switch case to call functions
'''
#importing header files/libraries
#import sys to get exit()
#csv - to make csv file
#re - regular/regex expressions to get data organised from details
#datetime - helps get the date&time in the right format
#requests - send http requests
#BeautifulSoup - extract html code
#importing pandas to remove duplicates
import sys
import csv
import re
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#######
Block 1: Program to update existing file with new data.         
#######
''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#Program to update the existing file with new data
def update(start, end):

    #https://www.clearadmit.com/livewire/ pulls in data from ajax file
    url = "https://www.clearadmit.com/wp-admin/admin-ajax.php"

    params = {
        "action": "livewire_load_posts",
        "school": "",
        "round": "",
        "status": "",
        "orderby": "",
        "paged": "",
    }

    #opening the file in read mode and storing data in csvFileArray
    csvfile = open('ClearAdmit LiveWire Scrape.csv', 'r')
    csvFileArray = []
    for row in csv.DictReader(csvfile):
        csvFileArray.append(row)    
    csvfile.close()
    #closing the file

    #opening the file again but in append mode
    file = open('ClearAdmit LiveWire Scrape.csv', 'a')
    writer = csv.writer(file) 
    #writer.writerow(['Date', 'Time', 'Status','School','GPA','GRE','GMAT','Round', # <----- Header row
    #                 'Location','Post-MBA Career','via','on','Details','Note'])

    #assigining variable which breaks when duplicate data is detected using while loop.
    #LOOP WILL RUN INFINITELY IF NO DUPLICATE DATA TILL LAST PAGE OF SCAN
    loop = True

    while loop is True:
        #loop for page numbers
        for page in range(1, 100): 
            if not loop:
                break

            #prints page number on terminal
            print("Checking page {}..".format(page))

            #getting data from the website
            params["paged"] = page
            data = requests.post(url, data=params).json()
            soup = BeautifulSoup(data["markup"], "html.parser")

            #loop to get the data from each entry (livewire-entry)
            for entry in soup.select(".livewire-entry"):

                datime = entry.select_one(".adate") #date&time ----- (1)
                status = entry.select_one(".status") #status ----- No conditions
                name = status.find_next("strong") #school ----- No conditions
                details = entry.select_one(".lw-details") #details ----- (2)
                postcar = entry.select_one(".post-career") #post-mba-career ----- (3)
                notes = entry.select_one(".note") #notes ----- (4)
                viaon = entry.select_one(".update") #via-and-on ----- (5)

                ################################
                #Conditions for getting specific data begin HERE ----- (Check numbering)
                #the code that is commeneted was used earlier, or can be a better alternative
                #in case of any problems with the existing code
                #each code has short description (sort of)

                #################
                #datetim - uses datetime to get the format - Spacing is imp ----- (date&time - (1))
                #datime gets collective value, can be used to get both d&t in one variable
                #date stores date from datetim
                #time stores time from datetim
                datime = datime.get_text(strip=True)
                datime = datetime.datetime.strptime(datime, '%B %d, %Y %I:%M%p')
                time = str(datime.time()) #returns time
                date = str(datime.date()) #returns date

                #################
                #notes conditions ----- (post-mba career - (4)) 
                #checks for None to display message
                if notes is None:
                            notes = 'No data provided'
                else:
                            notes = notes.get_text(strip=True),

                notes = ''.join(map(str, notes))  #returns notes
                notes = str(notes)

                #################
                #via-and-on - conditions applied to get 'via' and 'on' fields ----- (5)
                #on conditions - gets from viaon and strips to get all data after via ----- (5.1)
                #later using nested if...elif...else to eliminate extra text
                #'Today' returns date from column 1 - adate
                #'on' returns the date mentioned after it
                #'on' returns date from col 1 - adate when 'date not specified'
                #any exception returns date from col 1 - adate
                on = viaon.get_text(strip=True)
                on = on.split('via', maxsplit=1)[-1].strip()
                on = " ".join(on.split()[1:-1])
                on = on.split('.')[0] #returns all possible data
                onsplit = on.split() #splits the data

                #checks first word for 'today' to return date from 'adate'
                if onsplit[0] == "Today": 
                    ond = date
                #checks first word for 'on' to return the date in format
                elif onsplit[0] == "on":
                    #adds the date to make string
                    onsum = onsplit[1] +  " " + onsplit[2] + " " + onsplit[3]
                    #checks for Date not specified
                    if onsum == "Date Not Specified":
                        ond = date
                        #ond = "Date Not Specified"
                    else:
                        #converts the date into format
                        ond = datetime.datetime.strptime(onsum, '%B %d, %Y')
                        ond = ond.date()
                #else shows No data Provided when it is wrong
                else:
                    ond = date 
                    #ond = "No data provided" 
                    #returns ond = on date

                ond = str(ond)

                #via - uses via-on to get data after 'via' using strip and split ----- (5.2)
                #checks for attached strings/words
                #via - picks and returns data as a word with any attached word^^^^ eg : n/aGPA
                #viaref - refined version of data after removing extra letters/words
                via = viaon.get_text(strip=True)
                via = via.split('via', maxsplit=1)[-1].strip().split()[0]
                viaref = via.replace("GPA:", "").replace("GRE:", "").replace("GMAT:", "").replace("Round:", "")
                if viaref not in ("n/a", "portal", "email", "phone"):
                    viaref = "n/a"
                #returns viaref

                viaref = str(viaref)
                ######################

                #################
                #post-mba career conditions ----- (post-mba career - (3)) 
                #checks for None to display message
                #Note: Starts from 17th index to skip 'post-mba career:'
                if postcar is None:
                            postcar = 'No data provided'
                else:
                            postcar = postcar.get_text(strip=True)[17:]

                postcar = ''.join(map(str, postcar))  #returns postcar            
                postcar = str(postcar)

                #################
                #details - conditions derived from details to get GPA, GRE, GMAT, Round & location ----- (details - (2))
                #GPA - uses re expressions to get data from details ----- (GPA - (2.1))
                GPA = re.findall('\W*GPA: ([\d.]+)', details.get_text(strip = True))
                if GPA == []:
                    GPA = 'No data provided'
                else:
                    GPA = (''.join(GPA))  #returns GPA

                GPA = str(GPA)


                #GRE - uses re expressions to get data from details ----- (GRE - (2.2))
                GRE = re.findall('\W*GRE: ([\d.]+)', details.get_text(strip = True))
                if GRE == []:
                    GRE = 'No data provided'
                else:
                    GRE = (''.join(GRE))  #returns GRE

                GRE = str(GRE)

                #GMAT - uses re expressions to get data from details ----- (GMAT - (2.3))
                GMAT = re.findall('\W*GMAT: ([\d.]+)', details.get_text(strip = True))
                if GMAT == []:
                    GMAT = 'No data provided'
                else:
                    GMAT = (''.join(GMAT))  #returns GMAT

                GMAT = str(GMAT)

                #Round - uses re expressions to get data from details ----- (Round - (2.4))
                #Commented gives just round number
                #New gives rolling admissions
                #Round = re.findall('\S*Round ([a-zA-Z0-9]+)', details.get_text(strip = True))
                Round = re.findall('Round: (.*?)($|\|)', details.get_text(strip = True))
                if Round == []:
                    Round = 'No data provided'
                else:
                    #(''.join(Round))
                    Round = Round[0][0]  #returns Round

                Round = str(Round)

                #location - uses re expressions to get data from details ----- (location - (2.5))
                location = re.search('\|(.+)', details.get_text(strip = True))
                if location:
                    location = (location.group(1).strip())
                else:
                    location = 'No data provided'  #returns location

                location = str(location)

                #DONT MESS W/ INDENTATION
                #Conditions to check duplicates using csvFileArray
                already_exists = False
                for firstentry in csvFileArray:
                    already_exists = (firstentry['Date'] == date
                                 and firstentry['Time'] == time
                                 and firstentry['Status'] == (status.get_text(strip=True))
                                 and firstentry['School'] == name.get_text(strip=True)
                                 and (firstentry['GPA'] == str(GPA))
                                 and (firstentry['GRE'] == str(GRE))
                                 and (firstentry['GMAT'] == str(GMAT))
                                 and (firstentry['Round'] == str(Round))
                                 and (firstentry['Location'] == str(location))
                                 and (firstentry['Post-MBA Career'] == str(postcar))
                                 and (firstentry['via'] == str(viaref))
                                 and (firstentry['on'] == str(ond))
                                 and firstentry['Details'] == details.get_text(strip=True)
                                 and (firstentry['Note'] == str(notes)))

                    if already_exists:
                        print('Drop')
                        loop = False
                        break

                if not already_exists:
                    print('New entry found - Updating...')
                    writer.writerow(
                        [date, time, status.get_text(strip=True), name.get_text(strip=True), 
                         GPA, GRE, GMAT, Round, location, postcar, viaref, ond,
                         details.get_text(strip=True), notes]) 
            #draws a clean line after one page on terminal
            print("-" * 80) 

    #closing the file
    file.close()
    #message on terminal after program ends
    print("Data scraped successfuly!")
    
    print("\nChecking for Duplicates...")
    df = pd.read_csv('ClearAdmit LiveWire Scrape.csv')
    df = df.drop_duplicates()
    df.to_csv("ClearAdmit LiveWire Scrape.csv", index=False)
    print("\nDuplicates checked")
    print("\nProgram ends here!")
    #program ends here

''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#######                                                 --------------------------- ENDS HERE
Block 1: Program to update existing file with new data. --------------------------- ENDS HERE
#######                                                 --------------------------- ENDS HERE
''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''

''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#######                                                
Block 2: Program to write new file. 
#######                                                
''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#Program to write new data from the website

def write(start, end):

    #https://www.clearadmit.com/livewire/ pulls in data from ajax file
    url = "https://www.clearadmit.com/wp-admin/admin-ajax.php"

    params = {
        "action": "livewire_load_posts",
        "school": "",
        "round": "",
        "status": "",
        "orderby": "",
        "paged": "",
    }

    #opening the file in write mode
    file = open('ClearAdmit LiveWire Scrape.csv', 'w') # <----- (add destination - pwd) Change the name of file HERE
    writer = csv.writer(file) 
    writer.writerow(['Date', 'Time', 'Status','School','GPA','GRE','GMAT','Round', # <----- Header row
                     'Location','Post-MBA Career','via','on','Details','Note'])

    #loop for page numbers
    for page in range(start, (end+1)): # <----- (0, n-1) Change the page number range HERE

        #prints page number on terminal
        print("Getting page {}..".format(page))

        #getting data from the website
        params["paged"] = page
        data = requests.post(url, data=params).json()
        soup = BeautifulSoup(data["markup"], "html.parser")

        #loop to get the data from each entry (livewire-entry)
        for entry in soup.select(".livewire-entry"):

            datime = entry.select_one(".adate") #date&time ----- (1)
            status = entry.select_one(".status") #status ----- No conditions
            name = status.find_next("strong") #school ----- No conditions
            details = entry.select_one(".lw-details") #details ----- (2)
            postcar = entry.select_one(".post-career") #post-mba-career ----- (3)
            notes = entry.select_one(".note") #notes ----- (4)
            viaon = entry.select_one(".update") #via-and-on ----- (5)


            ################################
            #Conditions for getting specific data begin HERE ----- (Check numbering)
            #the code that is commeneted was used earlier, or can be a better alternative
            #in case of any problems with the existing code
            #each code has short description (sort of)

            #################
            #datetim - uses datetime to get the format - Spacing is imp ----- (date&time - (1))
            #datime gets collective value, can be used to get both d&t in one variable
            #date stores date from datetim
            #time stores time from datetim
            datime = datime.get_text(strip=True)
            datime = datetime.datetime.strptime(datime, '%B %d, %Y %I:%M%p')
            time = datime.time() #returns time
            date = datime.date() #returns date

            #################
            #details - conditions derived from details to get GPA, GRE, GMAT, Round & location ----- (details - (2))
            #GPA - uses re expressions to get data from details ----- (GPA - (2.1))
            GPA = re.findall('\W*GPA: ([\d.]+)', details.get_text(strip = True))
            if GPA == []:
                GPA = 'No data provided'
            else:
                GPA = (''.join(GPA))  #returns GPA

            #GRE - uses re expressions to get data from details ----- (GRE - (2.2))
            GRE = re.findall('\W*GRE: ([\d.]+)', details.get_text(strip = True))
            if GRE == []:
                GRE = 'No data provided'
            else:
                GRE = (''.join(GRE))  #returns GRE

            #GMAT - uses re expressions to get data from details ----- (GMAT - (2.3))
            GMAT = re.findall('\W*GMAT: ([\d.]+)', details.get_text(strip = True))
            if GMAT == []:
                GMAT = 'No data provided'
            else:
                GMAT = (''.join(GMAT))  #returns GMAT

            #Round - uses re expressions to get data from details ----- (Round - (2.4))
            #Commented gives just round number
            #New gives rolling admissions
            #Round = re.findall('\S*Round ([a-zA-Z0-9]+)', details.get_text(strip = True))
            Round = re.findall('Round: (.*?)($|\|)', details.get_text(strip = True))
            if Round == []:
                Round = 'No data provided'
            else:
                #(''.join(Round))
                Round = Round[0][0]  #returns Round

            #location - uses re expressions to get data from details ----- (location - (2.5))
            location = re.search('\|(.+)', details.get_text(strip = True))
            if location:
                location = (location.group(1).strip())
            else:
                location = 'No data provided'  #returns location

            #################
            #post-mba career conditions ----- (post-mba career - (3)) 
            #checks for None to display message
            #Note: Starts from 17th index to skip 'post-mba career:'
            if postcar is None:
                        postcar = 'No data provided'
            else:
                        postcar = postcar.get_text(strip=True)[17:]

            postcar = ''.join(map(str, postcar))  #returns postcar

            #################
            #notes conditions ----- (post-mba career - (4)) 
            #checks for None to display message
            if notes is None:
                        notes = 'No data provided'
            else:
                        notes = notes.get_text(strip=True),

            notes = ''.join(map(str, notes))  #returns notes

            #################
            #via-and-on - conditions applied to get 'via' and 'on' fields ----- (5)
            #on conditions - gets from viaon and strips to get all data after via ----- (5.1)
            #later using nested if...elif...else to eliminate extra text
            #'Today' returns date from column 1 - adate
            #'on' returns the date mentioned after it
            #'on' returns date from col 1 - adate when 'date not specified'
            #any exception returns date from col 1 - adate
            on = viaon.get_text(strip=True)
            on = on.split('via', maxsplit=1)[-1].strip()
            on = " ".join(on.split()[1:-1])
            on = on.split('.')[0] #returns all possible data
            onsplit = on.split() #splits the data

            #checks first word for 'today' to return date from 'adate'
            if onsplit[0] == "Today": 
                ond = date
            #checks first word for 'on' to return the date in format
            elif onsplit[0] == "on":
                #adds the date to make string
                onsum = onsplit[1] +  " " + onsplit[2] + " " + onsplit[3]
                #checks for Date not specified
                if onsum == "Date Not Specified":
                    ond = date
                    #ond = "Date Not Specified"
                else:
                    #converts the date into format
                    ond = datetime.datetime.strptime(onsum, '%B %d, %Y')
                    ond = ond.date()
            #else shows No data Provided when it is wrong
            else:
                ond = date 
                #ond = "No data provided" 
                #returns ond = on date


            #via - uses via-on to get data after 'via' using strip and split ----- (5.2)
            #checks for attached strings/words
            #via - picks and returns data as a word with any attached word^^^^ eg : n/aGPA
            #viaref - refined version of data after removing extra letters/words
            via = viaon.get_text(strip=True)
            via = via.split('via', maxsplit=1)[-1].strip().split()[0]
            viaref = via.replace("GPA:", "").replace("GRE:", "").replace("GMAT:", "").replace("Round:", "")
            if viaref not in ("n/a", "portal", "email", "phone"):
                viaref = "n/a"
            #returns viaref

            #conditions end here! ----- ((P))((!))
            ################################

            #prints details on terminal
            print(
                "{:<25} {:<25} {}".format(
                    #date,
                    status.get_text(strip=True),
                    name.get_text(strip=True),
                    details.get_text(strip=True)
                    #postcar
                    #notes
                )
            )


            #writes rows in loop
            writer.writerow([date, time, status.get_text(strip=True), name.get_text(strip=True),
                             GPA, GRE, GMAT, Round, location, postcar, viaref, ond,
                             details.get_text(strip=True), notes])

            #loop ends

        #draws a clean line after one page on terminal
        print("-" * 80) 

    #closing the file
    file.close()
    #message on terminal after program ends
    print("Data scraped successfuly!")
    #program ends here

''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#######                                                 --------------------------- ENDS HERE
Block 2: Program to write new file------------------------------------------------- ENDS HERE
#######                                                 --------------------------- ENDS HERE
''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''

''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#######                                                
Block 3: Program to update file from specific range 
#######                                                
''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''

#Update from specific range

def updaterange(start, end):
    
    #https://www.clearadmit.com/livewire/ pulls in data from ajax file
    url = "https://www.clearadmit.com/wp-admin/admin-ajax.php"

    params = {
        "action": "livewire_load_posts",
        "school": "",
        "round": "",
        "status": "",
        "orderby": "",
        "paged": "",
    }

    #opening the file in write mode
    file = open('ClearAdmit LiveWire Scrape.csv', 'a') # <----- (add destination - pwd) Change the name of file HERE
    writer = csv.writer(file) 
    #writer.writerow(['Date', 'Time', 'Status','School','GPA','GRE','GMAT','Round', # <----- Header row
    #                 'Location','Post-MBA Career','via','on','Details','Note'])

    #loop for page numbers
    for page in range(start, (end+1)): # <----- (0, n-1) Change the page number range HERE

        #prints page number on terminal
        print("Getting page {}..".format(page))

        #getting data from the website
        params["paged"] = page
        data = requests.post(url, data=params).json()
        soup = BeautifulSoup(data["markup"], "html.parser")

        #loop to get the data from each entry (livewire-entry)
        for entry in soup.select(".livewire-entry"):

            datime = entry.select_one(".adate") #date&time ----- (1)
            status = entry.select_one(".status") #status ----- No conditions
            name = status.find_next("strong") #school ----- No conditions
            details = entry.select_one(".lw-details") #details ----- (2)
            postcar = entry.select_one(".post-career") #post-mba-career ----- (3)
            notes = entry.select_one(".note") #notes ----- (4)
            viaon = entry.select_one(".update") #via-and-on ----- (5)


            ################################
            #Conditions for getting specific data begin HERE ----- (Check numbering)
            #the code that is commeneted was used earlier, or can be a better alternative
            #in case of any problems with the existing code
            #each code has short description (sort of)

            #################
            #datetim - uses datetime to get the format - Spacing is imp ----- (date&time - (1))
            #datime gets collective value, can be used to get both d&t in one variable
            #date stores date from datetim
            #time stores time from datetim
            datime = datime.get_text(strip=True)
            datime = datetime.datetime.strptime(datime, '%B %d, %Y %I:%M%p')
            time = datime.time() #returns time
            date = datime.date() #returns date

            #################
            #details - conditions derived from details to get GPA, GRE, GMAT, Round & location ----- (details - (2))
            #GPA - uses re expressions to get data from details ----- (GPA - (2.1))
            GPA = re.findall('\W*GPA: ([\d.]+)', details.get_text(strip = True))
            if GPA == []:
                GPA = 'No data provided'
            else:
                GPA = (''.join(GPA))  #returns GPA

            #GRE - uses re expressions to get data from details ----- (GRE - (2.2))
            GRE = re.findall('\W*GRE: ([\d.]+)', details.get_text(strip = True))
            if GRE == []:
                GRE = 'No data provided'
            else:
                GRE = (''.join(GRE))  #returns GRE

            #GMAT - uses re expressions to get data from details ----- (GMAT - (2.3))
            GMAT = re.findall('\W*GMAT: ([\d.]+)', details.get_text(strip = True))
            if GMAT == []:
                GMAT = 'No data provided'
            else:
                GMAT = (''.join(GMAT))  #returns GMAT

            #Round - uses re expressions to get data from details ----- (Round - (2.4))
            #Commented gives just round number
            #New gives rolling admissions
            #Round = re.findall('\S*Round ([a-zA-Z0-9]+)', details.get_text(strip = True))
            Round = re.findall('Round: (.*?)($|\|)', details.get_text(strip = True))
            if Round == []:
                Round = 'No data provided'
            else:
                #(''.join(Round))
                Round = Round[0][0]  #returns Round

            #location - uses re expressions to get data from details ----- (location - (2.5))
            location = re.search('\|(.+)', details.get_text(strip = True))
            if location:
                location = (location.group(1).strip())
            else:
                location = 'No data provided'  #returns location

            #################
            #post-mba career conditions ----- (post-mba career - (3)) 
            #checks for None to display message
            #Note: Starts from 17th index to skip 'post-mba career:'
            if postcar is None:
                        postcar = 'No data provided'
            else:
                        postcar = postcar.get_text(strip=True)[17:],

            postcar = ''.join(map(str, postcar))  #returns postcar

            #################
            #notes conditions ----- (post-mba career - (4)) 
            #checks for None to display message
            if notes is None:
                        notes = 'No data provided'
            else:
                        notes = notes.get_text(strip=True),

            notes = ''.join(map(str, notes))  #returns notes

            #################
            #via-and-on - conditions applied to get 'via' and 'on' fields ----- (5)
            #on conditions - gets from viaon and strips to get all data after via ----- (5.1)
            #later using nested if...elif...else to eliminate extra text
            #'Today' returns date from column 1 - adate
            #'on' returns the date mentioned after it
            #'on' returns date from col 1 - adate when 'date not specified'
            #any exception returns date from col 1 - adate
            on = viaon.get_text(strip=True)
            on = on.split('via', maxsplit=1)[-1].strip()
            on = " ".join(on.split()[1:-1])
            on = on.split('.')[0] #returns all possible data
            onsplit = on.split() #splits the data

            #checks first word for 'today' to return date from 'adate'
            if onsplit[0] == "Today": 
                ond = date
            #checks first word for 'on' to return the date in format
            elif onsplit[0] == "on":
                #adds the date to make string
                onsum = onsplit[1] +  " " + onsplit[2] + " " + onsplit[3]
                #checks for Date not specified
                if onsum == "Date Not Specified":
                    ond = date
                    #ond = "Date Not Specified"
                else:
                    #converts the date into format
                    ond = datetime.datetime.strptime(onsum, '%B %d, %Y')
                    ond = ond.date()
            #else shows No data Provided when it is wrong
            else:
                ond = date 
                #ond = "No data provided" 
                #returns ond = on date


            #via - uses via-on to get data after 'via' using strip and split ----- (5.2)
            #checks for attached strings/words
            #via - picks and returns data as a word with any attached word^^^^ eg : n/aGPA
            #viaref - refined version of data after removing extra letters/words
            via = viaon.get_text(strip=True)
            via = via.split('via', maxsplit=1)[-1].strip().split()[0]
            viaref = via.replace("GPA:", "").replace("GRE:", "").replace("GMAT:", "").replace("Round:", "")
            if viaref not in ("n/a", "portal", "email", "phone"):
                viaref = "n/a"
            #returns viaref

            #conditions end here! ----- ((P))((!))
            ################################

            #prints details on terminal
            print(
                "{:<25} {:<25} {}".format(
                    #date,
                    status.get_text(strip=True),
                    name.get_text(strip=True),
                    details.get_text(strip=True)
                    #postcar
                    #notes
                )
            )


            #writes rows in loop
            writer.writerow([date, time, status.get_text(strip=True), name.get_text(strip=True),
                             GPA, GRE, GMAT, Round, location, postcar, viaref, ond,
                             details.get_text(strip=True), notes])

            #loop ends

        #draws a clean line after one page on terminal
        print("-" * 80) 

    #closing the file
    file.close()
    #message on terminal after program ends
    #print("Data scraped successfuly!")
    #program ends here

    print("\nChecking for Duplicates...")
    df = pd.read_csv('ClearAdmit LiveWire Scrape.csv')
    df = df.drop_duplicates()
    df.to_csv("ClearAdmit LiveWire Scrape.csv", index=False)
    print("Data scraped successfuly!")

''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#######                                                 --------------------------- ENDS HERE
Block 3: Program to update file from specific range.------------------------------- ENDS HERE
#######                                                 --------------------------- ENDS HERE
''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''

''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#######                                                
Block 4: Getting input from user and performing accordingly 
#######                                                
''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''

print("\nClearAdmit LiveWire Scrape")
print("\nPlease make sure 'ClearAdmit-LiveWire-Scrape.csv' exists")
print("\n1. Update the existing file \n2. Update file from a specific range \n3. Write a new file \n4. Exit" )

option = input("\nEnter the option number for the operation to be performed and press Enter: ")
option = int(option)

if option == 1:
    print('Update the existing file')
    start = 1
    end = 101
    print('\n')
    update(start, end)
    
elif option == 2:
    print('Update file from a specific range')
    start = int(input("Start at page: "))
    end = int(input("End at page: "))
    print('\n')
    updaterange(start, end)
    
elif option == 3:
    print('Write a new file')
    start = int(input("Start at page: "))
    end = int(input("End at page: "))
    print('\n')
    write(start, end)
    
elif option == 4:
    sys.exit()
    
else:
    print('Incorrect option!')