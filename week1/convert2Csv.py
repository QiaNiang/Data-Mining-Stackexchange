""" File to convert to csv. 
"""
import csv
import sys
import xml.etree.ElementTree as ET
import pandas as pd
import html
import re
import matplotlib.dates as mdates
headers = [
  "Id", "Reputation", "CreationDate", "DisplayName", "LastAccessDate",
  "WebsiteUrl", "Location", "AboutMe", "Views", "UpVotes", "DownVotes", "AccountId"
]

def regHtml(text):
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('\n', ' ').replace('\r', ' ').replace('"', "'")
    return text.strip()

def readFile(file):
    tree = ET.parse(file)
    root = tree.getroot()
    return root
numbers = [9466, 37296, 96630, 121995, 140393, 95949, 150567, 126792, 136093, 144336, 164550, 167287, 167399, 150567, 126792, 136093, 144336, 164550, 167287, 167399, 214859, 228628, 259813, 220577, 276981, 254242, 300548, 300548, 301386, 291437, 328894, 382805]


def parseLines(root):
    data= []
    count = 0
    for row in root.findall('row'):
        flag = False
        if int(row.attrib.get("Id", "0")) in numbers:
            flag = True
            count +=1 
        rowData = [row.attrib.get(h, '') for h in headers]
        if(flag):
            print(rowData[3])
        
        rowData[7] = regHtml(rowData[7])

        data.append(rowData)
    df = pd.DataFrame(data, columns= headers)
    df.to_csv('Users.csv', index=False, quoting=csv.QUOTE_ALL, lineterminator="\r")

    print("count", count)




def main(file):
    root = readFile(file)
    parseLines(root)
    


file = "/Users/adilshamji/Documents/Data-mining-lab/Datasets/physics.stackexchange.com/Users.xml"
main(file)

