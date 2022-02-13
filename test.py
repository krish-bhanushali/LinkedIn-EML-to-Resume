import email
from email import policy
from email.parser import BytesParser
import glob
import os
from requests import get  # to make GET request
import quopri

import urllib.request


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

path = './' # set this to "./" if in current directory

eml_files = glob.glob(path + '*.eml') # get all .eml files in a list
for eml_file in eml_files:
    with open(eml_file, 'rb') as fp:  # select a specific email file from the list
        name = fp.name # Get file name
        msg = BytesParser(policy=policy.default).parse(fp)
    text = msg.get_body(preferencelist=('plain')).get_content()
    fp.close()
 
    text = text.split("\n")
    print (name) # Get name of eml file
    print (text)
    
    downloadLink = ""

    for index in range(len(text)):
        if('Download resume:' in text[index]):
            print(text[index + 1])
            url = decoded_string = quopri.decodestring(text[index + 1])
            #download(text[index + 1], 'krish.pdf')
            urllib.request.urlretrieve(url, "mp3212.pdf")



            # try:
            #     with open(eml_file, 'r') as file:
            #         data = file.read()
                    
            #         aTag = getAnchorHref(data)
            #         directoryPath = getSetPath(data)
                    
            #         #print(data)

            #         decoded_string = quopri.decodestring(aTag)
            #         # print(decoded_string.decode('utf-8'))
            #         beautifulSoupText = BeautifulSoup(decoded_string.decode('utf-8'), 'html.parser')
                    
            #         url = beautifulSoupText.contents[0]['href'];
            #         downloadFile(url,directoryPath+'/')
                    
            #         writeLogFiles('logs/success.txt',eml_file+'\n')
            
            # except:
            #     writeLogFiles('logs/error.txt',eml_file+'\n')