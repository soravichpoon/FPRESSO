import requests
import timeit
from threading import Thread

def send_verify_request(apps):
    url = 'https://sso-service-swlzbjlflq-as.a.run.app/verify'
    cookies = {'sso_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsInJvbGUiOnsiYXBwMSI6eyJyb2xlIjoiYWRtaW4ifSwiYXBwMiI6eyJyb2xlIjoidXNlciJ9LCJhcHAzIjp7InJvbGUiOiJ1c2VyIn19LCJleHAiOjE3MTQ1MTk2NDZ9.AqgaRrkvFjcAx2ZLHpx4Pp1j0nwrN0Cy9zowuM7LajM'}
    headers = {'appNo': apps}
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        return response.status_code, response.json()
    except requests.RequestException as e:
        return None, {'error': str(e)}

def run_test(app):
    """Function to run a verification test and print the results."""
    response = send_verify_request(app)
    print(f"Response for {app}: {response}")

def test_performance(apps, num_runs):
    """Function to measure performance of verification requests."""
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
    test_performance(apps_to_test, num_runs=25)  # Specify number of runs as needed



# def run_test(app):
#     response = send_verify_request(app)
#     print(f"Response for {app}: {response}")

# def test_performance():
#     number_of_runs = 1
#     threads = []
    # i = 1
    # start_time = timeit.default_timer()
    # while i <= 10:
    #     thread = Thread(target=run_test, args=(f'app{i}',))
    #     threads.append(thread)
    #     thread.start()
    #     i+=1

    # for thread in threads:
    #     thread.join()
    
    # total_time = timeit.default_timer() - start_time
    # print(f"Total time for {number_of_runs} runs: {total_time:.4f} seconds.")

# if __name__ == '__main__':
#     test_performance()