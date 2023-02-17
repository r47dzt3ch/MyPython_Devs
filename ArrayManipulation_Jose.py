import array as myArr
class myArrayManipulation:
    def sumOfIntegers(arr):
            # comment: 
            integerSum=0
            for i in arr:
                integerSum+=i
            return integerSum
    def highElement(arr):
        highValue=None
        for i in arr:
            if highValue is None or i > highValue:
                highValue = i
        return highValue
    def lowestElement(arr):
        lowValue=None
        for i in arr:
            if lowValue is None or i < lowValue:
                lowValue = i
        return lowValue
    
    
    def allOddAndEvenElements(arr):
        # comment: 
        even=""
        odd=""
        sumOfEven=0
        sumOfOdd=0
        for i in arr:
            if i%2==0:
                sumOfEven+=i
                even+=str(i)+" "
            else:
                sumOfOdd+=i
                odd+=str(i)+" "
        print("The even elements is: ",even)
        print("The odd elements is: ",odd)
        print("The Sum of even number is: ",sumOfEven)
        print("The Sum of odd number is: ",sumOfOdd)
    def AllPositiveAndNegativeElements(arr):
        positiveValue=""
        negativeValue=""
        for i in arr:
            if i >=0:
                positiveValue+=str(i)+" "
            else:
                negativeValue+=str(i)+" "
        print("all positive value is: ",positiveValue)
        print("all negative value is: ",negativeValue)
    def reverseArr(arr):
        arr.reverse()
        return arr
        # comment: 
    # end def
        # comment: 
    # end def
        # end def
    if __name__ == "__main__":
        arr=myArr.array('i',[34,100,-89,76,55,100,10,20,45,-15,50,78,-69,13,5,150])
        print("The Array element is: ",arr)
        print("The sum of all integers is: ",sumOfIntegers(arr))
        print("The highest element is: ",highElement(arr))
        print("The lowest element is: ",lowestElement(arr))
        allOddAndEvenElements(arr)
        AllPositiveAndNegativeElements(arr)
        print("The reverse array is: ",reverseArr(arr))
        
    # end main


