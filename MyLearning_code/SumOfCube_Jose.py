#!/usr/bin/python3
"""
Name: Jerald Jose
Instructions: 
1. Create class SumOfCube[Surname] 
2. Problem Scenario 
Write a program that accepts two integer values: start and end and then computes the sum of  the cube a number from start to end such that  
start= 2 and end=5 
which yields  
23 + 33 + 43 + 53 = 8 + 27 + 64 + 125 = 224 
3. Input 
Input consist of a two positive integersstart and end, a values for the limits or range of iterations.
 4. Constraints 
1 ≤ start/end ≤ ∞ 
5. Output 
Your program should output the sum of the cube of two numbers: start and end 
If start is 0 or below, display “Invalid input”. Ask again. 
If end is 0 or below, display “Invalid input”. Ask again. 
If end is lower than start, ask higher value for end. And then proceed. 
If inputs are correct, proceed to calculations as sumOf(start3: end3)
6. Source Codes 
7. Sample Input/Output 
NOTE: Provide a screenshot and describe your observation for each action you performed based on  the item below: 
✓ Input valid values for start and end 
✓ Input zero or negative value for start such that 0 or -4 
✓ Input zero or negative value for end such that 0 or -4 
✓ Input lower value for end 
✓ Input decimal value for both start and end 
8. Submit your file with filename convention: SumOfCube [Surname] 
"""
import ast
import os
from colorama import init,Fore
init(autoreset=True)
class SumOfCube_Jose:
    def SumOfCube():
        line='='*50
        while True:
            try:
                # comment: 
                start3 = ast.literal_eval(input("Please enter number to start: "))
                if(type(start3) != (int)):
                    print("\n\t\t\t{1}The number: {0} you enter is a Float type\n".format(start3,Fore.RED))
                
                elif (start3<=0):
                    print("\n\t\t\t{1}Invalid Input for number: {0},please Retry.\n".format(start3,Fore.RED))
                   
                else:
                    break
            except:
                print("\n\t\t\t{}Error: Enter only a number\n".format(Fore.RED))
                
            # END TRY

        if (start3>0):
            while True:     
                try:
                    end3=ast.literal_eval(input("Please enter number to end: "))
                    # comment: 
                    if(type(end3) != (int)):
                        print("\n\t\t\t{1}The number {0} you enter is Float type\n".format(end3,Fore.RED))
                    elif (end3<=start3 and end3 >0):
                        print("\n\t\t\t{1}The Number Enter is lower than start = {0}.\n".format(start3,Fore.RED))
                    elif(end3<=0):
                        print("\n\t\t\t{1}Invalid Input: {0},please Retry. \n".format(end3,Fore.RED))
                    else:

                        break
                except:
                        print("\n\t\t\t{}Error: Enter only a number\n".format(Fore.RED)) 
                # END TRY
            if(end3>start3):
                sumOfCube=0
                print(line)
                for i in range(start3, end3+1):
                    print("#\tThe cube of {0} is: {2}{1}{3}".format(i,i**3,Fore.YELLOW,Fore.RESET))
                    sumOfCube+=(i**3)
                print(line)
                print("#\n#\tThe total sum of Cube from {0} to {1} is: {3}{2}{4}\n#".format(start3,end3,sumOfCube,Fore.YELLOW,Fore.RESET))
                print(line)
    cond = True
    while cond:
        SumOfCube()
        print("\n{}Are you want to Retry?\n{}(enter)-Yes\t\t{}(1)-No".format(Fore.YELLOW,Fore.GREEN,Fore.RED))
        key = input("enter: ")
        os.system('cls')
        if str(key) =='1' or str(key)=='no':
            cond=False 
    
    pass