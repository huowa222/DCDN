import numpy as np
import matplotlib.pyplot as plt

# Simulate getting rtt data from WebRTC NetEQ
def get_rtt_values():
    # This is just simulated data. In reality, it needs to be obtained from WebRTC.
    num_samples = 1000
    # Simulate rtt data, assuming it follows a normal distribution
    rtt_values = np.random.normal(loc=10, scale=5, size=num_samples)
    return rtt_values

# Plot the probability distribution histogram of rtt data and calculate statistical values
def plot_rtt_histogram(rtt_values):
    # Calculate the mean, median, and 95th percentile values
    mean_rtt = np.mean(rtt_values)
    median_rtt = np.median(rtt_values)
    percentile_95_rtt = np.percentile(rtt_values, 95)

    print(f"Mean rtt: {mean_rtt:.2f} ms")
    print(f"Median rtt: {median_rtt:.2f} ms")
    print(f"95% Percentile rtt: {percentile_95_rtt:.2f} ms")

    # Set the parameters of the histogram
    num_bins = 20  # Number of bars in the histogram
    plt.figure(figsize=(10, 6))

    # Plot the histogram
    n, bins, patches = plt.hist(rtt_values, bins=num_bins, density=True, alpha=0.7, color='blue')

    # Plot vertical lines for the mean, median, and 95th percentile values
    plt.axvline(mean_rtt, color='red', linestyle='dashed', linewidth=2, label='Mean')
    plt.axvline(median_rtt, color='green', linestyle='dashed', linewidth=2, label='Median')
    plt.axvline(percentile_95_rtt, color='orange', linestyle='dashed', linewidth=2, label='95th Percentile')

    # Add titles and labels
    plt.title('Probability Distribution Histogram of NetEQ rtt')
    plt.xlabel('rtt (ms)')
    plt.ylabel('Probability Density')

    # Display the legend
    plt.legend()

    # Display the grid lines
    plt.grid(True)

    # Display the graph
    plt.show()

# Get rtt data
rtt_values = get_rtt_values()

# Plot the histogram and calculate statistical values
plot_rtt_histogram(rtt_values)
