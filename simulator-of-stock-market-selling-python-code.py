import random
from datetime import datetime, timezone, timedelta
import time

# Initialize the initial stock price, max price increase, cash available, bought price, and shares owned
stock_price = 33.22
max_price_increase = 0
cash_available = 35000  # Start with $35,000 in cash
bought_price = 32.75  # Initial bought price
shares_owned = 50  # Start with 50 shares

# Open a text file for logging buy and sell signals
log_file = open("log-file-of-buy-and-sell-signals.txt", "a")

# Define a function to log buy and sell signals
def log_signal(signal, price, shares):
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p %Z")
    log_file.write(f"{timestamp}: {signal} {shares} VST at {price:.2f}\n")

# Define a function to simulate a change in stock price
def simulate_price_change(current_price):
    # Generate a random percentage change between -1% and 1%
    percent_change = random.uniform(-1, 1) / 100
    # Update the current price based on the percentage change
    new_price = current_price * (1 + percent_change)
    return new_price

# Define a function to simulate the opening price (fixed)
def simulate_opening_price():
    return 33.22  # Fixed opening price for " VST"

# Define a function to simulate the closing price (fixed)
def simulate_closing_price():
    return 33.21  # Fixed closing price for "VST"

# Define a function to buy up to 50 shares if there's enough cash
def buy_up_to_50_shares(opening_price, current_price, cash_available):
    # Define the factor to subtract as a decimal (0.5% decrease)
    factor_to_subtract = 0.995

    # Calculate the maximum number of shares that can be bought with available cash (up to 50 shares)
    max_shares = min(50, cash_available // current_price)

    # Buy condition: Buy up to 50 shares when the current price is 0.5% below the opening price
    if (max_shares > 0) and (current_price <= opening_price * factor_to_subtract):
        cash_spent = max_shares * current_price  # Calculate the total cost
        cash_available -= cash_spent  # Deduct the purchase cost
        return max_shares, cash_available  # Return updated values
    else:
        return 0, cash_available  # Return 0 shares and unchanged cash

# Define a function to sell all shares of stock
def sell_all_shares(opening_price, current_price, shares_owned, cash_available):
    global max_price_increase  # Use the global max_price_increase variable

    # Calculate the maximum price increase since purchase
    max_price_increase = max(max_price_increase, current_price - bought_price)

    # Condition 1: Sell when the price increases by 1% or more than the bought price
    if (current_price >= bought_price * 1.01) and shares_owned > 0:
        cash_available += shares_owned * current_price  # Add the selling proceeds to cash
        log_signal("Sold", current_price, shares_owned)
        print(f"Sold {shares_owned} shares of VST at {current_price:.2f} each on {datetime.now().strftime('%Y-%m-%d %I:%M %p %Z')}")
        shares_owned = 0  # Set shares owned to 0 after selling all shares

    return shares_owned, cash_available

# Main program loop
while True:  # Infinite loop
    stock_price = simulate_price_change(stock_price)
    opening_price = simulate_opening_price()
    closing_price = simulate_closing_price()

    # Print separation line
    print("----------------------------------------------------------------------------------------------------------------------------")

    # Print local time in Eastern time zone
    eastern_time = datetime.now(timezone.utc) + timedelta(hours=-5)  # Eastern time is UTC-5
    print(f"Eastern Time: {eastern_time.strftime('%I:%M %p')}")

    # Print current price and cash available with neat separation
    print("----------------------------------------------------------------------------------------------------------------------------")
    print(f"Current Price of VST: {stock_price:.2f}     |     Cash Available: {cash_available:.2f}")
    print("----------------------------------------------------------------------------------------------------------------------------")

    # Update the display for the number of shares owned and their value
    if shares_owned > 0:
        total_value = shares_owned * stock_price
        print(f"Currently own {shares_owned} shares of VST valued at ${total_value:.2f}")
    else:
        print(f"Currently own 0 shares of VST valued at $0.00")

    # Buy up to 50 shares if conditions are met
    bought_shares, cash_available = buy_up_to_50_shares(opening_price, stock_price, cash_available)

    if bought_shares > 0:
        bought_price = stock_price
        log_signal("Bought", bought_price, bought_shares)
        print(f"Bought {bought_shares} shares of VST at {bought_price:.2f} on {datetime.now().strftime('%Y-%m-%d %I:%M %p %Z')}")

    # Sell all shares if conditions are met
    shares_owned, cash_available = sell_all_shares(opening_price, stock_price, shares_owned, cash_available)

    time.sleep(1)  # Wait for 1 second before the next iteration

# Close the log file (note: this line will never be reached in the infinite loop)
log_file.close()
