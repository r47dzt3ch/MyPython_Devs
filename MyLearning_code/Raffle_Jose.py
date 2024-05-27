#!/usr/bin/env python
#Jearld Jose
import random
from progress.bar import Bar


PEOPLE = [
  '$1',
  '$2',
  '$5',
  '$10',
  '$20',
  'Joker'
]


print("\n\n")
bar = Bar('You won...', max=10)
for i in range(54+1):
    [x for x in range(60000)]  # short pause...
    bar.next()
bar.finish()
print("\n\n\t{}!\n\n".format(random.choice(PEOPLE)))
print("-" * 60 + "\n")