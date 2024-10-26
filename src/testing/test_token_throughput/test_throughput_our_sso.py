import asyncio
import aiohttp
import time

# The single server URL to be used
SERVER_URL = "https://app1-276513832600.asia-southeast1.run.app/protected"

# Sample token (replace with a valid one)
VALID_SSO_TOKEN = "IZou9Jsmaw4cwyZVphk6qPaUdogTop4eId7AGalO672xvUC2yu7uQBZn52wcAzjDjLY0SCLK6R_djP8r0LOTlRE-F4emZsnpj_90OPxdyEftwEKspWlnw1o16FrcZj1qIhQFEVu7VLKr7TjuFUMWNcbHVhwuBo7JWniHJRKFHlZleUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKMWMyVnlTVVFpT2lKMWMyVnlNU0lzSW5KdmJHVnpJanA3SW1Gd2NERWlPaUl6TldFek56RTJaRE0wTXpBME1HTTJOalpoTURjeE5EYzNOREkzTlRNMVlXUmhOekJtTnpSalpXVmxPR0k1WkRrd05UaGtORFF4TW1OaVpUUXdZelV5SWl3aVlYQndNaUk2SWpCaU16VmlPVEl5Wm1ReFl6VTROVE5qWmpZMVlqY3pOMlkwT1dNME9XUTRaV1kzTlRBNU5EWmlOVGt6T1RRME16QTFObVE1TkdJellUTTFNVEJrWXpZaUxDSmhjSEF6SWpvaU1HSXpOV0k1TWpKbVpERmpOVGcxTTJObU5qVmlOek0zWmpRNVl6UTVaRGhsWmpjMU1EazBObUkxT1RNNU5EUXpNRFUyWkRrMFlqTmhNelV4TUdSak5pSjlMQ0p3WlhKdGFYTnphVzl1Y3lJNmV5SmhjSEF4SWpvaU1UTTRZelJpTUdJNU5tTXdNV0l3TnpFMVpEZzNNR014TVdNd09EVXpOVGt5WVdFek1qRXpOMk0wTWpGbE56TTRNamM0TWpGbVpURTBZemxoWVdJMlpTSXNJbUZ3Y0RJaU9pSXdaREV5Tnpsak1tVXpOekpqWmpGak9HUmpZelJpWldZd1kyWXlORE14WldGaVkySTJNV1JrWkRVeVkyUTJNVE0yTnpOak1UVmxZakpqWWpoaE9UVTRJaXdpWVhCd015STZJamRsTmpSaE56VTJZVEF4T0RnNE4ySTJNemMzTm1RNE5Ua3lPRFZqWkdNNU1UQXhNbVUwT0RNMFpEYzBaREV4TXpObE1qWTFNR1ptTmpjeU56Y3daRFlpZlN3aVpYaHdJam94TnpJMU56TXpPRFk1ZlEuc0ZhOTdQODItUlVtQjhVTmk1UkxZdFhSeDlIa1NNeGY2TWxTS3ZqLURhcy4zYTdhMmIwODFiMzVmZjZjMGM0YzJmZWYyYTFkZTVhYjZjZDNiNWU3NzFkNGZhNjA5M2MxNGQxNGIxOGRhOTI0OTk5NzNjODBlN2IxNjEyZGFjMDY4OWY3MTQ4ZWIxODg5OTdmMmY4MDVmMGJkNTNhMDFiZDY0OGFkOTNlNzRjZGEzY2QzNzMxZjhhZWEwNThiMWZhZGI5ZGNmZjliYjU4MTE4NWEwZTM1MTY1NDdjZGYzZTQ0NmNjOGQ3YmU3YTg0Mzg4YTBkZjA4NzIwZGQ2NDM2ZGE1MDEyMmQwNDlkNTU3YmNmMDE5ODYxNzY2MGViNDZkMzU0OGE1MGNlYWM4MjZkMTI3ZDVkOWQ1OTAyMThlZTg5Y2E1Yjg3YzU2YTA4ZDUxZTFlN2YxMDFmM2M1MDgzNzk3NmY2YmJjNjIxMmJkYjRiNzQzMWQ1NzA2NmVhM2FjOTRlNGQzNGU4ODA0ODc2OGY5ZmU4ODEzZGViMjFjZGNkMzRiMTY3MDgzODQzOGRmMGFjMjcyZGRiYjg0MDM5MmE2ZjQwZDBhODE2N2FhYTNjYWQ4N2VhYTFkYTRlYTI5YzlkMzk4YzU0OGRlM2JiZWQ0ZjQ3YWI0MDViODgwM2JjNDBmYWE4Y2RkYTk1NzNiZDUzZGNlZTkxYTA3YTRhMTFlNzMyMjcwZjkwMQLyxqglXYgQ_oI_V0AyFqMvtotKKJnrM8MDo2CMuF4yK49ddMumnOgbaNb8vpqIZD-gTh94ngc9llWvQB4hRKWK4czdpPAXdW27dk5QuDsffsDrHFGw009cKi4O4kkxKA2g3YIE5SK2Re-DVqtMP98xnAJfVnUEB-PK31MM8QSP"

async def send_request(session, token):
    try:
        async with session.get(SERVER_URL, cookies={'sso_token': token}) as response:
            return response.status, await response.text()
    except Exception as e:
        return 500, str(e)

async def concurrent_throughput_test(token, num_requests):
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, token) for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)

    # Calculating total elapsed time
    total_time = time.time() - start_time

    success_count = sum(1 for status, _ in results if status == 200)
    failure_count = len(results) - success_count
    print(f"Total Requests: {num_requests}")
    print(f"Success: {success_count}")
    print(f"Failures: {failure_count}")
    print(f"Total Time Taken: {total_time:.2f} seconds")
    print(f"Requests Per Second: {num_requests / total_time:.2f}")

def throughput_test(token, num_requests):
    print("Running async throughput test...")
    asyncio.run(concurrent_throughput_test(token, num_requests))

# Example test
if __name__ == "__main__":
    num_requests = 20480  # Adjust this value based on the load you want to test
    throughput_test(VALID_SSO_TOKEN, num_requests)
