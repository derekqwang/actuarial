# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 15:49:42 2021

@author: derek

This program simulates the movement of a stock price using the 
Black-Scholes framework. After feeding it with the necessary option greek
parameters, and choosing a long or short call/put/stock, it will simulate
stock price movements for 1 year. It will then tell the user the payoff/profit
of the position they chose.

"""

# Importing relevant modules
import numpy as np
from numpy import log as ln
import matplotlib.pyplot as plt
import math
from scipy.stats import norm

print("Welcome to the NYSE. Please give me information " \
      "about the stock you are interested in.")

# Initializing variables

# Dividend yield rate
d = -1
# Volatility
v = -1
# Risk-free interest rate
r = -1
# Stock price at time t=0
S = -1
# Strike price of the call/put, if selected
K = -1
# Time until expiration of option, or exit time of stock position
T = -1
# User selections
userAction1 = ''
userAction2 = ''

# Prompting user for relevant information about the stock
stock_name = input("What is the name of the stock? ")

while d < 0 or d > 1:
    try:
        d = float(input("What is the dividend yield rate? "))
    except ValueError:
        print("\n\tPlease enter a number between 0 and 1")
        continue
    if d < 0 or d > 1:
        print("\n\tPlease enter a number between 0 and 1")


while v < 0 or v > 1:
    try:
        v = float(input("What is the volatility? "))
    except ValueError:
        print("\n\tPlease enter a number between 0 and 1")
        continue
    if v < 0 or v > 1:
        print("\n\tPlease enter a number between 0 and 1")

    
while r < 0 or r > 1:
    try:
        r = float(input("What is the risk-free interest rate? "))
    except ValueError:
        print("\n\tPlease enter a number between 0 and 1")
        continue
    if r < 0 or r > 1:
        print("\n\tPlease enter a number between 0 and 1")

        
while S <= 0:
    try:
        S = float(input("What is the current stock price in dollars? "))
    except ValueError:
        print("\n\tPlease enter a number larger than 0")
        continue
    if S <= 0:
        print("\n\tPlease enter a number larger than 0")


# Asking the user what position they would like to enter with the underlying
# asset being the stock, and then if they want to enter a long or short position       
while userAction1.upper() not in ['C','P','S']:
    userAction1 = input("Are you interested in a European call (C), " \
                        "European put (P) or the stock itself (S)? ")
    if userAction1.upper() not in ['C','P','S']:
        print("\n\tPlease type C, P, or S for call, put, or stock respectively")


if userAction1.upper() == 'C':
    position = 'call'
elif userAction1.upper() == 'P':
    position = 'put'
else:
    position = 'stock'
        
        
while userAction2.upper() not in ['L','S']:
    userAction2 = input("Do you wish to enter a long (L) " + position + " position " \
                        "or a short (S) " + position + " position? ")
    if userAction2.upper() not in ['L','S']:
        print("\n\tPlease type L for long, or S for short")

# If the user chose call or put, ask for the strike price and the time
# until expiration. Else for a stock, ask when they intend to sell their stock
# (for a long stock) or buy their stock back (for a short stock)
if userAction1.upper() in ['C','P']:
    while K <= 0:
        try:
            K = float(input("What is the desired strike price for your " \
                            + position + "? "))
        except ValueError:
            print("\n\tPlease enter a positive number")
            continue
        if K <= 0:
            print("\n\tPlease enter a positive number")
    
    while T <= 0 or T > 4:
        try:
            T = float(input("What is the desired time until expiration (in years) " \
                            "for your " + position + "? We will simulate up to 4 years. "))
        except ValueError:
            print("\n\tPlease enter a number larger than 0 and less than or " \
                  "equal to 4")
            continue
        if T <= 0 or T > 4:
            print("\n\tPlease enter a number larger than 0 and less than or " \
                  "equal to 4")
                
else: # If user didn't select call or put, they must have selected stock
    while T <= 0 or T > 4:
        try: T = float(input("When do you intend to exit your stock position" \
                             " (in years)? We will simulate up to 4 years. "))
        except ValueError:
            print("\n\tPlease enter a number larger than 0 and less than or " \
                  "equal to 4")
        if T <= 0 or T > 4:
            print("\n\tPlease enter a number larger than 0 and less than or " \
                  "equal to 4")
     
                        
# Creating the plot of Stock Price vs. Time Elapsed                        
x = np.linspace(0,4,1600)
y = [S]

for i in range(0,1599):
    n = np.random.normal(0,1)
    new_value = y[i] * math.exp((r-d-0.5*v**2)*0.0025+v*math.sqrt(0.0025)*n)
    y.append(new_value)

plt.figure(figsize=(10,4.8))
plt.title(stock_name + " Stock Price")
plt.xlabel("Time Elapsed in Years")    
plt.ylabel("Stock Price in $")
plt.plot(x,y)


if userAction1.upper() in ['C','P']:
     fps = S * math.exp(-d * T)
     fpk = K * math.exp(-r * T)
     d1 = (ln(fps/fpk) + 0.5*(v**2)*T)/(v*math.sqrt(T))
     d2 = d1 - v*math.sqrt(T)
     if userAction1.upper() == 'C':
         premium = fps*norm.cdf(d1) - fpk*norm.cdf(d2)
         # Payoff of a long call. For a short call I will put a negative sign
         # in front of it
         payoff = max(0, y[int(T/0.0025)-1] - K)
     else: #userAction1.upper() == 'P'
         premium = fpk*norm.cdf(-d2) - fps*norm.cdf(-d1)
         # Payoff of a long put. For a short put I will put a negative sign
         # in front of it
         payoff = max(0, K - y[int(T/0.0025)-1])
     print("\nYour " + position + " premium is " + str(round(premium,2)) + " dollars.")
     print("After " + str(T) + " years, the stock price hit " + str(round(y[int(T/0.0025)-1],2))\
           + " dollars.")
     if userAction2.upper() == 'L':
         print("The payoff of your long " + str(position) + " is " + \
               str(round(payoff,2)) + " dollars.")
         print("The profit of your long " + str(position) + " is " + \
               str(round(payoff-premium*math.exp(r*T),2)) + " dollars.")
     else:
         print("The payoff of your short " + str(position) + " is " + \
               str(round(-payoff,2)) + " dollars.")
         print("The profit of your short " + str(position) + " is " + \
               str(round(premium*math.exp(r*T)-payoff,2)) + " dollars.")
             
else: # userAction1.upper() == 'S'
    # Payoff of a long stock. For a short stock I will put a negative sign
    # in front of it
    payoff = y[int(T/0.0025)-1]
    print("After " + str(T) + " years, the stock price hit " + str(round(y[int(T/0.0025)-1],2))\
           + " dollars.")
    if userAction2.upper() == 'L':
        print("The payoff of your long " + str(position) + " is " + \
              str(round(payoff,2)) + " dollars.")
        print("The profit of your long " + str(position) + " is " + \
              str(round(payoff-S*math.exp(r*T),2)) + " dollars.")
    else: # userAction2.upper() == 'S':
        print("The payoff of your long " + str(position) + " is " + \
              str(round(-payoff,2)) + " dollars.")
        print("The profit of your long " + str(position) + " is " + \
              str(round(S*math.exp(r*T)-payoff,2)) + " dollars.")
            
print("\nPlease refer to the graph of the stock price for details.")
    

