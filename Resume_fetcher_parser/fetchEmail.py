from base64 import encode
import datetime

import os
from imbox import Imbox # pip install imbox
from urllib import request #pip install urllib

from pathlib import Path

from bs4 import BeautifulSoup #pip install bs4

# enable less secure apps on your google account
# https://myaccount.google.com/lesssecureapps

host = "imap.gmail.com"
username = "your email"
password = 'your key'
download_folder = "./outputs/"

if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)
    
mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)


#fetch mail you want to parse from last comments
messages = mail.messages(sent_from='bhanushali123krish@gmail.com',date__on=datetime.date(2022, 2, 12)) # defaults to inbox


def downloadFile(url,directory):
    filename = request.urlopen(request.Request(url)).info().get_filename()
    
                    
    request.urlretrieve(url,directory +filename)

    return filename

def getSetPath(data):
    
    firstPos = data.find(", has a new applicant!")
    print(firstPos)
    data = data[:firstPos]
    secondPos = data.find("Your job, ")
    print(secondPos)
    data = data[secondPos+10:]
    print(data)

    
    Path("./outputs/"+data).mkdir(parents=True, exist_ok=True)

    return "./outputs/"+data

def getAnchorHref(data):
    firstPos = data.find("Download resume:")
    # print(firstPos)
    data = data[firstPos + 17:]

    secondPos = data.find("Download resume")
    # print(secondPos)
    data = data[:secondPos]

    lastPos = data.rfind("<a")
    # print(lastPos)
    data = data[lastPos:] + '</a>'

    return data


def writeLogFiles(path,data):
	f = open(path,'a+')
	f.write(data) # get all .eml files in a list


for (uid, message) in messages:
    mail.mark_seen(uid) # optional, mark message as read
    
    print('Parsing Emails')

    email_items_html = message.body['html']
    email_items_html = email_items_html[1:]
    count = 0
    for emailEML in email_items_html:

       
        count+=1
        print(f'Email:{count}')
        # print(count)
        try:
            aTag = getAnchorHref(emailEML)
            directoryPath = getSetPath(emailEML)
            beautifulSoupText = BeautifulSoup(aTag, 'html.parser')
            url = beautifulSoupText.contents[0]['href'];
            fileName = downloadFile(url,directoryPath+'/')
            writeLogFiles('logs/success.txt',directoryPath+'/'+fileName+'\n')
        except:
                        #         
            
            # except:
            
            writeLogFiles('logs/error.txt',directoryPath + f'Please Refer email:{count}' + '\n')          
          








    



mail.logout()


"""
Available Message filters: 

# Gets all messages from the inbox
messages = mail.messages()

# Unread messages
messages = mail.messages(unread=True)

# Flagged messages
messages = mail.messages(flagged=True)

# Un-flagged messages
messages = mail.messages(unflagged=True)

# Messages sent FROM
messages = mail.messages(sent_from='sender@example.org')

# Messages sent TO
messages = mail.messages(sent_to='receiver@example.org')

# Messages received before specific date
messages = mail.messages(date__lt=datetime.date(2018, 7, 31))

# Messages received after specific date
messages = mail.messages(date__gt=datetime.date(2018, 7, 30))

# Messages received on a specific date
messages = mail.messages(date__on=datetime.date(2018, 7, 30))

# Messages whose subjects contain a string
messages = mail.messages(subject='Christmas')

# Messages from a specific folder
messages = mail.messages(folder='Social')
"""