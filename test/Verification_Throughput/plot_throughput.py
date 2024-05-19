import json
import matplotlib.pyplot as plt

# Load results from JSON file
with open('throughput_results.json', 'r') as f:
    results = json.load(f)

# Check if there are results to plot
if results:
    users, throughput = zip(*results)
    plt.figure(figsize=(10, 6))
    plt.plot(users, throughput, marker='o', linestyle='-', color='b', label='Throughput')

    plt.title('System Throughput vs. Number of Users')
    plt.xlabel('Number of Users')
    plt.ylabel('Throughput (Requests per Second)')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("No results to plot.")
