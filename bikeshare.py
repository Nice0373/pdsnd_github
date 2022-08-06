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
    city = input('Would you like to see data for Chicago, New York City, Washington ?').lower()          
    print("Looks like you want to hear about " + city + ' ! ')
    while city not in ['chicago','new york city','washington']:
        print("Don't have this city information")
        city = input('Would you like to see data for Chicago, New York City, Washington ?').lower() 
    # get user which filter they want (month,day,none)
    filter = input("Which filter do you want to use month, day, both, or none. Plese write the same as showing")
    # get user input for month (all, january, february, ... , june)
    if filter == 'month' :
        month = input('Which month? January, February, March, April, May, or June? Please type out the full month name.')
        day = 'all'
    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif filter == 'day' :
        day = input('Which day? Please type response as Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday')
        month = 'all'
    elif filter == 'both' :
        month = input('Which month? January, February, March, April, May, or June? Please type out the full month name.')
        day = input('Which day? Please type response as Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday')
    else :
        day = 'all'
        month ='all'


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
    df['day_of_week'] = df['Start Time'].dt.strftime("%w")

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)  + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the day of week to get the corresponding int
        days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        day = days.index(day) 
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == str(day)]

    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = months[popular_month - 1]
    print('Most Popular Month : ',popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    popular_day_of_week = days[int(popular_day_of_week )]
    print('Most Popular Day of Week : ',popular_day_of_week)

    # display the most common start hour
    popular_start_hour = df['Start Time'].mode()[0]
    print('Most Populat Start Hour : ',popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station : ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station : ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Destination'] = "Start : " + df['Start Station'] + "     " + "End : "+df['End Station']
    popular_destination = df['Destination'].mode()[0]
    print("Most Popular Destination : ",popular_destination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total Duration : ', total_travel)
    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('Mean Duration : ', mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    if city == 'chicago' or city == 'new york city':
    # Display counts of gender

        gender_types = df['Gender'].value_counts()
        print(gender_types)

    # Display earliest, most recent, and most common year of birth
        earliest_year = min(df['Birth Year'])
        print('Earliest Year : ',earliest_year)
        most_recent = max(df['Birth Year'])
        print('Most Recent Year : ',most_recent)
        most_comon = df['Birth Year'].mode()[0]
        print('Most Common : ',most_comon)
    else :
        print('There is no gender information and birth year information')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
#Show details of each user
def view_info(df):
    permission = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while (permission == 'yes'):
        end_loc = start_loc + 5 
        print(df.iloc[start_loc : end_loc ])
        start_loc += 5
        permission = input("Do you wish to continue?: ").lower()
    print("End of giving information")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        view_info(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
