"""
Test file for the Weather program
Python conversion from Fortran
Western Governors University
Created September 2024

This file contains comprehensive tests for the Weather class to ensure:
1. Proper initialization of Weather objects
2. Correct calculation of temperature averages
3. Accurate finding of extreme temperatures
4. Proper weather description determination
5. Correct display functionality
"""

import unittest
from io import StringIO
import sys
from weather import Weather


class TestWeather(unittest.TestCase):
    """
    Test class for Weather functionality.
    
    This class contains unit tests that verify all methods of the Weather class
    work correctly with various input scenarios.
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        
        This method runs before each test and creates a standard Weather object
        with known data for testing purposes.
        """
        # Test data - same as in the original Fortran program
        self.fh_test = [78, 76, 80, 82, 85, 79, 75]  # High temperatures
        self.fl_test = [75, 70, 75, 76, 75, 70, 69]  # Low temperatures
        self.ws_test = 9                              # Wind speed
        self.wc_test = 'P'                           # Weather code
        self.num_temps = 7                           # Number of temperatures
        
        # Create Weather object for testing
        self.weather = Weather(self.fh_test, self.fl_test, self.num_temps, 
                              self.ws_test, self.wc_test)
    
    def test_weather_initialization(self):
        """
        Test that Weather object initializes correctly.
        
        Verifies that:
        - Temperature arrays are properly stored
        - Wind speed is correctly set
        - Weather code is properly assigned
        - Number of temperatures is accurate
        """
        # Test that the weather object was created successfully
        self.assertIsInstance(self.weather, Weather)
        
        # Test that internal data matches input data
        # Note: We can't directly access private attributes, so we test through methods
        self.assertEqual(self.weather._number_temperatures, 7)
        self.assertEqual(self.weather._ws_mph, 9)
        self.assertEqual(self.weather._w_code, 'P')
    
    def test_calculate_average_fahrenheit_high_temp(self):
        """
        Test calculation of average high temperature.
        
        Manually calculates expected average and compares with method result.
        Expected: (78 + 76 + 80 + 82 + 85 + 79 + 75) / 7 = 555 / 7 = 79.28571...
        """
        # Calculate expected average manually
        expected_avg = sum(self.fh_test) / len(self.fh_test)
        
        # Get actual average from method
        actual_avg = self.weather.calculate_average_fahrenheit_high_temp()
        
        # Compare with small tolerance for floating point precision
        self.assertAlmostEqual(actual_avg, expected_avg, places=5)
        
        # Also test with known value
        self.assertAlmostEqual(actual_avg, 79.28571428571429, places=5)
    
    def test_calculate_average_fahrenheit_low_temp(self):
        """
        Test calculation of average low temperature.
        
        Manually calculates expected average and compares with method result.
        Expected: (75 + 70 + 75 + 76 + 75 + 70 + 69) / 7 = 510 / 7 = 72.857...
        """
        # Calculate expected average manually
        expected_avg = sum(self.fl_test) / len(self.fl_test)
        
        # Get actual average from method
        actual_avg = self.weather.calculate_average_fahrenheit_low_temp()
        
        # Compare with small tolerance for floating point precision
        self.assertAlmostEqual(actual_avg, expected_avg, places=5)
        
        # Also test with known value
        self.assertAlmostEqual(actual_avg, 72.85714285714286, places=5)
    
    def test_find_weekly_fahrenheit_high_temp(self):
        """
        Test finding the highest temperature of the week.
        
        From test data [78, 76, 80, 82, 85, 79, 75], the highest should be 85.
        """
        # Expected highest temperature from our test data
        expected_high = max(self.fh_test)  # Should be 85
        
        # Get actual highest from method
        actual_high = self.weather.find_weekly_fahrenheit_high_temp()
        
        # Compare results
        self.assertEqual(actual_high, expected_high)
        self.assertEqual(actual_high, 85)
    
    def test_find_weekly_fahrenheit_low_temp(self):
        """
        Test finding the lowest temperature of the week.
        
        From test data [75, 70, 75, 76, 75, 70, 69], the lowest should be 69.
        """
        # Expected lowest temperature from our test data
        expected_low = min(self.fl_test)  # Should be 69
        
        # Get actual lowest from method
        actual_low = self.weather.find_weekly_fahrenheit_low_temp()
        
        # Compare results
        self.assertEqual(actual_low, expected_low)
        self.assertEqual(actual_low, 69)
    
    def test_determine_description(self):
        """
        Test weather description determination for all weather codes.
        
        Tests each weather code ('S', 'P', 'C', 'N') to ensure correct descriptions.
        """
        # Test cases: (weather_code, expected_description)
        test_cases = [
            ('S', "SUNNY"),
            ('P', "PARTLY CLOUDY"),
            ('C', "CLOUDY"),
            ('N', "CLEAR")
        ]
        
        for weather_code, expected_desc in test_cases:
            # Create weather object with specific weather code
            test_weather = Weather(self.fh_test, self.fl_test, self.num_temps, 
                                 self.ws_test, weather_code)
            
            # Call determine_description method
            test_weather.determine_description()
            
            # Check that description was set correctly
            self.assertEqual(test_weather._description, expected_desc)
    
    def test_display_today_weather(self):
        """
        Test today's weather display output.
        
        Captures printed output and verifies it contains expected information.
        """
        # Capture stdout to test print statements
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Call the display method
        self.weather.display_today_weather()
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # Get the captured output
        output = captured_output.getvalue()
        
        # Check that output contains expected elements
        self.assertIn("SUNDAY FORECAST", output)
        self.assertIn("High: 78", output)  # First high temp
        self.assertIn("Low: 75", output)   # First low temp
        self.assertIn("(F)", output)       # Fahrenheit indicator
    
    def test_display_weekly_weather(self):
        """
        Test weekly weather display output.
        
        Captures printed output and verifies it contains all expected information.
        """
        # First determine description so it's set for display
        self.weather.determine_description()
        
        # Capture stdout to test print statements
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Call the display method
        self.weather.display_weekly_weather()
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # Get the captured output
        output = captured_output.getvalue()
        
        # Check that output contains expected elements
        self.assertIn("THE WEEKLY FORECAST", output)
        self.assertIn("Average Hi:", output)
        self.assertIn("Average Low:", output)
        self.assertIn("Highest Weekly Temperature: 85", output)
        self.assertIn("Lowest Weekly Temperature:  69", output)
        
        # Check that all days are displayed
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for day in days:
            self.assertIn(day, output)
    
    def test_edge_cases(self):
        """
        Test edge cases and boundary conditions.
        
        Tests scenarios like:
        - All temperatures the same
        - Single temperature arrays
        - Invalid weather codes
        """
        # Test with all same temperatures
        same_temps_high = [75, 75, 75, 75, 75, 75, 75]
        same_temps_low = [70, 70, 70, 70, 70, 70, 70]
        
        same_weather = Weather(same_temps_high, same_temps_low, 7, 5, 'S')
        
        # Average should equal the constant temperature
        self.assertEqual(same_weather.calculate_average_fahrenheit_high_temp(), 75.0)
        self.assertEqual(same_weather.calculate_average_fahrenheit_low_temp(), 70.0)
        
        # Min and max should be the same
        self.assertEqual(same_weather.find_weekly_fahrenheit_high_temp(), 75)
        self.assertEqual(same_weather.find_weekly_fahrenheit_low_temp(), 70)
        
        # Test invalid weather code (should result in empty description)
        invalid_weather = Weather(same_temps_high, same_temps_low, 7, 5, 'X')
        invalid_weather.determine_description()
        self.assertEqual(invalid_weather._description, "")


def run_tests():
    """
    Function to run all tests and display results.
    
    This function creates a test suite and runs all the test methods,
    providing detailed output about test results.
    """
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestWeather)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED!")
        
    return result.wasSuccessful()


# Run tests if this file is executed directly
if __name__ == "__main__":
    run_tests()