import numpy as np
import matplotlib.pyplot as plt

# Define the Kalman filter class for handling packet loss
class KalmanFilterForPacketLoss:
    def __init__(self, initial_estimate, initial_covariance, process_noise, measurement_noise):
        # Initialize the state estimate
        self.x_hat = initial_estimate
        # Initialize the covariance matrix
        self.P = initial_covariance
        # Set the process noise covariance
        self.Q = process_noise
        # Set the measurement noise covariance
        self.R = measurement_noise

    def predict(self):
        # Prediction step of the Kalman filter
        self.x_hat = self.x_hat
        # Update the covariance matrix in the prediction step
        self.P = self.P + self.Q

    def update(self, measurement):
        # Calculate the Kalman gain
        K = self.P / (self.P + self.R)
        # Update the state estimate using the measured value
        self.x_hat = self.x_hat + K * (measurement - self.x_hat)
        # Update the covariance matrix after the update step
        self.P = (1 - K) * self.P

    def get_estimate(self):
        # Return the current state estimate
        return self.x_hat

# Simulate the measurements of packet loss rate
np.random.seed(0)
# Generate the true packet loss rate over time
true_packet_loss = np.linspace(0.05, 0.15, 100)
# Generate the noisy measurements of the packet loss rate
measurements = true_packet_loss + np.random.normal(0, 0.02, 100)

# Initialize the Kalman filter
initial_estimate = measurements[0]
initial_covariance = 0.1
process_noise = 0.001
measurement_noise = 0.02**2
kf = KalmanFilterForPacketLoss(initial_estimate, initial_covariance, process_noise, measurement_noise)

# Apply the Kalman filter to the measurements
estimates = []
for measurement in measurements:
    # Perform the prediction step
    kf.predict()
    # Perform the update step
    kf.update(measurement)
    # Store the current estimate
    estimates.append(kf.get_estimate())

# Plot the results
plt.figure(figsize=(10, 6))
# Plot the true packet loss rate
plt.plot(true_packet_loss, label='True Packet Loss Rate')
# Plot the measured packet loss rate with a dashed line
plt.plot(measurements, label='Measured Packet Loss Rate', linestyle='--')
# Plot the smoothed packet loss rate in red
plt.plot(estimates, label='Smoothed Packet Loss Rate', color='red')
# Set the label for the x - axis
plt.xlabel('Time Step')
# Set the label for the y - axis
plt.ylabel('Packet Loss Rate')
# Set the title of the plot
plt.title('Kalman Filter for Smoothing Packet Loss Rate')
# Display the legend
plt.legend()
# Show the grid on the plot
plt.grid(True)
# Display the plot
plt.show()
