import random
from datetime import datetime
import time

# Initialize the initial stock price, max price increase, and cash available
stock_price = 33.22
max_price_increase = 0
cash_available = 10000  # Replace with your actual cash value

# Open a text file for logging buy and sell signals
log_file = open("log-file-of-buy-and-sell-signals.txt", "a")

# Define a function to log buy and sell signals
def log_signal(signal, price):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file.write(f"{timestamp}: {signal} VST at {price:.2f}\n")

# Define a function to simulate a change in stock price
def simulate_price_change(current_price):
    # Generate a random percentage change between -1% and 1%
    percent_change = random.uniform(-1, 1) / 100
    # Update the current price based on the percentage change
    new_price = current_price * (1 + percent_change)
    return new_price

# Define a function to simulate the opening price (fixed)
def simulate_opening_price():
    return 33.22  # Fixed opening price for "VST"

# Define a function to simulate the closing price (fixed)
def simulate_closing_price():
    return 33.21  # Fixed closing price for "VST"

# Define a function to buy stocks
def buy_stock(opening_price, current_price, cash_available):
    qty_of_one_stock = 1

    # Calculate the total cost if we buy 'qty_of_one_stock' shares
    total_cost_for_qty = current_price * qty_of_one_stock

    # Define the factor to subtract as a decimal (0.5% decrease)
    factor_to_subtract = 0.995

    # Buy condition: Buy when the current price is 0.5% below the opening price
    if (cash_available >= total_cost_for_qty) and (current_price <= opening_price * factor_to_subtract):
        return qty_of_one_stock  # Return the quantity of stocks bought
    else:
        return 0  # Return 0 if no stocks were bought

# Define a function to sell stocks
def sell_stock(opening_price, current_price, bought_price):
    global max_price_increase  # Use the global max_price_increase variable

    # Calculate the maximum price increase since purchase
    max_price_increase = max(max_price_increase, current_price - bought_price)

    # Implement your stop-loss strategy (e.g., sell if the price drops below max increase - 0.02)
    if current_price <= (bought_price + max_price_increase - 0.02):
        return True  # Return True if the stock was sold
    else:
        return False  # Return False if the stock was not sold

# Main program loop
for _ in range(10):
    stock_price = simulate_price_change(stock_price)
    opening_price = simulate_opening_price()
    closing_price = simulate_closing_price()

    # Print current price
    print(f"Current Price of VST: {stock_price:.2f}")

    # Buy stocks if conditions are met
    stocks_bought = buy_stock(opening_price, stock_price, cash_available)

    if stocks_bought > 0:
        bought_price = stock_price
        log_signal("Bought", bought_price)
        print(f"Bought VST at {bought_price:.2f} on {datetime.now()}")

    # Check if stocks were sold and log the signal
    stock_sold = sell_stock(opening_price, stock_price, bought_price)
    if stock_sold:
        log_signal("Sold", stock_price)
        print(f"Sold VST at {stock_price:.2f} on {datetime.now()}")

    time.sleep(1)  # Wait for 1 second before the next iteration

# Close the log file
log_file.close()
