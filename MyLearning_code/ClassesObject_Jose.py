


def divide( num1, num2):
    #Your codes right here
    divide=num1 // num2
    return divide

def remainder( num1, num2):
# Your codes right here
    return num1%num2
def power( base, exponent):
# Your codes right here.
# Do not use base**exponent
    base**exponent
def decimalToBinary( value):
# Your codes right here.
   return bin(value)

num1 = int(input("Please Input number: "))
print('num1 is: ',num1)
num2 = int(input("Please Input number: "))
print('num2 is: ',num2)
base = int(input("Please Input base number: "))
print('base is: ',base)
exponent = int(input("Please Input exponent number: "))
print('exponent is: ',exponent)
decimal = int(input("Please Input decimal number: "))
print('decimal is: ',decimal)

print('#'*100)
print('The Quotient is ',divide( num1, num2))
print('The Ramainder is ',remainder( num1, num2))


print('The exponent of ',base, ' in ',exponent,' is ',power( base, exponent))
print('The binary of decimal ',decimal, ' is ',decimalToBinary( decimal))



