import argparse
import configparser
import csv
import logging
import requests
import sys



class WeatherAPI:
    def __init__(self):
        # Parse command-line arguments
        self.args = self.argument_parser()
        

    # Function to pass the arguments
    def argument_parser(self):
        try:
            parser = argparse.ArgumentParser(description='Fetch weather information for multiple locations.')
            # nargs='+' is used for multiple location names eg: Kalyan Thane
            parser.add_argument('--locations', nargs='+', help='List of locations (e.g., city names)')
            parser.add_argument('--days', type=int, default=3, help='Number of days for which to fetch weather data')
            return parser.parse_args()
        except Exception as e:
            self.log_error(f"Error parsing command-line arguments: {str(e)}")
            sys.exit(0)

    # Function to get the weather data in json format
    def get_json_data(self, api_key, location, days):
        try:
            self.weather_data_list = []  # Clear the list for each location
            url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days={days}&aqi=yes&alerts=no"
            #url = f"http://api.weatherapi.com/v1/forecast.json?key=75ed65ab0d864c1ca5483719232407&q=London&days=3&aqi=yes&alerts=no"
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
                self.weather_data_list.append(weather_data)
            else:
                self.log_error("No data stored")
            return self.weather_data_list
        except Exception as e:
            print(e)
            sys.exit(0)

    # Function to fetch the weather data
    def get_weather_data(self):
        self.final_weather_data_list = []
        try:
            for weather_data in self.weather_data_list:
                location = weather_data['location']['name']
                self.log_info(f"Fetching weather information for {location}:")
                for day_data in weather_data['forecast']['forecastday']:
                    date_to_fetch = day_data['date']
                    forecast_day = day_data['day']
                    country = weather_data['location']['country']
                    city = location
                    temp_c = forecast_day.get('avgtemp_c', "N/A")
                    max_temp_c = forecast_day.get('maxtemp_c', "N/A")
                    min_temp_c = forecast_day.get('mintemp_c', "N/A")
                    humidity = forecast_day.get('avghumidity', "N/A")
                    air_quality_details = forecast_day.get('air_quality', {}).get('co', "N/A")
                    self.log_info(f"Date:{date_to_fetch}, Country: {country}, City: {city}, Avg Temp: {temp_c} C, Max_Temp: {max_temp_c} C, Min_Temp: {min_temp_c}, Humidity: {humidity}, Air Quality (Co2): {air_quality_details}")
                    self.final_weather_data_list.append([date_to_fetch, country, city, temp_c, max_temp_c, min_temp_c, humidity, air_quality_details])
        except Exception as e:
            self.log_error(f"Error processing weather data for {self.location}: {str(e)}")
            sys.exit(0)

    # Function for INFO log
    def log_info(self, message):
        try:
            logging.info(message)
        except Exception as e:
            print(f"Error logging INFO: {str(e)}")

    # Function for ERROR log
    def log_error(self, message):
        try:
            logging.error(message)
        except Exception as e:
            print(f"Error logging ERROR: {str(e)}")

    # Reading the API Key from the config.ini file
    def read_config_file(self):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            self.api_key = config.get('WeatherAPI', 'api_key')
        except Exception as e:
            self.log_debug(f"Error reading config file: {str(e)}")

    # Function to save the data in a csv file
    def save_to_csv(self):
        try:
            header = ['Date', 'Country', 'City', 'Avg Temperature (C)', 'Max Temperature (C)', 'Min Temperature (C)', 'Humidity', 'Air Quality Co2']
            with open('weather_data.csv', 'a', newline='') as csvfile:   
                csv_writer = csv.writer(csvfile)
                # Write the header only if the file is empty
                if csvfile.tell() == 0:
                    csv_writer.writerow(header)
                csv_writer.writerows(self.final_weather_data_list)
        except Exception as e:
            self.log_error(f"Error saving data to weather_data.csv: {str(e)}")
            sys.exit(0)

    # Function to create a log.txt file
    def setup_logging(self):
        try:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            log_file_handler = logging.FileHandler('log.txt')
            log_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logging.getLogger('').addHandler(log_file_handler)
        except Exception as e:
            print(f"Error setting up logging: {str(e)}")

    def main(self):
        try:
            self.setup_logging()
            self.read_config_file()
            for self.location in self.args.locations:
                self.get_json_data(self.api_key, self.location, self.args.days)
                self.get_weather_data()
                self.save_to_csv()
        except Exception as e:
            self.log_error(f"Error executing main(): {str(e)}")


if __name__ == '__main__':
    weather_api = WeatherAPI()
    weather_api.main()
