class Bird:
    
    def __init__(self):
        print('Bird is ready')

    def whoisThis(self):
        print('Bird')

    def swim(self):
        print('Swim faster')

# child class
class Penguin(Bird):

    def __init__(self):
        # call super() function
        super().__init__()
        print('Penguin is ready')

    def whoisThis(self):
        print('Penguin')

    def run(self):
        print('Run faster')

peggy = Penguin()
peggy.whoisThis()
peggy.swim()
peggy.run()

class Parrot:
    
    def fly(self):
        print('Parrot can fly')

    def swim(self):
        print('Parrot can not swim')

class Penguin:

    def fly(self):
        print('Penguin can not fly')

    def swim(self):
        print('Penguin can swim')

# common interface
def flying_test(bird):
    bird.fly()

#instantiate objects
blu = Parrot()
peggy = Penguin()

# passing the object
flying_test(blu)
flying_test(peggy)