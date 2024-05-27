import random
import os
import time
from colorama import init,Fore,Style
init()
class GuessingGame_Jose:
   
    """
    Instructions:
    1. Create class GuessingGame[Surname]
    2. Problem Scenario
    You’re going to make a “Guess the Number” game. The computer will think of a random number
    from 1 to N, and ask you to guess it. The computer will tell you if each guess is too high or too low.
    You win if you can guess the number.

    3. Input/Output and constraints
    Input consist of the following:
    ✓ Name. Your name or player name. Must not be empty or null.
    ✓ Bet. It is the integer value you want to place in the game which cost you 10 pesos per bet. The
    value must be divisible by 10.
    ✓ N value. It is the range of the number (integer) you will guess. The higher the N the
    higher the prize as it will be calculated as 10 times the N. The input must be greater
    than 4 to infinity.

    Sample Run of Guess the Number
    Here’s what the program looks like to the player when run. The text that the player types in is
    in bold. (Assuming the number to guess is 5 and won)
    Hi! Martzel place your bet. 30
    You have 3 bets. Now, give me the max number to generate. 10
    Well, Martzel, you have to guess from 1 to 10 to win 100.
    Take a guess. 7
    Your guess is too high.
    Take a guess. 2
    Your guess is too low.
    Take a guess.5
    Good job, Martzel! You guessed the number in 3 guesses! You won 100.

    Sample Run of Guess the Number
    Here’s what the program looks like to the player when run. The text that the player types in is
    in bold. (Assuming the number to guess is 5 and lost)
    Your name? Martzel
    Hi! Martzel place your bet. 30
    You have 3 bets. Now, give me the max number to generate. 10
    Well, Martzel, you have to guess from 1 to 10 to win 100.
    Take a guess. 7
    Your guess is too high.
    Take a guess. 2
    Your guess is too low.
    Take a guess.4
    Sorry, Martzel! You are out of turn. You lost!

    4. Source Codes

    5. Sample Input/Output
    NOTE: Provide a screenshot and describe your observation for each action you performed based on
    the item below:
    ✓Input a zero integer for bet value.
    ✓Input a negative integer such that -3,-5,-7 for bet value.
    ✓Input any integer which is divisible by 10 for bet value.
    ✓Input any negative integer which divisible by 10 for bet value.
    ✓Input any integer less than 5 for N.
    ✓Input any integer greater than 5 for N.
    ✓Run a program where player wins
    ✓Run a program where player loses

    6. Submit your file with filename convention: Count[Surname]
    """
    def Guesing():
        # comment:
        line='='*100
        while True:
            print(line)
            print("Welcome to the guessing game".upper().center(100))
            print(line)
            print("\tPlease input your name: {}".format(Style.BRIGHT),end="")
            name = input()
            if name == "":
                print("\tPlease dont forget to enter your name\n")
                time.sleep(1)  # 
                os.system("cls")
            else:
                break
        try:
            # comment: 
            print("\t{}Hi! {} place your bet: {}".format(Style.RESET_ALL,name.upper(),Fore.GREEN),end="")
            Bet=int(input())
            while(True):
                print("\t{}You have {} bets. Now, give me the max number to generate: {} ".format(Fore.RESET,Bet//10,Fore.GREEN),end="")
                N=int(input())
                if(N<=4):
                    print("\tSorry you should input max number greater than 4")
                    
                else:
                    break  
            print("\t{}Well, {}, you have to guess from 1 to {} to win {}.".format(Fore.RESET,name,N,N*10))
            print(line)  
            winning_num= random.randint(1, N)
            for item in range(1,(Bet//10)+1):
                print("Take a guess:{}".format(Fore.GREEN),end="")
                guess=int(input())
                if (guess==winning_num):
                    print("{}Good job, {}! You guessed the number in {} guesses! You won {}.".format(Fore.RESET,name,item,N*10))
                    break  
                elif(item==(Bet//10)):
                    print("{}Sorry, {}! You are out of turn. You lost!".format(Fore.RESET,name))
                elif (guess>winning_num):
                    print("{}Your guess is too high.".format(Fore.RESET))
                elif (guess<winning_num):
                    print("{}Your guess is too low.".format(Fore.RESET))
        except Exception as e:
            print(e)
        # end try
    # end def
    if __name__ == "__main__":
         Guesing()
        
    # end main
   
    pass