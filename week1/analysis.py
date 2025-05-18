
import pandas as pd
import sys
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from matplotlib.ticker import MaxNLocator
import pycountry


def reputationPlot(df):
    repCol = df.iloc[:, 1]
    repCol = repCol[repCol > 0]

    stats = {
        'min': repCol.min(),
        'q1': repCol.quantile(0.25),
        'median': repCol.median(),
        'mean': repCol.mean(),
        'q3': repCol.quantile(0.75),
        'max': repCol.max()
    }
    plt.boxplot(repCol, vert=False)
    plt.title("Reputation Boxplot")
    plt.xlabel("Reputation")
    plt.grid(True)

    for label, val in stats.items():
        plt.axvline(val, linestyle='--', label=f'{label}: {val:.1f}')

    plt.legend(loc='upper right')
    plt.show()

def logScaledViewsHistogram(df, index):
    views = pd.to_numeric(df.iloc[:, index], errors='coerce').dropna()
    views = views[views > 0]  # remove zeros to avoid log issues
    plt.hist(views, bins=100, edgecolor='black')
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=20))
    views = pd.to_numeric(df.iloc[:, index], errors='coerce').dropna()

    plt.yscale('log')  # or plt.xscale('log') if horizontal
    plt.title("Views Distribution (Log-Scaled)")
    plt.xlabel("Views")
    plt.ylabel("Frequency (log scale)")
    plt.grid(True)
    plt.show()

def zoomedViewsHistogram(df, index):
    views = pd.to_numeric(df.iloc[:, index], errors='coerce').dropna()
    views = views[ (views >0) & (views <= 2400)]
    plt.hist(views, bins=50, edgecolor='black')
    plt.title("Views Distribution (0–2400 range)")
    plt.xlabel("Views")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

def topNCommon(df, n):
    #Index 6
    #countries = [c.name for c in pycountry.countries]

    locations = df.iloc[:, 6].dropna()
    
    unique=locations.unique()
    top_locations = locations.value_counts().head(n)
    with open("unique_locations.txt", "w") as f:
        for loc in unique:
            f.write(f"{loc}\n")
    plt.barh(top_locations.index[::-1], top_locations.values[::-1])  # reverse for descending order
    plt.title(f"Top {n} Most Common User Locations")
    plt.xlabel("Number of Users")
    plt.ylabel("Location")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main(path):
    df = pd.read_csv(path)
    # Reputation plot, boxplot
    #reputationPlot(df)
    # User views, histogram 
    #logScaledViewsHistogram(df, 8)
    # Zoomed in of the <= 2400 views
    #zoomedViewsHistogram(df, 8)
    # Upvotes
    #logScaledViewsHistogram(df, 9)
    # Downvotes
    # logScaledViewsHistogram(df, 10)
    topNCommon(df, 5)







PATH = "Users.csv"
main(PATH)