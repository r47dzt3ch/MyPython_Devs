#!/usr/bin/python3
"""
[ Laboratory No. 2.1: The sum N even integers] 
Name: Jerald Jose
Instructions: 
1. Create class SumOfNEven[Surname] 
2. Problem Scenario 
3. Write a python program that will compute the sum of the first N positive even integers.  For example 
if N is 3, you should compute 2 + 4 +6 = 12 
4. Input 
Input consist of a positive integer N, a value for the limits of iterations.
5. Constraints 
1 ≤ N≤ ∞ 
6. Output 
Your program should output the sum of the first N positive integers by the format as shown  below: 
If N is 0, display “Invalid input” 
If N is 4, display “2+4+6+8=20” 
7. Source Codes 
8. Sample Input/Output 
NOTE: Provide a screenshot and describe your observation for each action you performed based on  the item below: 
✓ Input zero or negative value for N such that -6, 4 
✓ Input floating point value for N such that 3.7, 9.8 
✓ Input any valid value for N 
9. Submit your file with filename convention: SumOfNEven[Surname] 
"""
import os
import ast

from colorama import init
init(autoreset=True)
from colorama import Fore
class SumOfNEven_Jose:
    def SumOfNEven():
        # comment: 
        try:
            N =ast.literal_eval(input("Please enter a number: "))
            sumOfEven=0
            if  type(N) == int:
                if (N>0):
                    for i in range(1,N+1):
                    # comment:
                        if(i % 2==0):
                            sumOfEven = sumOfEven + i
                            print(i,end=' ')
                    print("\nThe Sum of Even Numbers from 1 to {0} = {2}{1}".format(N,sumOfEven,Fore.YELLOW))  
                elif (N <=0):
                # comment: :
                    print("\nInvalid Input: {1}{0}\n\n{2}It should be not equal to 0 or negative number".format(N,Fore.YELLOW,Fore.RESET)) 
            elif(type(N) == float ):
                print("\nInvalid Input: {1}{0} is a float type".format(N,Fore.YELLOW))
        except Exception as e:
            print('An exception occurred: ',e)
    cond = True
    while cond:
        SumOfNEven()
        print("\n{}Are you want to continue?\n{}(enter)-Yes\t\t{}(1)-No".format(Fore.YELLOW,Fore.GREEN,Fore.RED))
        key = input("enter: ")
        os.system('cls')
        if str(key) =='1' or str(key)=='no':
            cond=False
    pass
