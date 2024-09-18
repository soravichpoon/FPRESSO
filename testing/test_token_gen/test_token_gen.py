import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sso_token_url = 'https://sso-service-hlcp4m5f5q-as.a.run.app/authenticate'

users = [
    {'username': 'user1', 'appNo': 'app1'},
    {'username': 'user2', 'appNo': 'app2'}
] * 500  # 10 pairs of user-app combinations

def generate_sso_token(user):
    response = requests.get(sso_token_url, headers={'username': user['username'], 'appNo': user['appNo']})
    if response.status_code == 200 and 'sso_token' in response.cookies:
        sso_token = response.cookies['sso_token']
        return {'username': user['username'], 'appNo': user['appNo'], 'sso_token': sso_token}
    return None

def test_token_generation(users):
    times = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        start_time = time.time()
        future_to_user = {executor.submit(generate_sso_token, user): user for user in users}
        for future in as_completed(future_to_user):
            result = future.result()
            if result is not None:
                times.append(result)
        end_time = time.time()
    total_time = end_time - start_time
    return times, total_time

if __name__ == "__main__":
    token_times, total_time = test_token_generation(users)

    successful_generations = len(token_times)

    print(f"Total Users = {len(users)}, Successful Token Generations = {successful_generations}, Total Time = {total_time:.4f} seconds")
