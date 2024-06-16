import subprocess
import json

def send_request(endpoint):
    try:
        # Wykonanie żądania HTTP za pomocą curl
        response = subprocess.run(['curl', '-s', endpoint], capture_output=True, text=True)
        response_text = response.stdout

        # Sprawdzenie statusu HTTP
        status_code_response = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', endpoint], capture_output=True, text=True)
        status_code = int(status_code_response.stdout)

        # Parsowanie odpowiedzi JSON
        response_json = json.loads(response_text)
        return status_code, response_json
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON response from {endpoint}")
        return None, None

def test_api():
    base_url = "https://jsonplaceholder.typicode.com"
    endpoints = [
        "/posts/1",
        "/users/1",
        "/comments/1"
    ]
    
    tests_passed = 0

    for i, endpoint in enumerate(endpoints, start=1):
        full_url = base_url + endpoint
        status_code, response_json = send_request(full_url)

        if status_code == 200 and response_json:
            print(f"Test {i}: HTTP status code {status_code} - PASSED")

            # Sprawdzenie kluczowych elementów w odpowiedzi JSON
            keys_to_check = ['id', 'title', 'userId']
            if endpoint.startswith("/users"):
                keys_to_check = ['id']
            elif endpoint.startswith("/comments"):
                keys_to_check = ['id', 'postId']

            if all(key in response_json for key in keys_to_check):
                print(f"Test {i}: JSON response contains required keys - PASSED")
                tests_passed += 1
            else:
                print(f"Test {i}: JSON response missing required keys - FAILED")
        else:
            print(f"Test {i}: HTTP status code {status_code} - FAILED")

    print(f"\nSummary: {tests_passed} out of {len(endpoints)} tests PASSED")

if __name__ == "__main__":
    test_api()
