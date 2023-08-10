import argparse
import configparser
import csv
import logging
import requests
import sys


class WeatherAPI:
    def __init__(self):
        self.args = self.argument_parser()
        # Reading the api key from config.ini file
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.api_key = config.get('WeatherAPI', 'api_key')
        # Setting up log.txt file
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        log_file_handler = logging.FileHandler('log.txt')
        log_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger('').addHandler(log_file_handler)
        
    # Function to pass the arguments
    def argument_parser(self):
        try:
            parser = argparse.ArgumentParser(description='Fetch weather information for multiple locations.')
            # nargs='+' is used for multiple location names eg: Kalyan Thane
            parser.add_argument('-l', '--locations', nargs='+', help='List of locations (e.g., city names)')
            parser.add_argument('-d', '--days', type=int, default=3, help='Number of days for which to fetch weather data')
            return parser.parse_args()
        except Exception as e:
            self.log_exception(f"Error parsing command-line arguments: {str(e)}")
            raise e("Check the argument parser. argument_parser() is returning the error!!")

    # Function to get the weather data in json format
    def get_json_data(self):
        try:
            self.weather_data_list = []  # Clear the list for each location
            url = f"http://api.weatherapi.com/v1/forecast.json"
            params = {
                "key": self.api_key, 
                "q": self.location, 
                "days": self.args.days, 
                "aqi": "yes", 
                "alerts": "no"
            }
            response = requests.get(url, params = params)
            if response.status_code == 200:
                weather_data = response.json()
                self.weather_data_list.append(weather_data)
            else:
                self.log('error', f"Status code: {response.status_code}")
                self.log('error', "No data stored")
            return self.weather_data_list
        except Exception as e:
            self.log_exception('error',str(e))
            print(f"No Data available for {self.location} for past {self.args.days} days")
            raise e("Check the get_json_data(). It is returning the error!!")
            
    # Function to fetch the weather data
    def get_weather_data(self):
        try:
            for weather_data in self.weather_data_list:
                self.process_single_day_data(weather_data)
        except Exception as e:
            self.log_exception(f"Error processing weather data for {self.location}: {str(e)}")
            raise e("Check the get_weather_data(). It is returning the error!!")

    # Function to fetch single day data
    def process_single_day_data(self,weather_data):
        try:
            self.final_weather_data_list = []
            location = weather_data.get('location').get('name')
            self.log('info', f"Fetching weather information for {location}:")
            for day_data in weather_data.get('forecast').get('forecastday'):
                date_to_fetch = day_data.get('date')
                forecast_day = day_data.get('day')
                country = weather_data.get('location').get('country')
                city = location
                temp_c = forecast_day.get('avgtemp_c', "N/A")
                max_temp_c = forecast_day.get('maxtemp_c', "N/A")
                min_temp_c = forecast_day.get('mintemp_c', "N/A")
                humidity = forecast_day.get('avghumidity', "N/A")
                air_quality_details = forecast_day.get('air_quality', {}).get('co', "N/A")
                self.log('info', f"Date:{date_to_fetch}, Country: {country}, City: {city}, Avg Temp: {temp_c} C, Max_Temp: {max_temp_c} C, Min_Temp: {min_temp_c}, Humidity: {humidity}, Air Quality (Co2): {air_quality_details}")
                self.final_weather_data_list.append([date_to_fetch, country, city, temp_c, max_temp_c, min_temp_c, humidity, air_quality_details])
        except Exception as e:
            self.log_exception(f"Error processing weather data for {self.location}: {str(e)}")
            raise e("Check the process_single_day_data(). It is returning the error!!")

    # Function to set log levels
    def log(self,level,message):
        if level == 'info': 
            logging.info(message) 
        elif level == 'error': 
            logging.error(message) 
        elif level == 'debug': 
            logging.debug(message)
    
    # Function to log exceptions
    def log_exception(self, message, exception):
        self.log('error', f"{message}: {str(exception)}")
        sys.exit(1)

    # Function to save the data in a csv file
    def save_to_csv(self,filename = 'weather_data.csv'):
        try:
            header = ['Date', 'Country', 'City', 'Avg Temperature (C)', 'Max Temperature (C)', 'Min Temperature (C)', 'Humidity', 'Air Quality Co2']
            with open(filename, 'a', newline='') as csvfile:   
                csv_writer = csv.writer(csvfile)
                # Write the header only if the file is empty
                if csvfile.tell() == 0:
                    csv_writer.writerow(header)
                csv_writer.writerows(self.final_weather_data_list)
        except Exception as e:
            self.log_exception(f"Error saving data to weather_data.csv: {str(e)}")
            raise e("Check the save_to_csv(). It is returning the error!!")
            
    def main(self):
        try:
            for self.location in self.args.locations:
                self.get_json_data()
                self.get_weather_data()
                self.save_to_csv()
        except Exception as e:
            self.log_exception(f"Error executing main(): {str(e)}")


if __name__ == '__main__':
    weather_api = WeatherAPI()
    weather_api.main()
