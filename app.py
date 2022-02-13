from cmath import atan
from email import message, message_from_file
import email
import glob
import os
from bs4 import BeautifulSoup
import quopri
from urllib import request

from pathlib import Path



path = './input' # set this to "./" if in current directory

eml_files = glob.glob(path + '*.eml')

# Your job, Software Developer - Freshers, has a new applicant!

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


def downloadFile(url,directory):
    filename = request.urlopen(request.Request(url)).info().get_filename()
    
                    
    request.urlretrieve(url,directory +filename)

    return filename

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

def getResumesFromEml():
   
        for eml_file in eml_files:

            try:
                with open(eml_file, 'r') as file:
                    data = file.read()
                    
                    aTag = getAnchorHref(data)
                    directoryPath = getSetPath(data)
                    
                    #print(data)

                    decoded_string = quopri.decodestring(aTag)
                    # print(decoded_string.decode('utf-8'))
                    beautifulSoupText = BeautifulSoup(decoded_string.decode('utf-8'), 'html.parser')
                    
                    url = beautifulSoupText.contents[0]['href'];
                    downloadFile(url,directoryPath+'/')
                    
                    writeLogFiles('logs/success.txt',eml_file+'\n')
            
            except Exception as e:
                writeLogFiles('logs/error.txt',e+'\n' +eml_file+'\n')







   

        # urllib.request.urlretrieve(url, "hi.pdf")



getResumesFromEml()





