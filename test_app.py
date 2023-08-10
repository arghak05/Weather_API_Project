import unittest
from unittest.mock import patch, MagicMock
from app import WeatherAPI


class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.weather_api = WeatherAPI()
        self.weather_api.location = 'london'
        self.weather_api.args = MagicMock(days=3)

    @patch('app.requests.get')
    def test_get_json_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'forecast': {'forecastday': [{'date': '2023-05-05', 'day': {'mintemp_c': '10', 'maxtemp_c': '20', 'avghumidity': '70'}}]}, 'location': {'name': 'London', 'country': 'UK'}, 'current': {'air_quality': {'co': '1'}}}
        mock_get.return_value = mock_response
        result = self.weather_api.get_json_data()
        expected = {'forecast': {'forecastday': [{'date': '2023-05-05', 'day': {'mintemp_c': '10', 'maxtemp_c': '20', 'avghumidity': '70'}}]}, 'location': {'name': 'London', 'country': 'UK'}, 'current': {'air_quality': {'co': '1'}}}
        self.assertEqual(result[0], expected)

    @patch('app.requests.get')
    def test_get_json_data_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        result = self.weather_api.get_json_data()
        expected = []
        self.assertEqual(result, expected)

    @patch('argparse.ArgumentParser.parse_args', return_value=('london', 3))
    def test_argument_parser(self, mock_parse_args):
        result = self.weather_api.argument_parser()
        self.assertEqual(result[0], 'london')
        self.assertEqual(result[1], 3)

if __name__ == '__main__':
    unittest.main()
