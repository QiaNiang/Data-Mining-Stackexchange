import xml.etree.ElementTree as ET
import pandas as pd

# Parse the XML
tree = ET.parse('/Users/adilshamji/Documents/25-Data-mining-lab/Datasets/physics.stackexchange.com/Comments.xml')  # replace with your file path
root = tree.getroot()

# Extract all row attributes into a list of dicts
data = [row.attrib for row in root.findall('row')]

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('../data/Comments.csv', index=False)
