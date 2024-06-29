from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import requests

# URL for token verification
verification_url = 'https://app1-test-hlcp4m5f5q-as.a.run.app/protected'

# Warm-up requests count
warm_up_requests = 10

# Simulate multiple users making requests to the protected endpoint
def verify_token():
    start_time = time.time()
    response = requests.get(verification_url)
    end_time = time.time()

    if response.status_code == 200:
        verification_time = end_time - start_time
        return verification_time
    else:
        return None

def warm_up():
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(verify_token) for _ in range(warm_up_requests)]
        for future in as_completed(futures):
            future.result()  # We don't care about the result for warm-up

def test_token_verification(num_users):
    times = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(verify_token) for _ in range(num_users)]
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                times.append(result)
    
    successful_verifications = len(times)
    average_time = sum(times) / successful_verifications if successful_verifications > 0 else 0

    return successful_verifications, average_time

if __name__ == "__main__":
    num_users_list = [500, 1000]  # List of concurrent users to test
    num_iterations = 3  # Number of iterations for each user count

    for num_users in num_users_list:
        total_times = []
        total_successful_verifications = 0

        for _ in range(num_iterations):
            print(f"Warming up for {num_users} users...")
            warm_up()

            print(f"Starting actual test for {num_users} users...")
            successful_verifications, average_time = test_token_verification(num_users)
            total_times.append(average_time)
            total_successful_verifications += successful_verifications

            print(f"Iteration completed for {num_users} users")
            print("-----------------------------------------------------------")

        overall_average_time = sum(total_times) / num_iterations if num_iterations > 0 else 0

        print(f"Total Users = {num_users}, Successful Token Verifications = {total_successful_verifications // num_iterations}, Average Token Verification Time = {overall_average_time:.4f} seconds")
        print("===========================================================")
