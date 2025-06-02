import csv
import xml.etree.ElementTree as ET
import pandas as pd
import html
import re

# Your specified headers
headers = [
    "Id", "PostTypeId", "AcceptedAnswerId", "CreationDate", "Score", "ViewCount", "Body",
    "OwnerUserId", "LastEditorUserId", "LastEditDate", "LastActivityDate", "Title", "Tags",
    "AnswerCount", "CommentCount", "ContentLicense", "ParentId", "OwnerDisplayName",
    "ClosedDate", "LastEditorDisplayName", "CommunityOwnedDate", "FavoriteCount"
]

# Function to clean HTML
def regHtml(text):
    if not text:
        return ''
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)     # Remove HTML tags
    text = re.sub(r'\s+', ' ', text)        # Collapse all whitespace (incl. newlines, tabs)
    text = text.replace('"', "'")           # Replace double quotes
    return text.strip()

# Parse the XML file
def readFile(file):
    tree = ET.parse(file)
    return tree.getroot()

# Extract and clean rows
def parseLines(root):
    data = []
    for row in root.findall('row'):
        rowData = [row.attrib.get(h, '') for h in headers]

        # Clean HTML from Body (index 6) and Title (index 11)
        for i in [6, 11]:
            rowData[i] = regHtml(rowData[i])

        data.append(rowData)

    df = pd.DataFrame(data, columns=headers)
    df.to_csv('Posts.csv', index=False, quoting=csv.QUOTE_ALL, lineterminator="\r")
    print(f"Exported {len(df)} posts to Posts.csv")

# File path
file = "/Users/adilshamji/Documents/25-Data-mining-lab/Datasets/physics.stackexchange.com/Posts.xml"
root = readFile(file)
parseLines(root)
