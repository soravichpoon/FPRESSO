import requests
import timeit
from threading import Thread

def send_verify_request(apps):
    url = 'https://sso-test-swlzbjlflq-as.a.run.app/verify'  # SSO service verify endpoint
    token = {'sso_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTcxNDQ1ODAyN30.pryvdAJO8pCO2_I-sfVXOb3TW0FOn7KExwKewMacvso'}  # Replace with a valid token
    headers = {'appNo': apps}  # Specify the app number in the header
    try:
        response = requests.get(url, headers=headers, cookies=token)
        return response.status_code, response.json()
    except requests.RequestException as e:
        return None, {'error': str(e)}

def run_test(app):
    response = send_verify_request(app)
    print(f"Response for {app}: {response}")

def test_performance(apps, num_runs):
    threads = []
    
    # Record the start time
    start_time = timeit.default_timer()
    
    for i in range(num_runs):
        for app in apps:
            # Create and start a thread for each verification request
            thread = Thread(target=run_test, args=(app,))
            threads.append(thread)
            thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    # Record the total time elapsed
    total_time = timeit.default_timer() - start_time
    print(f"Total time for {num_runs*len(apps_to_test)} runs per app: {total_time:.4f} seconds.")

if __name__ == '__main__':
    apps_to_test = ['app1', 'app2']  # List of app numbers to test
    # apps_to_test = ['5201', '5202']
    test_performance(apps_to_test, num_runs=10)  # Specify number of runs as needed
