# This file is required. Use the same name, "test.py". Below you see an example
# of importing a class from "source.py", instantiating a new object and printing
# that object. Replace the code below with your own.

from source import Adequacy

print("What are your points being used for?")
print("")
print("1. Monument or Survey")
print("2. Engineering or Research Project")
print("3. Topography Map or Drainage Map")
print("")
user_input = input("Pick 1, 2, or 3: ")
aduequacy = Adequacy('Vertical Measurements.csv', user_input)
