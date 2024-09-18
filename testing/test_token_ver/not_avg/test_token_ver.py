from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import requests

# URL for token verification
verification_url = 'https://app1-test-hlcp4m5f5q-as.a.run.app/protected'

# Simulate multiple users making requests to the protected endpoint
def verify_token():
    start_time = time.time()
    response = requests.get(verification_url)
    end_time = time.time()

    if response.status_code == 200:
        return end_time - start_time
    else:
        return None

def test_token_verification(num_users):
    times = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(verify_token) for _ in range(num_users)]
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                times.append(result)
    end_time = time.time()
    total_time = end_time - start_time
    return times, total_time

if __name__ == "__main__":
    num_users = 1000  # Number of concurrent users

    verification_times, total_time = test_token_verification(num_users)

    total_users = num_users
    successful_verifications = len(verification_times)

    print(f"Total Users = {total_users}, Successful Token Verifications = {successful_verifications}, Total Time = {total_time:.4f} seconds")
