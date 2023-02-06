import time
import pandas as pd

CITY_DATA = { 'Chicago': 'chicago.csv','New York City': 'new_york_city.csv',
'Washington': 'washington.csv' }
months=["All","January","February","March","April","May","June"]
days=["All","Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday","Sunday"]


def get_filters():
    """Function to get filters data and to evaluate user inputs"""
    print('\x1b[2;30;44mHello! Let\'s explore some US bikeshare data!\033[0m\n\n')

    #1st, Enter and evaluate the name of the city.
    print("Enter the name of the city you want to explore")
    city=" ".join(input("You can enter'New York City','Chicago', or 'Washington': ").title().split())
    while city not in CITY_DATA :
        city=" ".join(input("\x1b[0;31;47mPlease, Enter a valid city name:\033[0m ").title().split())
    
    #2nd, Enter and evaluate the name of the month.
    print("\n\nEnter the month you want to explore")
    month=input("You can enter either 'All' or 'January' to 'June': ").title()
    while month not in months :
        month=input("\x1b[0;31;47mPlease, Enter a valid month name:\033[0m ").title()
    
    #3rd, Enter and evaluate the name of the day.
    print("\n\nEnter the day you want to explore")
    day=input("You can enter either 'All' or 'Monday' to 'Sunday': ").title()
    while day not in days :
        day=input("\x1b[0;31;47mPlease, Enter a valid day:\033[0m ").title()
        #day=day.title()
    print('-'*40)
    return city,month,day


# Create the main DataFrame to be analyzed!.
def load_data(city,month,day): 
    """Function to create a dataframe according to user inputs"""
    # Creat a data frame with required city information.
    df=pd.read_csv(CITY_DATA[city])
    # Convert the values of "Start Time" column to datetimelike values.
    df["Start Time"]=pd.to_datetime(df["Start Time"])
    # Create a new column "Month" with values of month full name.
    df["Month"]=df["Start Time"].dt.month_name()
    # To filter the data using month name:
    if month in months[1:]:
        df=df[df["Month"]==month]
    # Create a new column "Day" with values of day full name.
    df["Day"]=df["Start Time"].dt.day_name()
    # To filter the data using day name:
    if day in days[1:]:
        df=df[df["Day"]==day]
    # Create a new column called "Start Hour" as it's needed by time_stats()
    df["Start Hour"]=df["Start Time"].dt.hour
    
    return df

def time_stats(df): #
    """Displays statistics on the most frequent times of travel."""

    print('\n\x1b[1;37;42mCalculating The Most Frequent Times of Travel...\033[0m\n')
    start_time = time.time()

    # display the most common month
    print(f"The most common month is:\n{df['Month'].mode()[0]}\n")

    # display the most common day of week
    print(f"The most common day of week is:\n{df['Day'].mode()[0]}\n")

    # display the most common start hour
    print(f"The most common start hour is:\n{df['Start Hour'].mode()[0]}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n\x1b[1;37;42mCalculating The Most Popular Stations and Trip...\033[0m\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"The most commonly used start station is:\n{df['Start Station'].mode()[0]}\n")

    # display most commonly used end station
    print(f"The most commonly used end station is:\n{df['End Station'].mode()[0]}\n")

    # display most frequent combination of start station and end station trip
    print(f"The most frequent combination of start station and end station trip is:\n{(df['Start Station']+' : '+df['End Station']).mode()[0]}\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n\x1b[1;37;42mCalculating Trip Duration...\033[0m\n')
    start_time = time.time()

    # display total travel time
    print(f"The total travel time = {round(df['Trip Duration'].sum())} seconds\n")

    # display mean travel time rounded to the nearest hundredth.
    print(f"The mean travel time = {round(df['Trip Duration'].mean())} seconds\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\n\x1b[1;37;42mCalculating User Stats...\033[0m\n')
    start_time = time.time()

    # Display counts of user types
    print(f"Counts of user types:\n{df['User Type'].value_counts().to_string()}\n")


    # Display counts of gender
    if city != 'Washington':
        print(f"Counts of user gender:\n{df['Gender'].value_counts().to_string()}\n")

# Display earliest, most recent, and most common year of birth in a form of int.
        print(f"The earliest year of birth is:     {int(df['Birth Year'].min())}\n")
        print(f"The most recent year of birth is:  {int(df['Birth Year'].max())}\n")
        print(f"The most common year of birth is:  {int(df['Birth Year'].mode())}\n")

    else:
        print("\x1b[0;31;47mSorry!, No information availabe about the gender & birth year for 'Washington'\033[0m")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    """Displays raw data of bikeshare users."""

    df=pd.read_csv(CITY_DATA[city])
    print('\n\x1b[1;37;42mRaw data is available to check... \033[0m\n')
    x=input("May you want to have a look on the raw data? Type yes or no: ".lower())
    if x != 'yes':
        print("\x1b[1;37;45mSkipping...\033[0m")

    else:
        i=0
        while x=='yes':
            print(df.iloc[i:i+5])
            x=input("do you wish to display more? Type yes or no:\n".lower())
            i+=5

            if x != 'yes':
                print("\x1b[1;37;45mDisplay of the raw data is ended!\033[0m")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)  #Due to "Washington" special case, we need to add city as a function argument.
        display_raw_data(city)
        restart = input('\n\x1b[1;37;43mWould you like to restart? Enter yes or no.\033[0m\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
