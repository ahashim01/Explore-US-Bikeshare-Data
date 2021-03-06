import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    city = ""
    while city not in CITY_DATA:
        city = input('Would you like to see data for Chicago, New York or Washington?\n').lower()
        if city not in CITY_DATA:
            print('Invalid value, kindly choose from (chicago, new york city, washington)')
        else:
            print('Looks like you want to hear about {}!, If this is not true, restart program now!'.format(city.title()))
    
    # get user input for month (all, january, february, ... , june)
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    month = ""
    while month not in months:
        month = input("Do you want specific month or all? if not all please choose from\n ['all','january', 'february', 'march', 'april', 'may', 'june'] \n").lower()
        if month not in months:
            print('Invalid input Value')
            print()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ""
    while day not in days:
        day = input(
            "Do you want specific day or all? if not all please choose from\n  ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] \n"
        ).lower()
        if day not in days:
            print('Invalid input Value')
            print()
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
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[(df['month'] == month)]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[(df['day_of_week'] == day)]
    # print(df.head())
    return df 

def five_rows_data(df):
    show_five_row = input('Would you like to display 5 rows if data? if yes type yes\n').lower()
    if show_five_row == 'yes':
        print()
        head_or_tail = ""
        while head_or_tail not in ['head', 'tail']:
            head_or_tail = input("If you want to display first 5 rows type head, if you want to display last 5 rows type tail\n").lower()
            print(head_or_tail)
            if head_or_tail not in ['head', 'tail']:
                print('Invalid Value, kindly choose head or tail')
        if head_or_tail == 'head':
            print(df.head())
        else:
            print(df.tail())
    else:
        pass
            

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    print()
    print('The most common month:', calendar.month_name[df['month'].mode()[0]])
    print()

    # display the most common day of week
    print()
    print('The most common day of week:', df['day_of_week'].mode()[0])
    print()

    # display the most common start hour
    print()
    print('The most common start hour:',df['Start Time'].dt.hour.mode()[0])
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station:', df['Start Station'].mode()[0])


    # display most commonly used end station
    print('The most commonly used end station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    start_end_combination = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).keys()[0]
    print('The most frequent combination of start station and end station trip:', start_end_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time:', pd.Timedelta(seconds=df['Trip Duration'].sum()))

    # display mean travel time
    print('Mean Travel Time:', pd.Timedelta(seconds=df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df:
        print()
        print("Counts of user types:\n", df['User Type'].value_counts())
        print()
    else:
        print()
        print('The Used Data has no User Type data')
        print()
    # Display counts of gender
    if 'Gender' in df:
        print()
        print("Counts of user types:\n", df['Gender'].value_counts())
        print()
    else:
        print()
        print('The Used Data has no Gender data')
        print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print()
        print("Earlist birth Year:", df.sort_values('Birth Year')['Birth Year'].reset_index(drop=True)[0])
        print("Most Recent Birth Year:", df.sort_values('Birth Year',ascending=False)['Birth Year'].reset_index(drop=True)[0])
        print("The most common year of birth:", df['Birth Year'].mode())
        print()
    else:
        print()
        print('The Used Data has no Birth Year')
        print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.empty:
            print('DataFrame is empty!')
        else:
            five_rows_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
