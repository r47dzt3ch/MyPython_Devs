# Creating an empty tuple
# Jerald Jose
emptyTuple=();
emptyTuple
# Creating tuple with constructor
empty=tuple();
empty
# Creating tuple with homogeneous elements
intTuple=(1,2,3,5,6);
intTuple
# Creating tuple with heterogeneous elements
mixTuple=(1,2,3,4,"jerald","mark","arnic");
mixTuple

# Creating tuple with single element
t=(1,);
t
# Modifying elements of Tuple
primes=(3,5,7,11,13,17)
# The following line will give an error message.
#primes[0]=19
# Accessing tuple from front
primes=(3,5,7,11,13,19)
primes[1]

# Accessing tuple from end
primes[-1]

# Search within Tuple
primes=(3,5,7,11,13,17);
print (3 in primes)
print (43 in primes)

# Adding elements to tuple
# The following line will give an error message.
#primes.append(91)

# Deleting a Tuple
del primes

# Iterating over a tuple
primes=(3,5,7,11,13,17);
for prime in primes:
 print (prime);

# Concatenation
primes=(3,5,7,11,13);
names=("c","c++","java","angular");
primes+names

# Length of tuple
len(names+primes)

# Slicing operator
primes[0:3]

# Count function
primes=(3,5,7,11,13,11,7);
primes.count(3)

# Index function
primes.index(3)