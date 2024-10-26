import asyncio
import aiohttp
import time

# The single server URL to be used
SERVER_URL = "https://app13-276513832600.asia-southeast1.run.app/protected"

# Sample token (replace with a valid one)
VALID_SSO_TOKEN = "MwSnUBJE64Zc_np9xDIcCmfMCuWM4xwQKuiHGRMOjptRtZNBmHnOqFBIomP4ij7o2RRwmFYAUsGulz-aH3fXFsaY0IF_Jj_nKkcK8vLPjaylbHCz5SeOoo-R-wZqF79ge4va-SI-GBJ8dhOFGNqLxNxak0geOCIvfnUzwz1ozehleUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKMWMyVnlTVVFpT2lKMWMyVnlNU0lzSW5KdmJHVnpJanA3SW1Gd2NERWlPaUl6TldFek56RTJaRE0wTXpBME1HTTJOalpoTURjeE5EYzNOREkzTlRNMVlXUmhOekJtTnpSalpXVmxPR0k1WkRrd05UaGtORFF4TW1OaVpUUXdZelV5SWl3aVlYQndNaUk2SWpCaU16VmlPVEl5Wm1ReFl6VTROVE5qWmpZMVlqY3pOMlkwT1dNME9XUTRaV1kzTlRBNU5EWmlOVGt6T1RRME16QTFObVE1TkdJellUTTFNVEJrWXpZaUxDSmhjSEF6SWpvaU1HSXpOV0k1TWpKbVpERmpOVGcxTTJObU5qVmlOek0zWmpRNVl6UTVaRGhsWmpjMU1EazBObUkxT1RNNU5EUXpNRFUyWkRrMFlqTmhNelV4TUdSak5pSjlMQ0p3WlhKdGFYTnphVzl1Y3lJNmV5SmhjSEF4SWpvaU1UTTRZelJpTUdJNU5tTXdNV0l3TnpFMVpEZzNNR014TVdNd09EVXpOVGt5WVdFek1qRXpOMk0wTWpGbE56TTRNamM0TWpGbVpURTBZemxoWVdJMlpTSXNJbUZ3Y0RJaU9pSXdaREV5Tnpsak1tVXpOekpqWmpGak9HUmpZelJpWldZd1kyWXlORE14WldGaVkySTJNV1JrWkRVeVkyUTJNVE0yTnpOak1UVmxZakpqWWpoaE9UVTRJaXdpWVhCd015STZJamRsTmpSaE56VTJZVEF4T0RnNE4ySTJNemMzTm1RNE5Ua3lPRFZqWkdNNU1UQXhNbVUwT0RNMFpEYzBaREV4TXpObE1qWTFNR1ptTmpjeU56Y3daRFlpZlN3aVpYaHdJam94TnpJMU56TXlORGd3ZlEuZGJFTGJQWWtfRzJzU040VFVIN0FQU1J3Uk5ZTkdVVGRtQkphTXE5VzBVWS43Zjg4YWVhNjUyN2MyNDlkM2Y2NTdjOTVmZDIxNTQ0Nzg5MjdmOTQ5OTkzZDE0N2JhOTU1NGQ1NTI2YWNiNzQzMTA5NGNjZWU2MWZlMGQyZjU1YzgzMTIxYWNkODViM2JjZTgyZWFmMzExMjA5NzQ3ODRlYjNhNGUwYTVkZTAyZjE0NjFiM2Q2MzIwZmQ0MGY2NmU5MzdhYzkwNGYyNThmMmIwN2MzMTZmMGNmZTY3MzhhMmI0ZjZiNzQ0NTVmMjFjMTUyYjNmMDgyYmU0NTc2NmZmYjg5OTQ2NjhjNjdiY2RlYWQyZDQ4MTgxOTVmYTI5ZmIxZjM5OTQ0YmYwNGMwZTQxYzliMDNlODc3NDgzOTk1ZjMzMDU3NjkwYmE1OTY1MDI3Yzc2YTBkNTBkN2ZhYzExOTE1MDFjZTY5NzI4ZjAxNmE2MDg0ODBkNjY3YzQ1MTM2ODI3NWIyMGE2NzI4ODY1M2IzMjlmYmYyMGU2NGZlMzk1ZWFlYTQ1NmQ3MzkzNjdiYzFlNDNhNGJlYjExNDA3OTVhMTc5MGU0OTEwYWYwODIwZjE3NzMyYWEwNTk5ZWJiMzJlOTVlOTQxMGIzMTYxZTEwNjhlZmQzNTQyYjUwMTg3Nzg4ZDZlZTMyNGFiZmM3NjBlYWRhYjQ4ODNiYjQ1Y2MzMDcwMzAzNzRjMj8LUTWsSZLVFK-GVLwEkNfsGiuMcYBoV7Z0L66P5Rnc5_V3B4mHGVI4fLRtwoiSALVxAr9WB0Jcu_VQ-izYP47XxgTEnw5N3qTt6kq6RTOZztIgJkwA7gKzi1cBeK9wk9a-4yqkRK3BO35OLBUOH-Knou-egWoezLmSMxdfbqNW"

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
    print(f"Total Time Taken: {(total_time):.2f} seconds")
    print(f"Requests Per Second: {num_requests / total_time:.2f}")

def throughput_test(token, num_requests):
    print("Running async throughput test...")
    asyncio.run(concurrent_throughput_test(token, num_requests))

# Example test
if __name__ == "__main__":
    num_requests = 40960  # Adjust this value based on the load you want to test
    throughput_test(VALID_SSO_TOKEN, num_requests)