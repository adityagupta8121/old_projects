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
If ClearAdmit running, No problem

Read:
Block 1: Update existing file
Block 2: Write new file
Block 3: Switch case to call functions
'''
#importing libraries
#requests - request website
#csv - read/write csv
#datetime - read/write in date-time format
#pandas - detect duplicates/write dataframe
#sleep from time - delays program for n seconds when connecting server
import sys
import csv
import datetime
import requests
import pandas as pd
from time import sleep

#api link from Developer Toos -> Network -> XHR
link = 'https://gmatclub.com/api/schools/v1/forum/app-tracker-latest-updates'

''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#######
Block 1: Program to update existing file with new data.         
#######
''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#Program to update the existing file with new data
def update(link):
    #opening the file in read mode and storing data in csvFileArray
    csvfile = open('GMATClub-DT-Scrape.csv', 'r')
    csvFileArray = []
    for row in csv.DictReader(csvfile):
        csvFileArray.append(row)    
    csvfile.close()
    #closing the file

    #declaring parameters for the website
    params = {'limit': 500, 'offset': 0, 'year': 'all'}

    #declaring dictionary to identify status given by status-id (in website data)
    #add if any key missing
    status_mapping = {1: { 'id':1,'class':'mainApplicationSubmitted','name':'Application Submitted' },
                      3: { 'id':3,'class':'mainInterviewed','name':'Interviewed' },
                      4: { 'id':4,'class':'mainAdmitted','name':'Admitted' },
                      5: { 'id':5,'class':'mainDenied','name':'Denied' },
                      6: { 'id':6,'class':'mainDenied','name':'Denied' },
                      7: { 'id':7,'class':'mainWaitListed','name':'Waitlisted' },
                      8: { 'id':8,'class':'mainWaitListed','name':'Waitlisted' },
                      9: { 'id':9,'class':'mainMatriculating','name':'Matriculating' },
                      10: { 'id':10,'class':'mainWlAdmited','name':'Admitted from WL' },
                      11: { 'id':11,'class':'mainResearching','name':'Researching or Writing Essays' },
                      12: { 'id':12,'class':'mainInvitedToInterview','name':'Invited To Interview' },
                      13: { 'id':13,'class':'mainWithdrawn','name':'Withdrawn Application '},
                      14: { 'id':14,'class':'mainDeferred','name':'Deferred to Next Year'}}


    #opening the file in write-mode
    file = open('GMATClub-DT-Scrape.csv', 'a') # <----- Change the name of file HERE 
    writer = csv.writer(file) 

    #writer.writerow(['Date', 'Time', 'Status', 'School', 'Location','via','Industry','WE', #declaring header-row
    #                 'GPA', 'GMAT Total', 'GMAT Quant', 'GMAT Verbal', 
    #                 'GRE Total', 'GRE Quant', 'GRE Verbal',
    #                 'EA Total', 'EA Quant', 'EA Verbal', 'EA IR', 'CAT Percentile', 'CAT Total'])


    #sending requests and declaring user-agent
    with requests.Session() as con: 

        con.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.0.740 Yowser/2.5 Safari/537.36"
        con.get("https://gmatclub.com/forum/decision-tracker.html")

        while True:

            print("Getting data...")
            #repeat until we get correct response from server
            while True:

                try:
                    endpoint = con.get(link, params=params).json()
                    break

                except requests.exceptions.ConnectionError:
                    print("ConnectionError: Retrying in 3 seconds...")
                    sleep(3)  #wait a little bit and try again to connect incase of CorrectionError
                    continue

            if not endpoint["statistics"]:
                break 
                #breaks when detects no data

            #True till no duplicate found from csvFileArray
            #LOOP WILL RUN INFINITELY IF NO DUPLICATE DATA TILL LAST PAGE OF SCAN
            loop = True

            while loop is True:

                #loop to get data
                for item in endpoint["statistics"]:

                    if not loop:
                        break

                    ###############################
                    ########### data and conditions
                    #date
                    datime = item['date']
                    datime = datetime.datetime.strptime(datime, '%Y-%m-%d %H:%M:%S')
                    time = str(datime.time())
                    date = str(datime.date())
                    
                    #username
                    uname = str(item['user_name'])

                    #status
                    status = str(status_mapping[int(item['status_id'])]['name'])

                    #school
                    school = str(item['school_title'])

                    #location
                    country = str(item['country'])
                    state = str(item['state'])
                    location = country

                    #accepted-via
                    via = str(item['accepted_via'])

                    if via == "None":
                        via = "no data provided"

                    if via == "portal_update":
                        via = "portal"

                    #industry
                    industry = str(item['industry'])

                    if industry == "None" or industry == "Other":
                        industry = "no data provided"

                    #we
                    we = str(item['we'])

                    if we == "None":
                        we = "no data provided"

                    #under-grad-gpa
                    gpa = str(item['gpa'])

                    if gpa == "None":
                        gpa = "no data provided"

                    #GMAT-scores
                    gmattot = str(item['gmat_total'])
                    gmatq = str(item['gmat_quant'])
                    gmatv = str(item['gmat_verbal']) 

                    if gmattot == "None":
                        gmattot = "no data provided"            
                    if gmatq == "None":
                        gmatq = "no data provided"            
                    if gmatv == "None":
                        gmatv = "no data provided" 

                    #GRE-scores
                    gretot = str(item['gre_total'])
                    greq = str(item['gre_quant'])
                    grev = str(item['gre_verbal'])

                    if gretot == "None":
                        gretot = "no data provided"            
                    if greq == "None":
                        greq = "no data provided"            
                    if grev == "None":
                        grev = "no data provided" 

                    #ea-scores
                    eatot = str(item['ea_total'])
                    eaq = str(item['ea_quant'])
                    eav = str(item['ea_verbal'])
                    eai = str(item['ea_ir'])

                    if eatot == "None":
                        eatot = "no data provided"            
                    if eaq == "None":
                        eaq = "no data provided"            
                    if eav == "None":
                        eav = "no data provided" 
                    if eai == "None":
                        eai = "no data provided" 

                    #cat-india-scores
                    catp = str(item['cat_india_percentile'])
                    cattot = str(item['cat_india_total'])
                    if catp == "None":
                        catp = "no data provided"            
                    if cattot == "None":
                        cattot = "no data provided"            

                    #Conditions to check duplicates using csvFileArray
                    already_exists = False
                    for firstentry in csvFileArray:
                        already_exists = (firstentry['Date'] == date
                                     and firstentry['Time'] == time
                                     and firstentry['Status'] == status
                                     and firstentry['School'] == school
                                     and firstentry['Location'] == location
                                     and firstentry['via'] == via
                                     and firstentry['Industry'] == industry
                                     and firstentry['WE'] == we
                                     and firstentry['GPA'] == gpa
                                     and firstentry['GMAT Total'] == gmattot
                                     and firstentry['GMAT Quant'] == gmatq
                                     and firstentry['GMAT Verbal'] == gmatv
                                     and firstentry['GRE Total'] == gretot
                                     and firstentry['GRE Quant'] == greq
                                     and firstentry['GRE Verbal'] == grev
                                     and firstentry['EA Total'] == eatot
                                     and firstentry['EA Quant'] == eaq
                                     and firstentry['EA Verbal'] == eav
                                     and firstentry['EA IR'] == eai
                                     and firstentry['CAT Percentile'] == catp
                                     and firstentry['CAT Total'] == cattot
                                     and firstentry['Username'] == uname)

                        if already_exists:
                            print('Drop')
                            loop = False
                            break

                    if not already_exists:
                        print('New entry found - Updating...')
                        writer.writerow([date, time, uname, status, school, location, via, industry, we,
                                         gpa, gmattot, gmatq, gmatv, gretot, greq, grev, 
                                         eatot, eaq, eav, eai, catp, cattot])


            params['offset']+=499 #making sure parameters are increased for loop and data

        #loop ends

    #Confirms data scraped and closes file
    print('\nData Scraped Successfully!')
    file.close()

    #checks for duplicates and deleting using pandas
    print("\nChecking for Duplicates...")
    df = pd.read_csv('GMATClub-DT-Scrape.csv')
    df = df.drop_duplicates()
    df.to_csv('GMATClub-DT-Scrape.csv', index=False)
    print("\ncsv file is ready!")
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

def write(link):
    #declaring parameters for the website (link extension)
    params = {'limit': 500, 'offset': 0, 'year': 'all'}

    #declaring dictionary to identify status given by status-id (in website data)
    #add if any key missing
    status_mapping = {1: { 'id':1,'class':'mainApplicationSubmitted','name':'Application Submitted' },
                      3: { 'id':3,'class':'mainInterviewed','name':'Interviewed' },
                      4: { 'id':4,'class':'mainAdmitted','name':'Admitted' },
                      5: { 'id':5,'class':'mainDenied','name':'Denied' },
                      6: { 'id':6,'class':'mainDenied','name':'Denied' },
                      7: { 'id':7,'class':'mainWaitListed','name':'Waitlisted' },
                      8: { 'id':8,'class':'mainWaitListed','name':'Waitlisted' },
                      9: { 'id':9,'class':'mainMatriculating','name':'Matriculating' },
                      10: { 'id':10,'class':'mainWlAdmited','name':'Admitted from WL' },
                      11: { 'id':11,'class':'mainResearching','name':'Researching or Writing Essays' },
                      12: { 'id':12,'class':'mainInvitedToInterview','name':'Invited To Interview' },
                      13: { 'id':13,'class':'mainWithdrawn','name':'Withdrawn Application '},
                      14: { 'id':14,'class':'mainDeferred','name':'Deferred to Next Year'}}


    #opening the file in write-mode
    file = open('GMATClub-DT-Scrape.csv', 'w') # <----- Change the name of file HERE 
    writer = csv.writer(file) 
    writer.writerow(['Date', 'Time', 'Username','Status', 'School', 'Location','via','Industry','WE', #declaring header-row
                     'GPA', 'GMAT Total', 'GMAT Quant', 'GMAT Verbal', 
                     'GRE Total', 'GRE Quant', 'GRE Verbal',
                     'EA Total', 'EA Quant', 'EA Verbal', 'EA IR', 'CAT Percentile', 'CAT Total'])


    #sending requests and declaring user-agent
    with requests.Session() as con: 

        con.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.0.740 Yowser/2.5 Safari/537.36"
        con.get("https://gmatclub.com/forum/decision-tracker.html")

        while True:

            print("Getting data...")
            #repeat until we get correct response from server
            while True:

                try:#break when reached end
                    endpoint = con.get(link, params=params).json()
                    break

                except requests.exceptions.ConnectionError:
                    print("ConnectionError: Retrying in 3 seconds...")
                    sleep(3) #wait a little bit and try again to connect incase of CorrectionError
                    continue

            if not endpoint["statistics"]:
                break 
                #breaks when detects no data

            #loop to get data from statistics
            for item in endpoint["statistics"]:

                ###############################
                ########### data and conditions            
                #date
                datime = item['date']
                datime = datetime.datetime.strptime(datime, '%Y-%m-%d %H:%M:%S')
                time = str(datime.time())
                date = str(datime.date())
                
                #username
                uname = str(item['user_name'])

                #status
                status = str(status_mapping[int(item['status_id'])]['name'])

                #school
                school = str(item['school_title'])

                #location
                country = str(item['country'])
                state = str(item['state'])
                location = country

                #accepted-via
                via = str(item['accepted_via'])

                if via == "None":
                    via = "no data provided"

                if via == "portal_update":
                    via = "portal"

                #industry
                industry = str(item['industry'])

                if industry == "None" or industry == "Other":
                    industry = "no data provided"

                #we
                we = str(item['we'])

                if we == "None":
                    we = "no data provided"

                #under-grad-gpa
                gpa = str(item['gpa'])

                if gpa == "None":
                    gpa = "no data provided"

                #GMAT-scores
                gmattot = str(item['gmat_total'])
                gmatq = str(item['gmat_quant'])
                gmatv = str(item['gmat_verbal']) 

                if gmattot == "None":
                    gmattot = "no data provided"            
                if gmatq == "None":
                    gmatq = "no data provided"            
                if gmatv == "None":
                    gmatv = "no data provided" 

                #GRE-scores
                gretot = str(item['gre_total'])
                greq = str(item['gre_quant'])
                grev = str(item['gre_verbal'])

                if gretot == "None":
                    gretot = "no data provided"            
                if greq == "None":
                    greq = "no data provided"            
                if grev == "None":
                    grev = "no data provided" 

                #ea-scores
                eatot = str(item['ea_total'])
                eaq = str(item['ea_quant'])
                eav = str(item['ea_verbal'])
                eai = str(item['ea_ir'])

                if eatot == "None":
                    eatot = "no data provided"            
                if eaq == "None":
                    eaq = "no data provided"            
                if eav == "None":
                    eav = "no data provided" 
                if eai == "None":
                    eai = "no data provided" 

                #cat-india-scores
                catp = str(item['cat_india_percentile'])
                cattot = str(item['cat_india_total'])
                if catp == "None":
                    catp = "no data provided"            
                if cattot == "None":
                    cattot = "no data provided"


                ########### data and conditions end here
                ########################################

                #writing the data in rows
                writer.writerow([date, time, uname, status, school, location, via, industry, we,
                                 gpa, gmattot, gmatq, gmatv, gretot, greq, grev, 
                                 eatot, eaq, eav, eai, catp, cattot])



                #print(
                #    "{:<25} {:<25} {}".format(
                #        #date,
                #        school,
                #        country,
                #        state
                #    )
                #)

            params['offset']+=499 #making sure parameters are increased for loop and data

        #loop ends

    #Confirms data scraped and closes file
    print('\nData Scraped Successfully!')
    file.close()

    #checks for duplicates and deleting using pandas
    print("\nChecking for Duplicates...")

    df = pd.read_csv('GMATClub-DT-Scrape.csv')
    df = df.drop_duplicates()
    df.to_csv('GMATClub-DT-Scrape.csv', index=False)

    print("\ncsv file is ready!")
    #program ends here

''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#######                                                 --------------------------- ENDS HERE
Block 2: Program to write new file------------------------------------------------- ENDS HERE
#######                                                 --------------------------- ENDS HERE
''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''

''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''
#######                                                
Block 3: Getting input from user and performing accordingly 
#######                                                
''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' ''' '''

print("\nGMAT Club Decision Tracker Scrape")
print("\nPlease make sure 'GMATClub-DT-Scrape.csv' exists")
print("\n1. Update the existing file \n2. Write a new file \n3. Exit" )

option = input("\nEnter the option number for the operation to be performed and press Enter: ")
option = int(option)

if option == 1:
    print('Update the existing file')
    print('\n')
    update(link)
    
elif option == 2:
    print('Write a new file')
    print('\n')
    write(link)

elif option == 3:
    sys.exit()
    
else:
    print('Incorrect option!')