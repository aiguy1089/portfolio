## Weather Forecast Program

A simple console application written in Python that models a 7‑day weather forecast. It demonstrates object‑oriented design, data processing, and includes a full test suite.

## Overview

This is a console-based weather forecast program written in Python that displays weather information for a 7-day period. The program demonstrates object-oriented programming principles, data processing, and statistical calculations.

## Program Features

- **Daily Weather Display**: Shows today's (Sunday) weather forecast
- **Weekly Weather Summary**: Displays complete 7-day forecast
- **Statistical Analysis**: Calculates average high/low temperatures
- **Temperature Extremes**: Finds highest and lowest temperatures for the week
- **Weather Descriptions**: Converts weather codes to readable descriptions
- **Comprehensive Testing**: Includes unit tests and integration tests

## Files Description

### Core Program Files

#### `main.py`
- **Purpose**: Main entry point for the weather program
- **Functionality**: 
  - Initializes weather data for the week
  - Creates Weather object with sample data
  - Orchestrates the display of weather information
  - Demonstrates the complete program workflow

#### `weather.py`
- **Purpose**: Contains the Weather class with all weather-related functionality
- **Key Components**:
  - **Weather Class**: Encapsulates weather data and operations
  - **Data Storage**: Stores high/low temperatures, wind speed, and weather codes
  - **Statistical Methods**: Calculates averages and finds extremes
  - **Display Methods**: Formats and displays weather information

#### `test_weather.py`
- **Purpose**: Comprehensive test suite for the Weather class
- **Test Coverage**:
  - Unit tests for all Weather class methods
  - Integration tests for complete workflow
  - Data validation and edge case testing

## Usage Instructions

### Running the Main Program

```bash
python main.py
```

### Running Tests

```bash
python test_weather.py
```

## License and Credits

**Language**: Python 3.x  
**Paradigm**: Object-Oriented Programming