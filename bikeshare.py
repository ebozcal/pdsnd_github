# -*- coding: utf-8 -*-
"""Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KBd1Z_IGBUVY5zekPr5kmCwVuSnycMUY
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New york city OR Washington? Type 'none' for no time filter: ").lower()
    while city not in ['chicago','new york city', 'washington']:
      city = input("Please enter a city name as 'chicago', 'new york city' or 'washington'")

    i = 0
    while input("Would you like to see 5 lines of raw data? Please enter 'yes' or 'no' :").lower() == "yes":
      print(pd.read_csv(CITY_DATA[city])[i:i+5])
      i +=5
      continue

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    # get user input for month (all, january, february, ... , june)
    filtering_option = input("Would you like to filter the data by 'month', 'day', 'both' or 'not at all'? ").lower()

    if filtering_option.lower()=='month':
      month = input("Which month? - January, February, March, April, May, or June?: ").lower()
      while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
        month = input("Your input is invalid! Please enter a  month as January, February, March, April, May, or June: ").lower()
      day=None
      month = months.index(month) + 1

    elif filtering_option.lower()=='day':
      month = None
      day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?: ").title()
     

    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif filtering_option.lower()=='both':
      month = input("Which month - January, February, March, April, May, or June?: ").lower()
      day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?: ").title()
      
      month = months.index(month) + 1

    else:
      month  = None
      day = None

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month == None and day == None :
      df=df
      
    elif day == None:
      df = df[df['month'] == month] 

    elif month == None:
      df = df[df['day_of_week'] == day]

    else:
      df = df[df['month']==month]
      df = df[df['day_of_week']==day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    # display the most common month
    print('The most common month:', months[df['month'].mode()[0]-1])

    # display the most common day of week
    print('The most common day of week:', df['day_of_week'].mode()[0])

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is:", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most commonly used end station is:", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df["combined_stations"] = df['Start Station'] + ", " + df['End Station']
    print("The most frequent combination of start station and end station trip: {}".format(df['combined_stations'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Trip_time'] = df['End Time'] -df['Start Time'] 
    print("The total travel time is:",  df['Trip_time'].sum())

    # display mean travel time
    print("The average travel time is:",  df['Trip_time'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
   
    print("The counts of user types are: \n", df['User Type'].value_counts())
    # Display counts of gender
    print("The counts of genders are:\n", df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    print("The earliest year of birth is:", int(df['Birth Year'].min()))
    print("The most recent year of birth is:", int(df['Birth Year'].max()))
    print("The most common year of birth is:", int(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city == "chicago" or city == "new york city":
          user_stats(df)
        else:
          break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
  main()

