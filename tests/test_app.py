import unittest
from unittest.mock import patch, MagicMock
from app import send_request, test_api

class TestAPI(unittest.TestCase):

    @patch('subprocess.run')
    def test_send_request(self, mock_run):
        # Mock the subprocess.run response for the curl command
        mock_response = MagicMock()
        mock_response.stdout = '{"id": 1, "title": "foo", "userId": 1}'
        mock_status_code = MagicMock()
        mock_status_code.stdout = '200'

        mock_run.side_effect = [mock_response, mock_status_code]

        status_code, response_json = send_request("https://jsonplaceholder.typicode.com/posts/1")
        self.assertEqual(status_code, 200)
        self.assertIn('id', response_json)
        self.assertIn('title', response_json)
        self.assertIn('userId', response_json)

    @patch('app.send_request')
    def test_test_api(self, mock_send_request):
        mock_send_request.return_value = (200, {"id": 1, "title": "foo", "userId": 1})
        with patch('builtins.print') as mock_print:
            test_api()
            mock_print.assert_any_call("Test 1: HTTP status code 200 - PASSED")
            mock_print.assert_any_call("Test 1: JSON response contains required keys - PASSED")

if __name__ == "__main__":
    unittest.main()
