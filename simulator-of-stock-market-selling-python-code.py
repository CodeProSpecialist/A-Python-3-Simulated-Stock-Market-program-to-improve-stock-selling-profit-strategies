import random
from datetime import datetime, timezone, timedelta
import time
import pytz

# Declare global variables
global shares_owned, shares_sold, opening_price

# Initialize the initial stock price, max price increase, cash available, bought price, and shares owned
opening_price = 33.07
stock_price = 33.08
max_price_increase = 0
cash_available = 37449.57  # Start with $37,449.57 in cash
bought_price = 33.08  # Initial bought price
shares_owned = 1132.0  # Start with 1,132 shares

# Initialize variables to keep track of shares bought and sold
shares_bought = 0
shares_sold = 0

# Open a text file for logging buy and sell signals
log_file = open("log-file-of-buy-and-sell-signals.txt", "a")

# Define a function to log buy and sell signals
def log_signal(signal, price, shares, cash):
    # Get the current time in the US/Eastern timezone
    now = datetime.now(pytz.timezone('US/Eastern'))
    current_time_str = now.strftime("Eastern Time | %I:%M:%S %p | %m-%d-%Y |")

    # Calculate the change in the number of shares owned
    shares_change = shares_owned - shares

    # Log the signal with the current time, cash balance, and ownership details
    log_message = f"{current_time_str} {signal} {shares_change} VST at {price:.2f} | Cash Available: {cash:.2f} | Owned: {shares_owned} shares valued at ${shares_owned * price:.2f}\n"
    log_file.write(log_message)

    # Reset the number of shares bought and sold to 0 after logging
    global shares_bought, shares_sold
    shares_bought = 0
    shares_sold = 0

# Define a function to update the number of shares owned and their value
def update_shares_value():
    global shares_owned
    total_value = shares_owned * stock_price
    return shares_owned, total_value

# Define a function to simulate a change in stock price
def simulate_price_change(current_price):
    # Generate a random percentage change between -1% and 1%
    percent_change = random.uniform(-1, 1) / 100
    # Update the current price based on the percentage change
    new_price = current_price * (1 + percent_change)
    return new_price

# Define a function to simulate the opening price (fixed)
def simulate_opening_price():
    return 33.08  # Fixed opening price for "VST"

# Define a function to simulate the closing price (fixed)
def simulate_closing_price():
    return 33.21  # Fixed closing price for "VST"

# Define a function to buy as many shares as possible with available cash
def buy_all_available_shares(opening_price, current_price, cash_available):
    if cash_available <= 0:
        return 0, cash_available

    # Calculate the maximum number of shares that can be bought with available cash
    max_shares = cash_available // current_price

    # Buy condition: Buy as many shares as possible when the current price is below the opening price
    if max_shares > 0 and current_price <= opening_price:
        cash_spent = max_shares * current_price  # Calculate the total cost
        cash_available -= cash_spent  # Deduct the purchase cost
        global shares_owned, shares_bought
        shares_owned += max_shares  # Update the number of shares owned
        shares_bought += max_shares  # Update the number of shares bought
        return max_shares, cash_available  # Return updated values
    else:
        return 0, cash_available  # Return 0 shares and unchanged cash

# Define a function to sell all shares of stock
def sell_all_shares(opening_price, current_price, shares_owned, cash_available):
    global max_price_increase     # Use the global max_price_increase variable

    shares_sold = 0
    # Calculate the maximum price increase since purchase
    max_price_increase = max(max_price_increase, current_price - bought_price)

    # Condition 1: Sell when the price increases by 1% or more than the bought price
    if (current_price >= bought_price * 1.01) and shares_owned > 0:
        cash_gained = shares_owned * current_price  # Calculate the selling proceeds
        cash_available += cash_gained  # Add the selling proceeds to cash

        shares_sold += shares_owned  # Update the number of shares sold
        shares_owned = 0  # Set shares owned to 0 after selling all shares
        log_signal("Sold", current_price, shares_sold, cash_available)
    return shares_owned, cash_available

# Main program loop
while True:  # Infinite loop
    stock_price = simulate_price_change(stock_price)
    opening_price = simulate_opening_price()
    closing_price = simulate_closing_price()

    # Print separation line
    print("----------------------------------------------------------------------------------------------------------------------------")

    # Get the current time in the US/Eastern timezone
    now = datetime.now(pytz.timezone('US/Eastern'))
    current_time_str = now.strftime("Eastern Time | %I:%M:%S %p | %m-%d-%Y |")

    # Print current time and date
    print(current_time_str)

    # Print current price and cash available with neat separation
    print("----------------------------------------------------------------------------------------------------------------------------")
    print(f"Current Price of VST: {stock_price:.2f}     |     Cash Available: {cash_available:.2f}")
    print("----------------------------------------------------------------------------------------------------------------------------")

    # Update the number of shares owned and their value
    shares_owned, total_value = update_shares_value()
    print(f"Currently own {shares_owned} shares of VST valued at ${total_value:.2f}")

    # Buy as many shares as possible if conditions are met
    bought_shares, cash_available = buy_all_available_shares(opening_price, stock_price, cash_available)

    if bought_shares > 0:
        bought_price = stock_price
        log_signal("Bought", bought_price, shares_bought, cash_available)

    # Sell all shares if conditions are met
    shares_owned, cash_available = sell_all_shares(opening_price, stock_price, shares_owned, cash_available)

    time.sleep(1)  # Wait for 1 second before the next iteration

# Close the log file (note: this line will never be reached in the infinite loop)
log_file.close()
