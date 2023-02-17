#!/usr/bin/python3

"""
Name: Jerald Jose
Instructions: 
1. Create class Investment[Surname] 
2. Problem Scenario 
MEtsab corporation has been known for its excellency and 
transparency towards its clients in  terms of monetarization and capitalization. 
This year they have more than 10 million investors. And it is growing dramatically. 
Due to its manual processes in calculation in  interest, they are having delay and difficulty in giving
payouts on time. Hence, they might lose  some investors if this will continue to happen. 
To help the corporation sustain its missions  and values, help them automate the calculation of 
interest as to how much monthly payout  they should give to each investor. The formula is as follows: 
Interest/Month = Capital * (700%)  
Processing Fee = 1.5% of the Monthly Payout 
3. Input 
Input consist name of investors in string and capital in float, the capital of investment in currency.

4. Constraints 
5,000.00 ≤ Capital ≥ 500,000.00 
5. Output 
Investor 
Capital 
Month Interest 
Processing Fee 
Monthly Payout (Gross) 
Net Income in a Month 
Annual Interest (Calculate with no processing fee) 
Net Income in a year 
6. Source Codes
7. Sample Input/Output (Atleast 3 attempts) 
NOTE: Provide a screenshot and describe your observation for each action you performed 
based on  the item below: 
✓ Input any capital value between the constraints 
✓ Input any capital value NOT between the constraints 
✓ When a capital C is a negative value 
✓ When a capital C is a string or contain string 
✓ When a capital C contains comma 
8. Submit your file with filename convention: Investment[Surname] 
"""
import os
from operator import truediv
from colorama import init
init(autoreset=True)
from colorama import Fore, Back, Style
class Investment_Jose:
    print("welcome To investment Firm System")
    def execute(args):
        try:
            line=Fore.GREEN+"====================================================================="
            Investor=input("\nPlease enter the name of investors: ")
            Capital=float(input("\nPlease enter the Capital: "))
            if Capital >= 5000.00 and Capital <= 500000.00:        
                print("\nName of Investor is {}{}{} and the capital invested is {}{}\n\n".format(Fore.GREEN, Investor,Fore.RESET,Fore.GREEN,Capital))
                mthInterest=Capital*7
                prcFee=(mthInterest+Capital)*0.015
                mthPayout=(mthInterest+Capital)-prcFee
                anlInterest=mthInterest*12  
                netIncome=mthPayout-Capital
                yNetincome=(mthPayout*12)-Capital
                print("{}\n{}Monthly Interest for the {} capital is: {}{}\n{}\n".format(line,Fore.YELLOW,Capital,Fore.RED,mthInterest,line))
                print("Processing fee of the monthly payout is: {}1.5%\n".format(Fore.RED))
                print("{}\n{}Monthly Payout(Gross) is: {}{}\n{}".format(line,Fore.YELLOW,Fore.RED,mthPayout,line))
                print("{}\n{}Net Income in a month is: {}{}\n{}".format(line,Fore.YELLOW,Fore.RED,netIncome,line))
                print("{}\n{}Anual Interest with no processing fee is: {}{}\n{}".format(line,Fore.YELLOW,Fore.RED,anlInterest,line))
                print("{}\n{}Net income in a year is: {}{}\n{}".format(line,Fore.YELLOW,Fore.RED,yNetincome,line))
            elif Capital < 0:
                print("Enter positive Numbers only")
            else:  
                print("Sorry {}{}{} your {}{}{} Capital is not qualicable to invest in our Investment firm company".format(Fore.GREEN,Investor,Fore.RESET,Fore.GREEN,Capital,Fore.RESET))      
        except:    
            print("Error Please input Numbers only")
    pass
    cond=True
    while cond:
        execute(execute)
        print("\n{}Are you want to continue?\n{}(enter)-Yes\t\t{}(1)-No".format(Fore.YELLOW,Fore.GREEN,Fore.RED))
        key = input("enter: ")
        os.system('cls')
        if str(key) =='1' or str(key)=='no':
            cond=False
pass
