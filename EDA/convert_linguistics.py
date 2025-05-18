import xml.etree.ElementTree as ET
import pandas as pd
import os
from bs4 import BeautifulSoup  #to remove html tags

xml_folder = "/Users/qianiang/Library/CloudStorage/OneDrive-TUM/Studium/Data-Mining/physics.stackexchange.com"
csv_folder = "/Users/qianiang/Library/CloudStorage/OneDrive-TUM/Studium/Data-Mining/physics.stackexchange.com/CSV"

os.makedirs(csv_folder, exist_ok=True)

# get all xml files
xml_files = [f for f in os.listdir(xml_folder) if f.endswith(".xml")]

def clean_html(text):
    return BeautifulSoup(text, "html.parser").get_text()

for xml_file in xml_files:
    xml_path = os.path.join(xml_folder, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    data = [row.attrib for row in root.findall("row")]  # each entry
    df = pd.DataFrame(data)

    if 'Body' in df.columns:
        df['Body'] = df['Body'].apply(clean_html)

    csv_filename = xml_file.replace(".xml", ".csv")
    csv_path = os.path.join(csv_folder, csv_filename)
    df.to_csv(csv_path, index=False)
    print(f"saved done: {csv_filename}, row * column: {df.shape}")
