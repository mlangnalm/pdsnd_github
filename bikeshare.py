import time
import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago', 'new york city', 'washington', 'all']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
dow = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filterchicago by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #user inputs city
    while True:
        city = input('Which city would you like to see data from: {} : '.format(cities.title()))
        city = city.lower()
        if city in cities:
            print('Thank you, valid city input.')
            break
        else:
            print('Invalid city input. Please try again.')

    #user inputs month
    while True:
        month = input('Enter a month {} : '.format(months.title()))
        month = month.lower()
        if month in months:
            print('Thank you, valid month input.')
            break
        else:
            print('Invalid month input.  Please try again.')

    #user inputs day of week
    while True:
        day = input('Enter a day of the week ' + str(dow).title() +': ')
        day = day.lower()
        if day in dow:
            print('Thank you, valid day of the week input.')
            break
        else:
            print('Invalid day of the week input.  Please try again.')

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
    if city == 'all':
        df = pd.DataFrame([])
        for index in CITY_DATA.keys():
            df = df.append(pd.read_csv(CITY_DATA[index]), ignore_index = True)
    else:
        df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        day = dow.index(day)
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_count = df['month'].value_counts()
    common_month = months[month_count[month_count == max(month_count)].index[0] - 1].title()
    print('Most Common Month: {}'.format(common_month))

    # TO DO: display the most common day of week
    day_count = df['day_of_week'].value_counts()
    common_day = dow[day_count[day_count == max(day_count)].index[0]].title()
    print('Most Common Day: {}'.format(common_day))

    # TO DO: display the most common start hour
    hour_count = df['hour'].value_counts()
    common_hour = hour_count[hour_count == max(hour_count)].index[0]
    print('Most Common Start Time Hour: {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most popular start station is: {}'.format(common_start_station))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most popular end station is: {}'.format(common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    start_end_count = df.groupby(['Start Station'])['End Station'].value_counts()
    max_start_end = start_end_count[start_end_count == max(start_end_count)].index[0]
    print('Most popular start and end station combination is:\n    Start Station: {}\n    End Station: {}'.format(max_start_end[0], max_start_end[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    sum_trip_duration = df['Trip Duration'].sum()
    print('Sum Total Trip Duration: {} seconds.'.format(sum_trip_duration))

    # TO DO: display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print('Mean Average Trip Duration: {} seconds.'.format(mean_trip_duration))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print('User Types:')
    for i in range(len(user_type)):
        print('{}: {}'.format(user_type.index[i], user_type[i]))
    print('')

    try:  #washington does not have gender information
        # TO DO: Display counts of gender
        df['Gender'] = df['Gender'].fillna('Unknown')
        gender_count = df['Gender'].value_counts()
        print('User Gender Count:')
        for i in range (len(gender_count)):
            print('{}: {}'.format(gender_count.index[i], gender_count[i]))
        print('')
    except KeyError:
        print('No user gender information available.\n')


    try:  #washington does not have birth year information
        # TO DO: Display earliest, most recent, and most common year of birth
        df['Birth Year'].dropna(axis = 0, inplace = True) # drop NaN birth year values messing up .mode() calc
        earliest_by = min(df['Birth Year'])
        recent_by = max(df['Birth Year'])
        common_by = df['Birth Year'].mode()
        print('Birth Year Information:')
        print('Earliest Birth Year: {} \nMost Recent Birth Year: {} \nMost Common Birth Year: {}'.format(int(earliest_by), int(recent_by), int(common_by)))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        print('No user birth year information available.')


def raw_data_output(df):
    i = 0
    while True:
        output = input('Would you like to see raw data (y/n)? ')
        output = output.lower()
        if output == 'y':
            print(df[i:i+5])
            i += 5
        elif output == 'n':
            break
        else:
            print('Please provide valid input (y/n):\n')


def main():
    restart = 'x'
    while restart != 'no':
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_output(df)


        while (restart.lower() != 'no'):
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if (restart.lower() != 'yes' and restart.lower() != 'no'):
                print('Please provide valid input')
                continue
            elif restart.lower() == 'yes':
                print('\n')
                break
            elif restart.lower() == 'no':
                break

if __name__ == "__main__":
	main()
