#!/usr/bin/python
"""
This my lab activity coding for data science
Name: Jerald Jose
Instructions:
1. Create class WaterSupplyManagement[Surname]
2. Problem Scenario
A tank can contain 50 gallons of water and each gallon requires 5 liters. While each liter container 
contains 12 glasses to full. How much tanks, gallons, liters, and glasses is/are needed for an N 
water where N is an input supply of water.
3. Input
Input consist of integer N, the water supply in glasses.
4. Constraints
N ≥ 1 
5. Output
Output the Tanks, Gallons, Liters, and glasses required
"""
import os
from colorama import init
init(autoreset=True)
from colorama import Fore, Back, Style
class WaterSupplyManagement_Jose(object):
    def __init__(self, arg):
        super(WaterSupplyManagement_Jose, self).__init__()
        try:
            N = input("%sEnter The Amount of water to supply: "%(Fore.YELLOW))
            gla=int(N)
            if gla  >=  1:
                    print("\n{}The number of glasses supplied is: {}{} glasses\n".format(Fore.GREEN,Fore.MAGENTA,gla))
                    lit=gla//12   
                    print("{}The number of liters supplied is: {}{} liter\n".format(Fore.GREEN,Fore.MAGENTA,lit))
                    gal=lit//5
                    print("{}The number of galoons supplied is:{}{} galoon\n".format(Fore.GREEN,Fore.MAGENTA,gal))
                    tank= gal//50
                    print("{}The number of tank supplied is: {}{} tank\n".format(Fore.GREEN,Fore.MAGENTA,gal))
            else:
                print("\nError: Please input positive Integer only\n")
        except Exception as e:
          print('\nError: ',e)  
              
cond = True
while cond:
    WaterSupplyManagement_Jose(super)
    print("\n{}Are you want to continue?\n{}(enter)-Yes\t\t{}(1)-No".format(Fore.YELLOW,Fore.GREEN,Fore.RED))
    key = input("enter: ")
    os.system('cls')
    if str(key) =='1' or str(key)=='no':
        cond=False
       


    


    




