# This file is required. Use the same name, "source.py".
# All of your *foundational* code goes here, meaning the functions and classes
# that can be used to build larger processes. For example, the class you
# created for the OOP assignment would go here.

# Here is a test class, replace the code below with your own

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
    row_difference = df["H.I."]-df["F.S. (-)"]
    df['Elevation'] = row_difference
    df.to_csv('New Initial Meaurements.csv')
    df['Cumulative Length of Course(FEET)'] = df['LENGTH COURSE (FEET)'].cumsum()
    total_course_length = df.at[4,'Cumulative Length of Course(FEET)']
    self.first_order_equation = 0.12*((total_course_length/3281)**0.5)
    self.second_order_equation = 0.24*((total_course_length/3281)**0.5)
    self.third_order_equation = 0.48*((total_course_length/3281)**0.5)
    df['Length Ratio'] = df['Cumulative Length of Course(FEET)'] / total_course_length
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


