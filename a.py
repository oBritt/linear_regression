
import matplotlib.pyplot as plt
import numpy as np

# Generate synthetic data

def normalisation(s):
    return [(_ / max(s)) for _ in s]

def denormalize_1(theta1, x_values):
    return theta1 * (max(x_values) - min(x_values))

def denormalize_0(theta0, theta1, x_values, y_values):
    min_x = min(x_values)
    max_x = max(x_values)
    min_y = min(y_values)
    theta0_original = (theta0 * (max_x - min_x)) + min_y - (denormalize_1(theta1, x_values) * min_x)
    
    return theta0_original

def a():
    km_s = [240000.0, 139800.0, 150500.0, 185530.0, 176000.0, 114800.0, 166800.0, 89000.0, 144500.0, 84000.0, 82029.0, 63060.0, 74000.0, 97500.0, 67000.0, 76025.0, 48235.0, 93000.0, 60949.0, 65674.0, 54000.0, 68500.0, 22899.0, 61789.0]
    prices_s = [3650.0, 3800.0, 4400.0, 4450.0, 5250.0, 5350.0, 5800.0, 5990.0, 5999.0, 6200.0, 6390.0, 6390.0, 6600.0, 6800.0, 6800.0, 6900.0, 6900.0, 6990.0, 7490.0, 7555.0, 7990.0, 7990.0, 7990.0, 8290.0]
    # km_s = [10, 12, 23]
    # prices_s = [12, 15, 26]
    # Initialize parameters
    
    # max_km = max(km)
    # max_prices = max(prices)
    # scale_factor = 10 ** (len(str(int(max(max_km, max_prices)))))

    # Normalize data
    # km_normalized = [x / scale_factor for x in km]
    # prices_normalized = [x / scale_factor for x in prices]

    # Initialize parameters
    t0 = 0.0
    t1 = 0.0
    km = normalisation(km_s)
    prices = normalisation(prices_s)
    print(km)
    print(prices)

    # Gradient descent parameters
    learning_rate = 0.1
    acceptable_error = 0.001
    max_iterations = 50000
    M = len(km)

# Gradient Descent
    for iteration in range(max_iterations):
        sum1 = 0.0
        sum2 = 0.0
        for i in range(M):
            error = t0 + t1 * km[i] - prices[i]
            sum1 += error
            sum2 += error * km[i]
    
        # Update parameters
        t0 -= (learning_rate * sum1) / M
        t1 -= (learning_rate * sum2) / M
        
        # Print progress
        if iteration % 500 == 0:
            print(f"Iteration {iteration}: t0 = {t0}, t1 = {t1}, sum1 = {sum1}, sum2 = {sum2}")
        
        # Check for convergence
        if abs(sum1) < acceptable_error and abs(sum2) < acceptable_error:
            print(f"Converged after {iteration} iterations.")
            break

# Scale back the parameters
    # th0 = denormalize_0(t0, t1, km_s, prices_s)
    # th1 = denormalize_1(t1, km_s)

    t0 *= max(prices_s)
    t1 = t1 / max(km_s) * max(prices_s) 
    print(f"Final parameters (scaled back): t0 = {t0}, t1 = {t1}")
    # Optionally, sca   le back the data for verification or plotting

    np.random.seed(0)


    # Linear regression parameters (for demonstration purposes, you can replace these with your own)
    # Define the linear function based on the regression parameters
    def linear_function(x):
        return t0 + t1 * x

    # print(max(km), linear_function(max(km)))
    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot the data points
    plt.scatter(km_s, prices_s, color='blue', label='Data Points')

    # Plot the linear function
    x_values = np.linspace(min(km_s), max(km_s), 100)  # Generate x values for the line
    y_values = linear_function(x_values)  # Calculate y values using the linear function
    plt.plot(x_values, y_values, color='red', linewidth=2, label='Fitted Line')

    # Add labels and title
    plt.xlabel('Mileage')
    plt.ylabel('Price')
    plt.title('Linear Regression')
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.show()
a()