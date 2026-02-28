"""
Weather module for the Weather program
Python conversion from Fortran
Western Governors University
Created September 2024

This module contains the Weather class that manages weather data including:
- High and low temperatures for a week
- Wind speed
- Weather codes and descriptions
- Various calculations and display methods
"""

from typing import List


class Weather:
    """
    Weather class to store and manage weather data for a week.
    
    This class encapsulates weather information including temperature arrays,
    wind speed, weather codes, and provides methods for calculations and display.
    """
    
    def __init__(self, fh_array: List[int], fl_array: List[int], 
                 array_lengths: int, ws: int, wc: str):
        """
        Initialize Weather object with temperature and weather data.
        
        Args:
            fh_array: List of 7 high temperatures in Fahrenheit
            fl_array: List of 7 low temperatures in Fahrenheit  
            array_lengths: Number of temperature readings (should be 7)
            ws: Wind speed in MPH
            wc: Weather code character ('S', 'P', 'C', 'N')
        """
        # Private attributes (Python convention: prefix with underscore)
        self._f_high_array: List[int] = [0] * 7  # Initialize with zeros
        self._f_low_array: List[int] = [0] * 7   # Initialize with zeros
        self._ws_mph: int = 0                    # Wind speed in MPH
        self._number_temperatures: int = 0       # Number of temperature readings
        self._w_code: str = ' '                  # Weather code character
        self._description: str = ""              # Weather description string
        
        # Set the number of temperatures
        self._number_temperatures = array_lengths
        
        # Load the weather data using helper method
        self._load_weekly_weather(fh_array, fl_array, ws, wc)
    
    def _load_weekly_weather(self, fh_array: List[int], fl_array: List[int], 
                            ws: int, wc: str) -> None:
        """
        Load weekly weather data into the object's private attributes.
        
        This method populates the internal arrays and variables with the provided data.
        
        Args:
            fh_array: High temperature array
            fl_array: Low temperature array
            ws: Wind speed
            wc: Weather code
        """
        # Copy the temperature arrays (defensive copying)
        self._f_high_array = fh_array.copy()
        self._f_low_array = fl_array.copy()
        
        # Set wind speed and weather code
        self._ws_mph = ws
        self._w_code = wc
    
    def calculate_average_fahrenheit_high_temp(self) -> float:
        """
        Calculate the average of all high temperatures for the week.
        
        Returns:
            float: Average high temperature in Fahrenheit
        """
        # Sum all high temperatures using Python's built-in sum function
        hi_sum = sum(self._f_high_array)
        
        # Calculate average by dividing sum by number of temperatures
        # Convert to float for precise division
        avg_hi = float(hi_sum) / self._number_temperatures
        
        return avg_hi
    
    def calculate_average_fahrenheit_low_temp(self) -> float:
        """
        Calculate the average of all low temperatures for the week.
        
        Returns:
            float: Average low temperature in Fahrenheit
        """
        # Sum all low temperatures
        low_sum = sum(self._f_low_array)
        
        # Calculate average by dividing sum by number of temperatures
        avg_low = float(low_sum) / self._number_temperatures
        
        return avg_low
    
    def find_weekly_fahrenheit_high_temp(self) -> int:
        """
        Find the highest temperature from all high temperatures in the week.
        
        Returns:
            int: Highest temperature in Fahrenheit
        """
        # Start with the first temperature as the initial highest
        highest_temp = self._f_high_array[0]
        
        # Loop through remaining temperatures (starting from index 1)
        for day_count in range(1, self._number_temperatures):
            # If current temperature is higher than recorded highest, update it
            if self._f_high_array[day_count] > highest_temp:
                highest_temp = self._f_high_array[day_count]
        
        return highest_temp
    
    def find_weekly_fahrenheit_low_temp(self) -> int:
        """
        Find the lowest temperature from all low temperatures in the week.
        
        Returns:
            int: Lowest temperature in Fahrenheit
        """
        # Start with the first temperature as the initial lowest
        lowest_temp = self._f_low_array[0]
        
        # Loop through remaining temperatures (starting from index 1)
        for day_count in range(1, self._number_temperatures):
            # If current temperature is lower than recorded lowest, update it
            if self._f_low_array[day_count] < lowest_temp:
                lowest_temp = self._f_low_array[day_count]
        
        return lowest_temp
    
    def determine_description(self) -> None:
        """
        Determine weather description based on weather code.
        
        This method sets the internal description based on the weather code:
        - 'S': SUNNY
        - 'P': PARTLY CLOUDY  
        - 'C': CLOUDY
        - 'N': CLEAR
        """
        # Use dictionary mapping for cleaner code (equivalent to Fortran's select case)
        weather_descriptions = {
            'S': "SUNNY",
            'P': "PARTLY CLOUDY", 
            'C': "CLOUDY",
            'N': "CLEAR"
        }
        
        # Get description from dictionary, default to empty string if code not found
        self._description = weather_descriptions.get(self._w_code, "")
    
    def display_today_weather(self) -> None:
        """
        Display today's (Sunday's) weather forecast.
        
        Shows the high and low temperature for the first day (index 0).
        """
        print("SUNDAY FORECAST")
        # Display high and low temperatures for Sunday (first day, index 0)
        print(f"High: {self._f_high_array[0]} (F) Low: {self._f_low_array[0]} (F)")
        print()  # Empty line for formatting
    
    def display_weekly_weather(self) -> None:
        """
        Display complete weekly weather forecast with statistics.
        
        Shows:
        - Average high and low temperatures
        - Highest and lowest weekly temperatures
        - Daily forecast for each day of the week
        """
        # Define day names array (equivalent to Fortran's character array)
        days = ["Sunday   ", "Monday   ", "Tuesday  ", "Wednesday", 
                "Thursday ", "Friday   ", "Saturday "]
        
        print("THE WEEKLY FORECAST")
        
        # Display average temperatures (calling the calculation methods)
        print(f"Average Hi:  {self.calculate_average_fahrenheit_high_temp()}")
        print(f"Average Low: {self.calculate_average_fahrenheit_low_temp()}")
        print()  # Empty line
        
        # Display extreme temperatures for the week
        print(f"Highest Weekly Temperature: {self.find_weekly_fahrenheit_high_temp()} (F) ")
        print(f"Lowest Weekly Temperature:  {self.find_weekly_fahrenheit_low_temp()} (F) ")
        print()  # Empty line
        
        # Loop through each day and display its forecast
        for i in range(self._number_temperatures):
            print(days[i])
            # Display high and low for current day
            print(f"High: {self._f_high_array[i]} (F) Low: {self._f_low_array[i]} (F)")
            print()  # Empty line for formatting