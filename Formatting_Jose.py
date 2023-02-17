#!/usr/bin/python3
# Name: Jerald Jose
import os
from colorama import init,Fore
init(autoreset=True)
class Formatting_Jose:
    def Formatting():
        line= "="* 100 
        # comment:
        message="Welcome to personal information system".upper()
        welcome="{0}\n{1}{welcomeMessage}{2}\n{0}"
        print(welcome.format(line,Fore.CYAN,Fore.RESET,welcomeMessage=message.center(100)))

        utiCursor="\t\t\t\t\033[1A \033[9C{}".format(Fore.YELLOW)
        Name=input(f"{Fore.GREEN}Please enter your name:  ")
        Age =input("{}Please enter your age: ".format(Fore.GREEN))
        Address=input("%sPlease enter your address: "%(Fore.GREEN))
        School=input("{0}Please enter your school: ".format(Fore.GREEN))
        foregreen=Fore.GREEN
        Year=input("{Fgreen}Please enter your year level: ".format(Fgreen=foregreen))
        course=input("{0}Please enter your {1}".format(Fore.GREEN,"course: "))
        print(Fore.RESET,line)
        print("\n")

        personal_info="""Hello, I`am {}, {} years old, I live from {}, im currently schooling at {}, {} student, with the  course of {} """
        print(personal_info.format(Name,Age,Address,School,Year,course).upper())

    # END DEF
    cond = True
    while cond:
        Formatting()
        print("\n{}Are you want to continue?\n{}(enter)-Yes\t\t{}(1)-No".format(Fore.YELLOW,Fore.GREEN,Fore.RED))
        key = input("enter: ")
        os.system('cls')
        if str(key) =='1' or str(key)=='no':
            cond=False
    pass