from gpapi.googleplay import GooglePlayAPI, RequestError

import sys
import argparse
import os
from time import sleep
import json
import time
os.system("mkdir -p title")
os.system("mkdir -p author")
BATCH_SIZE_TITLE = 3

ap = argparse.ArgumentParser(description='Test download of expansion files')
ap.add_argument('-e', '--email', dest='email', help='google username')
ap.add_argument('-p', '--password', dest='password', help='google password')

args = ap.parse_args()

server = GooglePlayAPI('en_US', 'America/Virginia', 'sailfish')
# LOGIN

print('\nLogging in with email and password\n')
server.login(args.email, args.password, None, None)
gsfId = server.gsfId
authSubToken = server.authSubToken

print('\nNow trying secondary login with ac2dm token and gsfId saved\n')
server = GooglePlayAPI('en_US', 'America/Virginia', 'sailfish')
server.login(None, None, gsfId, authSubToken)

# SEARCH
author_list = []
package_name_list = []
details_list = []
title_list = []
counter = 0
keywords = ['smart home', 'smarthome', 'home smart', 'smart home system', 'smart home device', 'smart home automate', 'home automation', 'automate home', 'home automation system', 'home automation device', 'smart system', 'internet of things', 'iot', 'web of things']

for keyword in keywords:
    apps = server.search(keyword, 3004, None)
    print("Fetching apps for ", keyword , "...")
    with open(keyword + '_jsondump.json', 'a') as json_file:
        json_file.write('[')
        with open(keyword + '_applist.csv', 'a') as the_file:
            for a in apps:
                counter +=1
                package_name = a['docId']
                if (counter %20 ==0):
                    print(time.strftime('%M:%S'), '...')

                if(package_name not in package_name_list):
                    title = a['title']
                    author = a['author']
                    author_without_comma = str.replace(str(author),',','-')

                    details = server.details(package_name)

                    description = str.replace(str(details['description']),',','-' )
                    description = description.encode('ascii',
                    'ignore').decode('ascii')
                    title_list.append(title)



                    json_file.write('[' +  json.dumps(a) + ',' +json.dumps(details) + ']')
                    json_file.write(',')

                    if(package_name not in package_name_list):
                        package_name_list.append(package_name)

                    if (author not in author_list):
                        author_list.append(author)
                    the_file.write(package_name.encode('ascii',
'ignore').decode('ascii')+ ',' + title.encode('ascii',
'ignore').decode('ascii')  + ',' + author_without_comma.encode('ascii',
'ignore').decode('ascii') +',' + description)
                    the_file.write('\n')
                    time.sleep(1)
        json_file.write(']')
        print('number of results: %d for %s -- Author List: %d' % (len(apps), keyword, len(author_list)))

with open('UniqueList.csv', 'a') as uniqueDump:
    for i in package_name_list:
        uniqueDump.write(i)
        uniqueDump.write('\n')





print("\n Title \n")
#Get unique authors --> this gives more than we ask
#Get unique packagenames
#See if keyword in details
keywords = ['smart home', 'smarthome', 'home smart', 'smart home system', 'smart home device', 'smart home automate', 'home automation', 'automate home', 'home automation system', 'home automation device', 'smart system', 'internet of things', ' iot ', 'web of things']
app_counter = 0
title_counter = 0
counter = 0
for title in title_list:
    new_apps = server.search(title, 3004, None)
    title_counter +=1
    batch = BATCH_SIZE_TITLE
    if(title_counter %BATCH_SIZE_TITLE ==0):
        batch += BATCH_SIZE_TITLE
    with open('title/'+ 'new' +'_'+ str(batch) + '_' + '_applist_secondary.csv', 'a') as title_file:
        with open('title/'+'new' +'_'+ str(batch) + '_' + '_secondary_jsondump.json', 'a') as json_file:
            print('number of results: %d for %s' % (len(new_apps), title))
            for a in new_apps:
                package_name = a['docId']
                title = a['title']
                author = a['author']
                if (counter %20 ==0):
                    print(time.strftime('%M:%S'), '...')
                author_without_comma = str.replace(str(author),',','-')
                details = server.details(package_name)
                details_description = details['description']
                description = str.replace(str(details['description']),',','-' )
                description = description.encode('ascii',
                'ignore').decode('ascii')
                #sleep(0.2)
                if(package_name not in package_name_list):
                    package_name_list.append(package_name)
                    for keyword in keywords:
                        if(keyword in details_description.lower()):
                            print(package_name)
                            app_counter +=1

                            title_file.write( package_name.encode('ascii',
'ignore').decode('ascii')+ ',' + title.encode('ascii',
'ignore').decode('ascii')  + ',' + author_without_comma.encode('ascii',
'ignore').decode('ascii')+',' + description)
                            title_file.write('\n')

                            json_file.write('[' + json.dumps(a)  + ',' + json.dumps(details) + ']')

#                            title_json_file.write(json.dumps(details))
                            json_file.write(',')
                            break
                sleep(1) #Because of the rate limit
            json_file.write(']')
