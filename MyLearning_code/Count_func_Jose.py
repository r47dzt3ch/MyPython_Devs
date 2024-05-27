from colorama import init,Fore
init(autoreset=True)
class Count_jose:
    def power(base,exponent):
        return base**exponent

    def decToBinary(value): 
    #Your code goes here 
        val=bin(value)
        
        return val[2:]
    def isPalindrome(valStr): 
    #Your code goes here 
        revStr=""
        rev=reversed(valStr)
        for char in rev:
            revStr+=char
        if revStr==valStr:
            return "True"
        else:
            return "False"
    if __name__ == "__main__":
        while True:
            base=int(input("Base\t\t: ")) 
            if base < 1:
                print("Please input base number higher than 1") 
            else:
                break
        while True:
            exp=int(input("Exponent\t: ")) 
            if exp < 1:
                print("Please input exponent number higher than 1") 
            else:
                break
        p=power(base,exp)
        b=decToBinary(p) 
        pal=isPalindrome(b) 
        print("{0}{1}{4} raised to the power of {0}{2}{4} is {0}{3}{4}".format(Fore.YELLOW,base,exp,p,Fore.RESET)) 
        print("{0}{1}{3} is {0}{2}{3} in binary ".format(Fore.YELLOW,p,b,Fore.RESET)) 
        print("Palindrome: {0}{1}{2}".format(Fore.YELLOW,pal,Fore.RESET))
    # end main
    pass