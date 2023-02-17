def Fibonacci_Jose(value):
    try:
        fn1=0
        fn2=1
        fib = [fn2]
        fib_total=0
        for item in range(value-1):
            # comment:
                fn1=fn2-fn1
                fn2=fn1+fn2
                fib_total+=fn2
                fib.append(fn2)
        fib.reverse()
        print("""\n\t{}""".format(fib))
        if(fib_total==0):fib_total=1
        print("\tThe total sum of Fibonacci serries of {} is {}".format(value,fib_total))
    except Exception as e:
        raise e
    # end try
if __name__ == "__main__":
    while True:
        N = int(input("Please input the number of serries you want display: "))
        if(N<1):
            print("Please Enter number greater than or equal to 1")
        else:
            Fibonacci_Jose(N)
            continue
    


    
