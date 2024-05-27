#!/usr/bin/python
"""
Name: Jerald Jose
Instructions:
1. Create class Piglatin[Surname] 
2. Problem Scenario 
“Pig Latin” is used to obscure regular English words. To translate from English to Pig Latin, 
use the  following rules: 
✓ Words that begin with a vowel (a,e,i,o,u) should have string “ay” (not including the  quotes) 
added after it. 
For example, “apple” becomes “appleay”. 
✓ Words that begin with a consonant should have the first consonant moved to 
the end of  the word, and then “ay” should be added after the word. 
For example, “hello becomes “ellohay” 
Write a program to translate English words to Pig Latin. 
3. Input 
The input consists of a single word, consisting only of lowercase English letters. 
The word will be  at least 3 and at most 10 characters long. 
4. Constraints 
Words should NOT contain digits, special characters, null or empty values. 
5. Output 
Output a single line containing the Pig Latin Translation of that word. 
Sample input #1 Sample output #1 
tomato omatotay 
Sample input #1 Sample output #1 
umbrella umbrellaay 
Sample input #1 Sample output #1 
oregano oreganoay 
Sample input #1 Sample output #1 
tomato omatotay 
Sample input #1 Sample output #1 
yellow ellowyay 
6. Source Codes
7. Sample Input/Output 
NOTE: Provide a screenshot and describe your observation for each action you performed based on  the item below: 
✓ Input “University” as value 
✓ Input “University of Mindanao” 
✓ Input “GLORY” 
✓ Input “GOT” 
✓ Input empty string 
✓ Input any numerical value 
8. Submit your file with filename convention:Piglatin[Surname]
"""
import re
import os
from colorama import init,Fore
init(autoreset=True)
class Piglatin_Jose:
    def Piglatin():
        # comment: 
        line='='*100
        print("\n")
        print("{}Welcome to Piglatin conversion\n".center(100).upper().format(Fore.BLUE))
        print(line)
        print("""
        {}Instructions:{}Input consists of a single word, consisting only of lowercase English letters.
                        The word will be  at least 3 and at most 10 characters long.""".format(Fore.GREEN,Fore.YELLOW))
        print(line)
        while (True):
            p = re.compile('[a-z]')
            word = input("Please input a word: ")
            if(p.match(word.lower())==None):
                print(f"\t\t{Fore.RED}please input letter only")
            # comment: 
            else:
                break
        patt_vowels='aeiou'
        patt_consonant='bcdfghjklmnpqrstvwxyz' 
        wordSplit =word.split(' ')
        try:
            oWords1=""
            oWords2=""
            for words in wordSplit:
                cLength=0
                if words[0] in patt_vowels:
                    oWords1 += (words+"ay"+" ")
                else:
                    for char in words:
                        First_consec_Consonants =""
                        if char in patt_consonant:
                            # print(char,end="")
                            First_consec_Consonants += char
                            cLength=len(First_consec_Consonants)
                            oWords2 += words[cLength:]+First_consec_Consonants+"ay"+" "
                        else:
                            break
            print("\nThe Piglatin of the {2}{0}{3} is: {2}{1}".format(word,oWords1+oWords2,Fore.YELLOW,Fore.RESET))
            # print("\nThe Piglatin of the {4}{0}{5} is: {4}{1}{2}{3}".format(word,words[cLength:],ConsWStart,"ay",Fore.YELLOW,Fore.RESET))
        except Exception as e:
            raise e
        print("\n\n")
    # END DEF
    while True:
        Piglatin()
        print("\n{}Are you want to continue?\n{}(enter)-Yes\t\t{}(1)-No".format(Fore.YELLOW,Fore.GREEN,Fore.RED))
        key = input("enter: ")
        os.system('cls')
        if str(key) =='1' or str(key)=='no':
            break
    pass
# END TRY

    

