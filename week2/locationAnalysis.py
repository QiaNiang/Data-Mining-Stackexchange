import re
import pandas as pd
import pycountry
from countryAbb import countryAbb
from typing import Optional
from collections import defaultdict
# 1. Load data
users = pd.read_csv("../data/Users.csv")


cities = pd.read_csv(
    "/Users/adilshamji/Documents/25-Data-mining-lab/Data-Mining-Stackexchange/week2/Data/worldcities_clean.csv",
    header=None,
    names=["city", "lat", "lng","country", "population"],
    dtype=str

)
users["Location"] = users["Location"].fillna("").str.lower()
cities["city"] = cities["city"].str.lower()
cities["country"] = cities["country"].str.lower()
#users.to_csv("users_100.csv", index = False)
city_to_country = dict(zip(cities["city"], cities["country"]))

abbreviations = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA",
    "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO",
    "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI",
    "WV", "WY",
    "DC",
    "AS", "GU", "MP", "PR", "VI",
]

abbreviations = [abbr.lower() for abbr in abbreviations]
contryAbb = {
    "uk": ['united kingdom', 'england']
}

country_set = set(city_to_country.values())

city_to_countries = defaultdict(set)
for city, country in zip(cities["city"], cities["country"]):
    city_to_countries[city].add(country)

flat_countryAbb = {}

for canonical, aliases in countryAbb.items():
    for alias in aliases:
        flat_countryAbb[alias.lower()] = canonical.lower()
    flat_countryAbb[canonical.lower()] = canonical.lower()


logLines=[]
matched_locations = []
def match_location(loc):
    countries = []
    for part in map(str.strip, loc.split(",")):
        part = part.lower()

        if part in flat_countryAbb:
            result = flat_countryAbb[part]
            matched_locations.append((loc, result))
            return result

        if part in abbreviations:
            matched_locations.append((loc, "united states"))
            return "united states"

        if part in country_set:
            matched_locations.append((loc, part))
            return part

        if part in city_to_countries:
            countries = list(city_to_countries[part])

    if len(countries) == 1:
        matched_locations.append((loc, countries[0]))
        return countries[0]
    elif len(countries) > 1:
        logLines.append(f"{loc}: {countries}")
    
    return None



    


#users["match"] = users["Location"].apply(match_location)
users["LocationCountry"] = users["Location"].apply(match_location)

users.to_csv("../data/UsersWithCountry.csv", index=False)


#print(users[["Location", "match"]])
with open("Data/ambiguous_matches.txt", "w") as f:
    f.write("\n".join(logLines))