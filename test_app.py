import unittest
from unittest.mock import patch, MagicMock
from app import WeatherAPI


class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.weather_api = WeatherAPI()

    @patch('requests.get')
    def test_get_json_data_success(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'forecast': {'forecastday': [{'date': '2023-08-06', 'day': {'mintemp_c': '10', 'maxtemp_c': '20', 'avghumidity': '70'}}]}, 'location': {'name': 'London', 'country': 'UK'}, 'current': {'air_quality': {'co': '1'}}}
        mock_requests.return_value = mock_response
        location = "London"
        api_key = "12345678901234567890"
        days = 3
        result = self.weather_api.get_json_data(api_key, location, days)
        expected = {'forecast': {'forecastday': [{'date': '2023-08-06', 'day': {'mintemp_c': '10', 'maxtemp_c': '20', 'avghumidity': '70'}}]}, 'location': {'name': 'London', 'country': 'UK'}, 'current': {'air_quality': {'co': '1'}}}
        self.assertEqual(result[0], expected)

    @patch('requests.get')
    def test_get_json_data_failure(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = []
        mock_requests.return_value = mock_response
        location = "unknown_city"
        api_key = "12345678901234567890"
        days = 3
        result = self.weather_api.get_json_data(api_key, location, days)
        expected = []
        self.assertEqual(result, expected)

    @patch('argparse.ArgumentParser.parse_args', return_value=('London', 3))
    def test_argument_parser(self, mock_parse_args):
        result = self.weather_api.argument_parser()
        self.assertEqual(result[0], 'London')
        self.assertEqual(result[1], 3)

if __name__ == '__main__':
    unittest.main()
