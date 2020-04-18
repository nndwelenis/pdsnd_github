import time
import pandas as pd
import numpy as np

# These are the files we will be using in this project
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

    # Function to filter the data we are interested in
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('-'*80)
    print('Hello! Let\'s have some fun exploring some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). We used a while loop to handle invalid inputs
    city = input("\nPlease enter city name (chicago, new york city, washington): ").lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("City name entered name is invalid! Please enter another name: ").lower()

    # get user input for months (all, january, february, ... , june)
    month = input("Please enter a month name in full (all, january,... , june): ").lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input("Month name entered is invalid! Please enter another month name: ").lower()

    # get user input for day of week (all, monday, tuesday, ... , sunday)
    day = input("Please enter a day of the week (all, monday,... , sunday): ").lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input("Day of the week entered is invalid! Please enter another day of the week: ").lower()

    print('-'*80)
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
    # load data into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' and 'End Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding data
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create a new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # Returns the selected file as a dataframe (df) with relevant columns
    return df

# Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Uses mode method to find the most popular month
    popular_month = df['month'].mode()[0]

    print(f"Most Popular Month (1 = January,...,6 = June): {popular_month}")

    #Uses mode method to find the most popular day
    popular_day = df['day_of_week'].mode()[0]

    print(f"\nMost Popular Day: {popular_day}")

    #Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #Uses mode method to find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print(f"\nMost Popular Start Hour: {popular_hour}")

    #Prints the time taken to perform the calculation
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

    # Function to calculate station related statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display the most commonly used start station
    print(f"\nThe most commonly used start station is: {(df['Start Station'].mode().values[0])}")

    # Display most commonly used end station
    print(f"\nThe most commonly used end station is: {(df['End Station'].mode().values[0])}")

    # Display most frequent combination of start station and end station trip. We start by creating a new table, which is a combination of 'start station' and 'end station'.
    df['routes'] = df['Start Station']+ " " + df['End Station']
    print(f"\nThe most common start and end station combination is: {(df['routes'].mode().values[0])}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Function for calculating trip duration related statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

#Convert the Start Time and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['duration'] = df['End Time'] - df['Start Time']


    # Displaying the total travel time
    print("The total travel time is: {}".format(
        str(df['duration'].sum()))
     )

    # Display the mean travel time
    print("The mean travel time is: {}".format(
        str(df['duration'].mean()))
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Displaying the user_statisics
def user_stats(df, city):

    """Displays statistics on bikeshare users."""


    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying the counts of user types
    print("The following are the counts in terms of types:")
    print(df['User Type'].value_counts())

    # Displaying the counts of gender

    if  city != 'washington':
        print("\nThe following are the counts in terms of gender:")
        print(df['Gender'].value_counts())

    # Displaying the earliest, most recent, and most common year of birth
    if city != 'washington':
        print("\nThe following is an analysis in terms of year of birth:")
        print("The earliest birth year is: {}".format(
            str(int(df['Birth Year'].min())))
        )
        print("The latest birth year is: {}".format(
            str(int(df['Birth Year'].max())))
        )
        print("The most common birth year is: {}".format(
            str(int(df['Birth Year'].mode().values[0])))
        )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

#REFERENCES
#1 https://stackoverflow.com/questions/48400250/subtract-two-objects-data-type-in-python
#2 https://stackoverflow.com/questions/26763344/convert-pandas-column-to-datetime
