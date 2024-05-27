#!/usr/bin/python3
"""
Name: Jerald Jose
Instructions: 
1. Create class Count[Surname] 
2. Problem Scenario 
Create a program that accepts string value in sentence with mix of numbers and special characters. 
 Afterwards, the program will then count how many special characters, total alphabets,  consonants and vowels, 
 total number of digits, odd and even digits.  
3. Input 
Input consist of a string input, a statement or sentence with mix of alphanumeric, special  characters. 
4. Constraints 
Input must NOT be null or empty. Whitespaces such as space and tabs are included as special  characters. 
5. Output 
Your program should count/output the following: 
special characters 
total alphabets 
consonants 
vowels 
total number of digits 
odd 
even 
6. Source Codes
7. Sample Input/Output 
NOTE: Provide a screenshot and describe your observation for each action you performed based on  the item below: 
✓ Input valid value for string 
✓ Empty value for string 
✓ Try to implement split() in your program using any character. 
8. Submit your file with filename convention: Count[Surname] 
"""
import os
from colorama import init,Fore
init(autoreset=True)
import re
class MyClass:
    def Count():
        try:
            # comment: 
            while True:
                strI="Please Input your sentence: "
                message= input(strI).lower()
                if (not message):
                    print("\n\t\t\t\t{}Please dont leave empty the input\n".format(Fore.RED))
                else:
                    break
                    # comment: 
                # END IF
            print("\n\nThe Message you input is: {}{}".format(Fore.YELLOW,message))
            vowels= ['a','e','i','o','u']
            consonants= ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
            d= re.compile("[\d]")
            sc=re.compile('[^0-9a-zA-Z]')
            alp= re.compile('[a-z]')
            alpC=alp.findall(message)
            digits= d.findall(message)
            specialC= sc.findall(message)
            vC=0
            cC=0
            for char in message:
                if(char in vowels):
                    vC+=len(char)
                if(char in consonants):
                    cC+=len(char)
            countEven=0
            countOdd=0
            for value in digits:
                dV=int(value)
                if (dV%2==0):
                    countEven+=1
                else:
                    countOdd+=1
            print("\nThe count of special characters in the message is: {}{}".format(Fore.YELLOW,len(specialC)))
            print("The count of alphabests in the message is: {}{}".format(Fore.YELLOW,len(alpC)))
            print("The count of vowels in the message is: {}{}".format(Fore.YELLOW,vC))
            print("The count of consonants in the message is: {}{}".format(Fore.YELLOW,cC))
            print("The count of number of digits in the message is: {}{}".format(Fore.YELLOW,len(digits)))
            print("The Count of even digits in the message is: {}{} ".format(Fore.YELLOW,countEven))
            print("The Count of odd digits in the message is: {}{} ".format(Fore.YELLOW,countOdd))          
        except Exception as e:
            raise e
        # END TRY
    # END DEF
    cond = True
    while cond:
        Count()
        print("\n{}Are you want to continue?\n{}(enter)-Yes\t\t{}(1)-No".format(Fore.YELLOW,Fore.GREEN,Fore.RED))
        key = input("enter: ")
        os.system('cls')
        if str(key) =='1' or str(key)=='no':
            cond=False
    pass