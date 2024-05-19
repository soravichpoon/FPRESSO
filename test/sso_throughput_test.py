import asyncio
import aiohttp
import time
import random
import matplotlib.pyplot as plt

# List of SSO tokens for different users
sso_tokens = [
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsInJvbGUiOnsiYXBwMSI6eyJyb2xlIjoiYWRtaW4ifSwiYXBwMiI6eyJyb2xlIjoidXNlciJ9LCJhcHAzIjp7InJvbGUiOiJ1c2VyIn19LCJleHAiOjE3MTYxMTYxNzV9.gtZq-gGTHrPwHJ3pYV7J1eX4me_2ZthP1_UJIF81_4Q',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMiIsInJvbGUiOnsiYXBwMSI6eyJyb2xlIjoidXNlciJ9LCJhcHAyIjp7InJvbGUiOiJhZG1pbiJ9LCJhcHAzIjp7InJvbGUiOiJ1c2VyIn19LCJleHAiOjE3MTYxMTYzODR9.S37VKSeRplG4LBNWv-VFWnyd0qFIw0UFGOtrNOSHIqs',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsInJvbGUiOnsiYXBwMSI6eyJyb2xlIjoiYWRtaW4ifSwiYXBwMiI6eyJyb2xlIjoidXNlciJ9LCJhcHAzIjp7InJvbGUiOiJ1c2VyIn19LCJleHAiOjE3MTYxMTY0MzZ9.VCzG0ZmJt5_3FMhFs43ApdWL7x_80C17PC27SDNcEQY',
    # Add more tokens as needed
]

async def verify_token(session, url, headers, token):
    cookies = {'sso_token': token}
    async with session.get(url, headers=headers, cookies=cookies) as response:
        return await response.json(), response.status

async def run_test(num_users):
    url = 'https://sso-service-swlzbjlflq-as.a.run.app/verify'
    headers = {'appNo': 'app1'}  # Adjust the headers as needed

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_users):  # Number of requests
            token = random.choice(sso_tokens)  # Randomly select a token from the list
            tasks.append(verify_token(session, url, headers, token))
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        successful_requests = sum(1 for result in results if result[1] == 200)
        total_time = end_time - start_time
        throughput = successful_requests / total_time

        return throughput

def main():
    user_counts = [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240, 20480]  # Different numbers of users to test
    throughputs = []

    for num_users in user_counts:
        throughput = asyncio.run(run_test(num_users))
        throughputs.append(throughput)
        print(f'Users: {num_users}, Throughput: {throughput:.2f} requests/second')

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(user_counts, throughputs, marker='o')
    plt.title('SSO Token Verification Throughput')
    plt.xlabel('Number of Users')
    plt.ylabel('Throughput (requests/second)')
    plt.grid(True)
    plt.savefig('sso_throughput_graph.png')
    plt.show()

if __name__ == '__main__':
    main()
