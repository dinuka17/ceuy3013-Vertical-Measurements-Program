# This file is required. Use the same name, "source.py".
# All of your *foundational* code goes here, meaning the functions and classes
# that can be used to build larger processes. For example, the class you
# created for the OOP assignment would go here.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Adequacy:
  def __init__(self, csv_file, user_input):
    self.csv_file = csv_file
    self.user_input = user_input
    df = pd.read_csv(self.csv_file)
    self.error_of_Closure_in = self.find_error_of_closure(df)
    self.allowable_error = self.find_allowable_error()
    self.first_order_equation = 0
    self.second_order_equation = 0
    self.third_order_equation = 0
    self.compare_errors(df)
    

  def find_error_of_closure(self, df):
    row_difference = df["H.I."]-df["F.S. (-)"] #Adding additional Elevation column to initial data
    df['Elevation'] = row_difference 
    df.to_csv('New Initial Meaurements.csv') #Now we will save this new updated initial dataset
#The next step is to find the cumulative length when going from one station to the next. 
#The end goal is to find if the Allowable Error of Closure for whatever Order this program is for, is good or not. 
#If the Error of Closure is less than the Allowable Error of Closure for Whatever order and whatever length the program is intended for, then those points can be used to construct a site layout. 
    df['Cumulative Length of Course(FEET)'] = df['LENGTH COURSE (FEET)'].cumsum() #The goal of this cell block is to create an entirely new column that has the cumulative sum of the Course Length Column
# With the cumulative length column, the next step is finding the ratio of the cumulative length over the total length of the course. 
#The total length of the entire course is the last value in the Cumulative Length fo course (FEET) column. 
#Therefore, we will need to create a new variable that takes this point from our CSV
    total_course_length = df.at[4,'Cumulative Length of Course(FEET)'] # applying at/iat function to retrieve a value from a Pandas 
#First Class: Used to establish permanent survey monuments for National Control Network
#Second Class: Used for major Engineering and Research Projects
#Third Class: Serves as vertical references for projects, topography maps and drainage maps
    self.first_order_equation = 0.12*((total_course_length/3281)**0.5)
    self.second_order_equation = 0.24*((total_course_length/3281)**0.5)
    self.third_order_equation = 0.48*((total_course_length/3281)**0.5)
    df['Length Ratio'] = df['Cumulative Length of Course(FEET)'] / total_course_length
#The next step is adding a correction column to our DataFrame. To obtain the correction factor, the length ratio of each point must
#be multiplied by the difference in the elevation of the First Point, and the last. The first and last points are the same, but due
#to human error in taking measurements due to differential leveling, they are not the same. 
    first_and_last_points_difference = df.at[0,'Elevation'] - df.at[4,'Elevation']
    df['Correction Factor'] = df['Length Ratio'] * first_and_last_points_difference
    df['Adjusted Elevations'] = df['Elevation'] - df['Correction Factor']
    error_of_Closure_ft = df.at[0,'Adjusted Elevations'] - df.at[4,'Adjusted Elevations']
    error_of_Closure_in = abs(error_of_Closure_ft * 12)
    return error_of_Closure_in

  def compare_errors(self, df):
    if self.allowable_error < 0:
      print("Invalid input, try again.")
    else:
      if self.allowable_error < self.error_of_Closure_in:
          print("Your measurements are inadequate and you must take new measurements before proceeding with Site Layout.")
      else:
          print("Your measurements are good and you may proceed with Site Layout.")
          x, y = df['POINT'], df['Adjusted Elevations']
          plt.scatter(x, y)
          plt.title('Adjusted Points', fontweight='black', fontsize=18)
          plt.xlabel('Points', fontweight='bold')
          plt.ylabel('Elevation (ft)', fontweight='bold')
          plt.show()

  def find_allowable_error(self):
    if self.user_input == "1":
        return self.first_order_equation
    elif self.user_input == "2":
        return self.second_order_equation
    elif self.user_input == "3":
        return self.third_order_equation
    else:
        return -1
    

#TEST FILE

def main():

  print("What are your points being used for?")
  print("")
  print("1. Monument or Survey")
  print("2. Engineering or Research Project")
  print("3. Topography Map or Drainage Map")
  print("")
  user_input = input("Pick 1, 2, or 3: ")
  aduequacy = Adequacy('Vertical Measurements.csv', user_input)

main()

