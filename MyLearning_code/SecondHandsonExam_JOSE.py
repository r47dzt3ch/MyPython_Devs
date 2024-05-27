# Jerald Jose Hands On Exam
score = 0
acount=0
bcount=0
ccount=0
dcount=0
ecount=0
fcount=0
gcount =0
while score >= 0 and score <= 100:
    try:

        score = int(input("Enter a score: "))
        if score >= 96 and score <= 100:
            acount+=1
            print("A's :" , acount)
            print("B's :" , bcount)
            print("C's :" , ccount)
            print("D's :" , dcount)
            print("E's :" , ecount)
            print("F's :" , fcount)
            print("G's :" , gcount)
        elif score >= 91:
            bcount+=1
            print("A's :" , acount)
            print("B's :" , bcount)
            print("C's :" , ccount)
            print("D's :" , dcount)
            print("E's :" , ecount)
            print("F's :" , fcount)
            print("G's :" , gcount)
        elif score >= 86:
            ccount+=1
            print("A's :" , acount)
            print("B's :" , bcount)
            print("C's :" , ccount)
            print("D's :" , dcount)
            print("E's :" , ecount)
            print("F's :" , fcount)
            print("G's :" , gcount)
        elif score >= 80:
            dcount+=1
            print("A's :" , acount)
            print("B's :" , bcount)
            print("C's :" , ccount)
            print("D's :" , dcount)
            print("E's :" , ecount)
            print("F's :" , fcount)
            print("G's :" , gcount)
        elif score >= 75:
            ecount+=1
            print("A's :" , acount)
            print("B's :" , bcount)
            print("C's :" , ccount)
            print("D's :" , dcount)
            print("E's :" , ecount)
            print("F's :" , fcount)
            print("G's :" , gcount)
        elif score >= 21:
            fcount+=1
            print("A's :" , acount)
            print("B's :" , bcount)
            print("C's :" , ccount)
            print("D's :" , dcount)
            print("E's :" , ecount)
            print("F's :" , fcount)
            print("G's :" , gcount)
        elif score >= 0:
            gcount+=1
            print("A's :" , acount)
            print("B's :" , bcount)
            print("C's :" , ccount)
            print("D's :" , dcount)
            print("E's :" , ecount)
            print("F's :" , fcount)
            print("G's :" , gcount)
        else:
            exit
    except ValueError:
        print('Invalid Entry')
 
 


