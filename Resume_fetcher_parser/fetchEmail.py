#INSTRUCTIONS
#PLEASE INSTALL FOLLOWING DEPENDENCIES
#pip install imbox
#pip install urllib
#pip install BeautifulSoup4

#pip install certifi

#Please go to My Accounts In Google
#turn on two step verification
#generate an app password
#enter it in place of password



#GO TO MESSAGEGS OBJECT 

from base64 import encode
import datetime





import os
from imbox import Imbox # pip install imbox
from urllib import request #pip install urllib

from pathlib import Path

from bs4 import BeautifulSoup #pip install bs4


host = "imap.gmail.com"
username = "email"
password = 'key'
download_folder = "./outputs/"

if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)
    
mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)


#fetch type of mail you want to select
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

#bellow mail fetches mail from nitin26aajtak@gmail.com and date after 12/2/2022
messages = mail.messages(sent_from='nitin26.aajtak@gmail.com',date__gt=datetime.date(2022, 2, 12)) # defaults to inbox


def downloadFile(url,directory):
    Path("./outputs/"+directory).mkdir(parents=True, exist_ok=True)
    filename = request.urlopen(request.Request(url)).info().get_filename()
    
                    
    request.urlretrieve(url,"./outputs/"+directory +filename)

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

def getPostApplied(data):
    allTags = BeautifulSoup(data, 'html.parser')
    h2 = allTags.find_all("h2")
    if(len(h2)>0):
        if(len(h2[0].contents) > 0):
            postA = getJobPost(h2[0].contents[0])
            print(postA)
            return postA


def getJobPost(post):
    return post.split(",")[1][1:]
    #print(allTags)

def getAnchorNew(data):
    allTags = BeautifulSoup(data, 'html.parser')
    
    
    
    #finds all the anchor tags 
    for anchor in allTags.find_all("a"):
        
        if(len(anchor.contents) > 1):
            #print(anchor.contents[1])
            all_tds_inside_anchor = anchor.contents[1].find_all("td")
            if(len(all_tds_inside_anchor)>0):
                #anchor.contents[1].find_all("td")[0].find_all("a")
                link_anchor_inside_td = all_tds_inside_anchor[0].find_all("a")
                if(len(link_anchor_inside_td)>0):
                    href_inside_anchor = link_anchor_inside_td[0]["href"]
                    return href_inside_anchor
           
   


def writeLogFiles(path,data):
	f = open(path,'a+')
	f.write(data) # get all .eml files in a list

count = 0
for (uid, message) in messages:
    mail.mark_seen(uid) # optional, mark message as read
    
    print('Parsing Emails')

    email_items_html = message.body['html']
    #email_items_html = email_items_html[1:]

    subject_of_email = message.subject

    count+=1
    for emailEML in email_items_html:

        try:
       
            
            print(f'Email:{count}')
            email_href = getAnchorNew(emailEML)
            postName = getPostApplied(emailEML)


            
            if(postName == 'Node.js Developer'):

            
                try:
                    
                    fileName = downloadFile(email_href,postName+'/')
                
                    writeLogFiles('logs/success.txt',f'\n=========================\n{count}) Successfully Done For Subject: {subject_of_email}\nlink:{email_href}\npost:{postName}\n=========================\n')
                except Exception as e:
                                # 
                    print(e)        
                    
                    # except:
                    
                    writeLogFiles('logs/error.txt',f'\n=========================\n{count}) Error {e} For Subject: {subject_of_email}\nlink:{email_href}\npost:{postName}\n=========================\n')          

        except Exception as e: 
            writeLogFiles('logs/error.txt',f'\n{count}) Error For Subject: {subject_of_email}\n Link may not be found here!')                    





       








    



mail.logout()


