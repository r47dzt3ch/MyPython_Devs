# Creating an empty Dictionary
Dict = {}
print("Empty Dictionary: ")
print(Dict)

# Adding elements one at a time
Dict[0] = 'jeraldjose'
Dict[2] = 'age 20'
Dict[3] = 'Phone No. 09101919317'
print("\nDictionary after adding 3 elements: ")
print(Dict)

# Adding set of values
# to a single Key
Dict['Value_set'] = "Address: Montevista Davao de oro", 'Zipcode: 8801', 'Purok 3a BanagBanag'
print("\nDictionary after adding 3 elements: ")
print(Dict)

# Updating existing Key's Value
Dict[2] = 'Welcome'
print("\nUpdated key value: ")
print(Dict)

# Adding Nested Key value to Dictionary
Dict[5] = {'Nested' :{'Hello' : 'Programmer', 'Life' : 'Now'}}
print("\nAdding a Nested Key: ")
print(Dict)
