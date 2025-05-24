
import pandas as pd
import sys
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from matplotlib.ticker import MaxNLocator
import pycountry
import matplotlib.dates as mdates
from datetime import datetime


def reputationPlot(df):
    repCol = df.iloc[:, 1]
    repCol = repCol[repCol > 1]
    

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

def logScaledViewsHistogram(df, index, title):
    views = pd.to_numeric(df.iloc[:, index], errors='coerce').dropna()
    views = views[views > 0]  # remove zeros to avoid log issues
    plt.hist(views, bins=100, edgecolor='black')
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=20))
    views = pd.to_numeric(df.iloc[:, index], errors='coerce').dropna()

    plt.yscale('log')  # or plt.xscale('log') if horizontal
    plt.title(f"{title} Distribution (Log-Scaled)")
    plt.xlabel(title)
    plt.ylabel("Frequency (log scale)")
    plt.grid(True)
    plt.show()

def zoomedViewsHistogram(df, index, viewsCap):
    views = pd.to_numeric(df.iloc[:, index], errors='coerce').dropna()
    views = views[ (views >0) & (views <= viewsCap)]
    plt.hist(views, bins=50, edgecolor='black')
    plt.title(f"Views Distribution (0–{str(viewsCap)} range) Log-Scaled")
    plt.xlabel("Views")
    plt.yscale('log')
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
    plt.barh(top_locations.index[::-1], top_locations.values[::-1]) 
    plt.title(f"Top {n} Most Common User Locations")
    plt.xlabel("Number of Users")
    plt.ylabel("Location")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def creationDateTrend(df):
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce')
    df = df.dropna(subset=['CreationDate'])

    # Group by month and count the number of accounts created per month
    df['YearMonth'] = df['CreationDate'].dt.to_period('M')
    monthly_signups = df.groupby('YearMonth').size()

    # Reset index and add a year column
    signup_counts_df = monthly_signups.reset_index(name='SignupCount')
    signup_counts_df['Year'] = signup_counts_df['YearMonth'].dt.year

    # Identify the months with the maximum and minimum signups each year
    max_months = signup_counts_df.loc[signup_counts_df.groupby('Year')['SignupCount'].idxmax()]
    min_months = signup_counts_df.loc[signup_counts_df.groupby('Year')['SignupCount'].idxmin()]

    # Plot
    plt.figure(figsize=(15, 6))
    plt.plot(signup_counts_df['YearMonth'].dt.to_timestamp(), signup_counts_df['SignupCount'],
             label="Monthly Signups", color='blue', linewidth=1.5)

    # Plot maximum and minimum months
    plt.plot(max_months['YearMonth'].dt.to_timestamp(), max_months['SignupCount'],
             'o', color='green', label='Yearly Maximum')
    plt.plot(min_months['YearMonth'].dt.to_timestamp(), min_months['SignupCount'],
             'o', color='red', label='Yearly Minimum')

    # Highlight the lockdown period (March 1 to June 30, 2020)
    lockdown_start = datetime(2020, 3, 1)
    lockdown_end = datetime(2020, 6, 30)
    plt.axvspan(lockdown_start, lockdown_end, color='gray', alpha=0.3, label='Global Lockdown (Mar–Jun 2020)')

    # Formatting
    plt.title("Monthly Account Signup Trend with Yearly Extremes")
    plt.xlabel("Year")
    plt.ylabel("Number of Accounts Created")
    plt.grid(True)
    plt.legend()

    # Set the x-axis to show yearly ticks only
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=0)

    plt.tight_layout()
    plt.show()

def creationMonthTrend(df):
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce')
    df = df.dropna(subset=['CreationDate'])

    # Extract month name from CreationDate
    df['Month'] = df['CreationDate'].dt.month_name()

    # Count users by month
    monthCounts = df['Month'].value_counts().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])

    plt.figure(figsize=(12, 5))
    plt.bar(monthCounts.index, monthCounts.values, color='skyblue', edgecolor='black')
    plt.title("Account Creations by Month (All Years Combined)")
    plt.xlabel("Month")
    plt.ylabel("Number of Accounts Created")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def cumulativeSignups(df):
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce')
    df = df.dropna(subset=['CreationDate'])

    # Sort by date and compute cumulative count
    df = df.sort_values('CreationDate')
    df['CumulativeCount'] = range(1, len(df) + 1)

    # Plot
    plt.figure(figsize=(15, 5))
    plt.plot(df['CreationDate'], df['CumulativeCount'], color='purple')
    plt.title("Cumulative Account Signups Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Accounts Created")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def detailedSignupTrends(df, year_ranges):
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce')
    df = df.dropna(subset=['CreationDate'])
    df['Year'] = df['CreationDate'].dt.year
    df['Month'] = df['CreationDate'].dt.month

    monthly_signups = df.groupby(['Year', 'Month']).size().reset_index(name='SignupCount')

    for start_year, end_year in year_ranges:
        subset = monthly_signups[(monthly_signups['Year'] >= start_year) & (monthly_signups['Year'] <= end_year)]

        pivot = subset.pivot(index='Month', columns='Year', values='SignupCount').sort_index()

        plt.figure(figsize=(10, 5))
        pivot.plot(marker='o', ax=plt.gca())
        plt.title(f"Monthly Signups per Year: {start_year}–{end_year}")
        plt.xlabel("Month")
        plt.ylabel("Number of Signups")
        plt.xticks(ticks=range(1, 13), labels=[
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ])
        plt.grid(True)
        plt.legend(title='Year')
        plt.tight_layout()
        plt.show()

def checkId(df):
    return df['AccountId'].isnull().sum()

def main(path):
    df = pd.read_csv(path)
    # # Reputation plot, boxplot
    reputationPlot(df)
    # # User views, histogram 
    # logScaledViewsHistogram(df, 8, "User views")
    # # Zoomed in of the <= 2400 views
    # zoomedViewsHistogram(df, 8, 2400)
    # # Zoomed in 800
    zoomedViewsHistogram(df, 8, 150)
    # # Upvotes
    # logScaledViewsHistogram(df, 9, "Upvotes")
    # # Downvotes
    # logScaledViewsHistogram(df, 10, "DownVotes")
    # topNCommon(df, 4)
    # creationDateTrend(df)
    # creationMonthTrend(df)
    # cumulativeSignups(df)
    # detailedSignupTrends(df, [(2016, 2017), (2018, 2019), (2020, 2021)])
    print(checkId(df))









PATH = "Users.csv"
main(PATH)