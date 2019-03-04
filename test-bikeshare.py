## import all packages and functions
import time
import pandas as pd
import numpy as np


## import files
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'


def get_city():
    '''Asks the user for a city and returns the filename for
    that city's bike share data.
    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = input('\nHello! Let\'s explore some US bikeshare data! (Hit Return to proceed) ')

    city = city.lower()

    while True:
        city = input("Please choose between Chicago, New York City, or Washington: ")
        if city == "new york city" or city == "ny" or city == "nyc":
            print("You chose New York! Let's explore this location's bikeshare data!")
            return new_york_city
        if city == "chicago" or city == "chi" or city == "ch":
            print("You chose Chicago! Let's explore this location's bikeshare data!")
            return chicago
        elif city == "washington" or city == "wa":
            print("You chose Washington! Let's explore this location's bikeshare data!")
            return washington
        else:
            print ("Sorry, I did not understand your input: " + city + " Please try again.")

        city = city.lower()


def get_time_period():
    '''Asks the user for a time period and returns the specified filter.
    Args:
        none.
    Returns:
        (str) Time period information.
    '''
    print("Let's get started by choosing the Month or Date to filter the dataset.")

    while True:
        time_period = input("Choose a time filter between 'MONTH', 'DAY' of the week, or 'ALL' to see all of the data \n").lower()

        if time_period == "month":

            while True:
                filterByDayOfMonth = input("Do you wish to filter by day as well? ('YES'/'NO')\n").lower()

                if filterByDayOfMonth == "no":
                    print('Please proceed to select your month.')
                    return 'month'

                elif filterByDayOfMonth == "yes":
                   print ('Please proceed to select your month first and then your day in the following prompt.\n')
                   return 'day_of_month'

        if time_period == "d" or time_period == "day":
            print('Please proceed to select the day.\n')
            return 'day_of_week'
        elif time_period == "all":
            print("Let's look at all the data!")
            return "none"
        time_period = time_period.lower()


def get_month(month_):
    '''Asks the user for a month and returns the specified month.
    Args:
        month_ - the output from get_time_period()
    Returns:
        (str) Month information.
    '''
    if month_ == 'month':

        month = input("Please select a month. Your options are: January, February, March, April, May, June.\n")
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input("Sorry, I didn't understand your input. Please try again. \nYour options are: January, February, March, April, May, June\n")
        return month.strip().lower()
    else:
        return 'none'

def get_day_of_month(df, dayOfMonth_):
    """Asks the user for a month and a day of month, and returns both
    Args:
        dayOfMonth_ - the ouput of get_time_period()
        df - the dataframe with all bikedata
    Returns:
        list with Month and day information
    """
    monthAndDay = []

    if dayOfMonth_ == "day_of_month":

        month = get_month("month")
        monthAndDay.append(month)

        maxDayOfMonth = get_max_day_of_month(df, month)

        while (True):

            promptString = """Input the date number as an integer between 1 and """

            promptString  = promptString + str(maxDayOfMonth) + "\n"

            dayOfMonth = input(promptString)

            try:

                dayOfMonth = int(dayOfMonth)

                if 1 <= dayOfMonth <= maxDayOfMonth:
                    monthAndDay.append(dayOfMonth)
                    return monthAndDay

            except ValueError:
                print("That is not an integer. " + promptString)

    else:
        return 'none'

def get_day(day_of_week):
    '''Asks the user for a day and returns the specified day.
    Args:
        day_ - string - should data be filtered by day
    Returns:
        (str) Day information.
    '''
    if day_of_week == 'day_of_week':
        day = input('Which day of the week? Your options are: Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday.\n')
        while day.lower().strip() not in ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
            day = input('Please try again. Your options are Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday.\n')
        return day.lower().strip()
    else:
        return 'none'


def load_data(city):
    """
    Reads the city file name and loads it to a dataframe
    INPUT:
    city - path to the file as a string
    OUTPUT:
    df - dataframe to be used to calculate all stats
    """
    print('\nLoading the data...\n')
    df = pd.read_csv(city)

    #add datetime format to permit easy filtering
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #add auxiliary columns to aid filtering
    #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.dt.weekday_name.html
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df["day_of_month"] = df["Start Time"].dt.day

    return df
def apply_time_filters(df, time_period, month, dayOfWeek, monthAndDay):
    '''
    Filters the data according to the criteria specified by the user.
    INPUT:
    df           - city dataframe
    time_period  - string indicating the specified time period (either "month", "day_of_month", or "day_of_week")
    month        - string indicating the month used to filter the data
    dayOfWeek    - string indicating the week day used to filter the data
    dayOfMonth   - list indicating the month (at index [0]) used to filter the data
                    and the day number (at index [1])
    OUTPUT:
    df - dataframe to be used to calculate all aggregates that is filtered according to
         the specified time period
    '''


    print("Data loaded. Let's look at the stats... \n")
    #Filter by Month if required
    if time_period == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week if required
    if time_period == 'day_of_week':
        days = ['Monday', 'Tuesday',
        'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday']
        for d in days:
            if dayOfWeek.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]

    if time_period == "day_of_month":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = monthAndDay[0]
        month = months.index(month) + 1
        df = df[df['month']==month]
        day = monthAndDay[1]
        df = df[df['day_of_month'] == day]

    return df
def popular_month(df):
    '''What is the most popular month for start time?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        most_popular_month - string of most frequent month
    '''
    print('\nMost popular month for bike traveling (if month is selected, disregard this): ', end="");
    mnth = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_popular_month = months[mnth - 1].capitalize()
    return most_popular_month


def popular_day(df):
    '''What is the most popular day of week for start time?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        popular_day - string with name of day with most rides
    '''
    print('\nMost popular day for bike traveling: ', end="");
    most_pop_day = df['day_of_week'].value_counts().reset_index()['index'][0]
    return most_pop_day


def popular_hour(df):
    '''What is the most popular hour of day for start time?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        popular_hour - int of the most popular hour
    '''
    print('\nMost popular hour of the day for bike traveling: ', end="");
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]


def trip_duration(df):
    '''What is the total trip duration and average trip duration?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        tuple = total trip duration, average trip durations
        each is a pandas._libs.tslib.Timedelta objects
    '''
    print('\nWhat is the total traveling time & the average time spent on each trip?\n');
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    #sum for total trip time, mean for avg trip time

    total_travel_time = np.sum(df['Travel Time'])
    totalDays = str(total_travel_time).split()[0]
    print ("\nTotal travel time: " + totalDays + " days \n")

    average_travel_time = np.mean(df['Travel Time'])
    averageDays = str(average_travel_time).split()[0]
    print("Average traveling time " + averageDays + " days \n")

    return total_travel_time, average_travel_time

def popular_stations(df):
    '''What is the most popular start station and most popular end station?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        tuple - indicating most popular start and end stations
    '''
    print("\nThe most popular start station and the most popular end station is at ", end="");
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]

    return start_station


def popular_trip(df):
    '''What is the most popular trip?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        result - pandas.core.frame.DataFrame - with start, end, and number of trips for most popular trip
    '''
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nWhich trip route is the most popular from start station to end station?');
    return result


def users(df):
    '''What are the counts of each user type?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        users - pandas series with counts for each user type
    '''
    print('\nWho are the users and how many of each in each category?');

    return df['User Type'].value_counts()


def gender(df):
    '''What are the counts of gender?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        gender - pandas.core.series.Series counts for each gender
    '''
    try:
        print('\nHow many males and how many females participate in bikeshare?\n');
        return df['Gender'].value_counts()

    except:
        print('No data available.')


def birth_years(df):
    '''What is the earliest, latest, and most frequent birth year?
    INPUT:
        df - dataframe returned from apply_time_filters
    OUTPUT:
        tuple of earliest, latest, and most frequent year of birth
    '''
    try:
        print('\nWhat is the earliest, latest, and most frequent year of birth among the users?')
        earliest = np.min(df['Birth Year'])
        print ("\nEarliest year of birth is: " + str(int(earliest)) + "\n")
        latest = np.max(df['Birth Year'])
        print ("Latest year of birth is: " + str(int(latest)) + "\n")
        most_frequent= df['Birth Year'].mode()[0]
        print ("Most frequent year of birth is: " + str(int(most_frequent)) + "\n")
        return earliest, latest, most_frequent
    except:
        print('No available data for this period.')

def compute_stat(f, df):
    """
    Calculates the time it takes to commpute a stat
    INPUT:
      f  - the applied stats function
      df - the dataframe with all the data
    OUTPUT:
        prints to console, doesn't return a value
    """

    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("Computation took %s seconds." % (time.time() - start_time))

def get_max_day_of_month(df, month):
    """
    Gets the max day of the month
    INPUT:
      df - the city dataframe
      month - string of the selected month
    OUTPUT:
      maxDay - integer with the max day of the month
    """
    months = {"january": 1, "february": 2, "march": 3, "april":4, "may": 5, "june":6}
    df = df[df["month"] == months[month]]

    maxDay = max(df["day_of_month"])
    return maxDay

def display_raw_data(df):
    """
    Displays the data used to compute the stats
    Input:
        the dataframe with all the bikeshare data
    Returns:
       none
    """

    #omit auxiliary columns from visualization
    df = df.drop(['month', 'day_of_month'], axis = 1)

    rowIndex = 0

    seeData = input("\nBut first... Would you like to see rows of the data used to compute the stats? Input ('YES'/'NO') \n").lower()

    while True:

        if seeData == 'no':
            return

        if seeData == 'yes':
            print(df[rowIndex: rowIndex + 5])
            rowIndex = rowIndex + 5


        seeData = input("\nWould you like to see five more rows of the data used to compute the stats? Input ('YES'/'NO') \n").lower()

def stats():
    '''Calculates and prints out the descriptive statistics about a city
    and time period specified by the user via raw input.
    Args:
        none.
    Returns:
        none.
    '''
    city = get_city()
    df = load_data(city)
    time_period = get_time_period()
    month = get_month(time_period)
    day = get_day(time_period)
    monthAndDay = get_day_of_month(df, time_period)
    df = apply_time_filters(df, time_period, month, day, monthAndDay)
    display_raw_data(df)
    stat_function_list = [popular_month,
                          popular_day, popular_hour,
                          trip_duration, popular_trip,
                          popular_stations, users, birth_years, gender]

    for func in stat_function_list:
        compute_stat(func, df)

# Prompt user to restart to see data for another city
    restart = input("\nWould you like to perform another analysis? Input 'YES'/'NO'")
    if restart.upper() == 'YES':
        stats()

if __name__ == '__main__':
    stats()

## For more details for the time: https://docs.python.org/3/library/time.html
## For more details for pandas: http://pandas.pydata.org/pandas-docs/stable/user_guide/index.html
## For more details for numpy: https://docs.scipy.org/doc/numpy/reference/routines.html
