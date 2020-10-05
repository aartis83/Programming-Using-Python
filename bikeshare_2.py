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
    city_name = ''
    while city_name.lower() not in CITY_DATA.keys():
        city_name = input("Would you like to see bikeshare data for Chicago, New York city or"
                      " Washington? Please pick your choice :\n")
        if city_name.lower() in CITY_DATA.keys():
            city = city_name.lower()
        else:
            print("Not a valid input. Please input either "
                  "Chicago, New York, or Washington.")
    print("You have chosen {} as your city.\n".format(city_name.lower()))

    # get user input for month (all, january, february, ... , june)
    # Dictionary that stores months from Jan to june and all options
    MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june','all']
    month_name = ''
    while month_name.lower() not in MONTH_DATA:
        month_name = input("\nEnter the name of the month from january to june to filter data or Enter"
                            " all to apply no filter:\n")
        if month_name.lower() in MONTH_DATA:
            month = month_name.lower()
        else:
            print("Not a valid input. Please input either all"
                      " or months january, february ,march ,april, may, june.")
    print("You have chosen {} as your month.\n".format(month_name.lower()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # LIST to store weekdays and all option
    DAY_DATA =   ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                   'Friday','Saturday','All']
    day_name = ''
    while day_name.lower() not in DAY_DATA:
        day_name = input("\nEnter the name of the day to filter data or Enter"
                            " all to apply no filter:\n")
        if day_name.lower() in DAY_DATA:
            day = day_name.lower()
        else:
            print("Not a valid input. Please input either all"
                      "or days from Sunday to Saturday.")
    print("You have chosen {} as your day.\n".format(day_name.title()))
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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular month:', popular_month)
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular day:', popular_day)
    # display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)
    # display most frequent combination of start station and end station trip
    # concatenate two columns of dataframe with space
    # Assign the result to a new column 'Start To End'
    # Find frequent combination by using Mode of start and end stations
    df['Start To End'] = df['Start Station'] + ' to ' + df['End Station']
    popular_combo_station = df['Start To End'].mode()[0]
    print('Most frequent combination Station:', popular_combo_station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    #converts total time into minutes and seconds
    minutes,seconds = divmod(total_time,60)
    #further converts minutes into hours and minutes
    hours,minutes = divmod(minutes,60)
    print("The total travel time is {} hours,{} minutes and {} seconds.".format(hours,minutes,seconds))
    # display mean travel time
    average_time = round(df['Trip Duration'].mean())
    mins,secs = divmod(total_time,60)
    hrs,mins = divmod(minutes,60)
    print("The mean travel time is {} hours,{} minutes and {} seconds.".format(hrs,mins,secs))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print("The user type by count:{}".format(user_type))
    print("Warning : Gender info may not be available")

    # Display counts of gender
    try:
        gender_type = df['Gender'].value_counts()
        print("The gender type by count:{}".format(gender_type))
    except:
        print("Gender info unavailable")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print("The earliest year of birth:{}\nThe most recent year of birth:{}"
        "\nThe most common year of birth:{}".format(earliest,most_recent,common_year))
    except:
        print("Birth details unavailable")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        Displays 5 (show_rows) lines, then asks if they would like to see 5 more.
    Returns:
        None.
    """
    print(df.head())
    next = 0
    while True:
        raw_data = input('\nTo view the next five rows of data please enter yes or no.\n')
        if raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
