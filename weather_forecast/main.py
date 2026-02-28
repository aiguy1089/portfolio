"""
Main file to start the weather console-based program
Python conversion from Fortran
Western Governors University
Created September 2024

This is the main entry point for the weather program that:
1. Initializes weather data with temperature arrays and weather conditions
2. Creates a Weather object to manage the data
3. Calls methods to determine weather descriptions and display forecasts
"""

# Import the Weather class from the weather module
from weather import Weather


def main():
    """
    Main function that runs the weather program.
    
    This function:
    1. Sets up the initial weather data (temperatures, wind speed, weather code)
    2. Creates a Weather object with this data
    3. Determines the weather description based on the weather code
    4. Displays today's weather forecast
    5. Displays the complete weekly weather forecast
    """
    
    # Main variables - equivalent to Fortran declarations
    # fh = Fahrenheit High temperatures for each day of the week
    fh = [78, 76, 80, 82, 85, 79, 75]  # List of 7 high temperatures
    
    # fl = Fahrenheit Low temperatures for each day of the week  
    fl = [75, 70, 75, 76, 75, 70, 69]  # List of 7 low temperatures
    
    # ws = Wind Speed in MPH
    ws = 9  # Wind speed value
    
    # numberTemperatures = The number of temperatures (same for high and low arrays)
    number_temperatures = 7  # Constant representing array length
    
    # wc = Weather Code character
    wc = 'P'  # Weather code ('P' for Partly Cloudy)
    
    # Create Weather object - equivalent to Fortran's type(Weather) :: w
    # This calls the Weather class constructor (__init__ method)
    w = Weather(fh, fl, number_temperatures, ws, wc)
    
    # Call procedures to determine and display weather information
    
    # Determine weather description based on weather code
    # This sets the internal description attribute based on the weather code
    w.determine_description()
    
    # Display today's (Sunday's) weather forecast
    # Shows high and low temperature for the first day
    w.display_today_weather()
    
    # Display complete weekly weather forecast with statistics
    # Shows averages, extremes, and daily forecasts for all 7 days
    w.display_weekly_weather()


# Python idiom: only run main() if this file is executed directly
# (not when imported as a module)
if __name__ == "__main__":
    main()