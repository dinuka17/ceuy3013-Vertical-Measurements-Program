**This is the Source that has all the step-by-step docstring of what each variable is and my thought process.**

#Since we will be manipulating numerical tables, we will need to import pandas first

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#The first thing we will import are the vertical measurments that will be taken manually using tools like the theodolite and the total station

df = pd.read_csv('Vertical Measurements.csv')

"""This program is intended to run when there is a CSV file that is uploaded with 5 columns and 6 rows. This means it is limited to a survey that has only 4 points, like in this case A through D. The first column has the names of the points, this can be letters or specific names. For instance, instead of point A, a surveyer could indicate point A to be an item like a tree or some sort of permanent monument to indicate where it was taken. The second solumn, abbreviated as BS (+) is the Backsight, and this is the first sight taken with a leveling staff, there is only one backsight and the rest of the values are zero for backsight afterwards. The next column is the H.I. which is the height of the instrument, which is constant throughout the experiment. The F.S. is the Fore Sight, which is the last staff reading taken (There is a minus because Foresight is considered "minus sight"). The last column in this CSV file is the Length of the Course, which is the distance between the point and the one right before it. 

In this initial data, what is missing is the Elevation, which is the difference between the Height of the Instrument and the Fore Sight.
"""

#Adding additional Elevation column to initial data

row_difference = df["H.I."]-df["F.S. (-)"]
df['Elevation'] = row_difference

#Now we will save this new updated initial dataset

df.to_csv('New Initial Vertical Measurements.csv')

#The next step is to find the cumulative length when going from one station to the next. 
#The end goal is to find if the Allowable Error of Closure for whatever Order this program is for, is good or not. 
#If the Error of Closure is less than the Allowable Error of Closure for Whatever order and whatever length the program is intended for, then those points can be used to construct a site layout. 


""" THe goal of this cell block is to create an entirely new column that has the cumulative sum of the Course Length Column
"""
df['Cumulative Length of Course(FEET)'] = df['LENGTH COURSE (FEET)'].cumsum()

# With the cumulative length column, the next step is finding the ratio of the cumulative length over the total length of the course. 
#The total length of the entire course is the last value in the Cumulative Length fo course (FEET) column. 
#Therefore, we will need to create a new variable that takes this point from our CSV

# applying at/iat function to retrieve a value from a Pandas 
total_course_length = df.at[4,'Cumulative Length of Course(FEET)']

#Add a new column with the ratio now
df['Length Ratio'] = df['Cumulative Length of Course(FEET)'] / total_course_length

#The next step is adding a correction column to our DataFrame. To obtain the correction factor, the length ratio of each point must
#be multiplied by the difference in the elevation of the First Point, and the last. The first and last points are the same, but due
#to human error in taking measurements due to differential leveling, they are not the same. 

first_and_last_points_difference = df.at[0,'Elevation'] - df.at[4,'Elevation']

df['Correction Factor'] = df['Length Ratio'] * first_and_last_points_difference

#Now we can get the last column of the adjusted elevations

df['Adjusted Elevations'] = df['Elevation'] - df['Correction Factor']

#Now we're finding the error of closure from our points. The error of closure will be converted into inches because the formula to get
#the Allowable Error of Closure is set in inches

error_of_Closure_ft = df.at[0,'Adjusted Elevations'] - df.at[4,'Adjusted Elevations']
error_of_Closure_in = abs(error_of_Closure_ft * 12)

#Here we create variables for the Allowable Error Of Closure based on what type of Survey the points are taken for

"""
First Class: Used to establish permanent survey monuments for National Control Network
Second Class: Used for major Engineering and Research Projects
Third Class: Serves as vertical references for projects, topography maps and drainage maps
"""

first_order_equation = 0.12*((total_course_length/3281)**0.5) 
second_order_equation = 0.24*((total_course_length/3281)**0.5) 
third_order_equation = 0.48*((total_course_length/3281)**0.5) 


#First have to create a way for the user to select what kind of Survey they are using the points for. This will
#given to them in a selectable manner, like multiple choice. 

def main():
    allowable_error = finding_equation()
    print('Your allowable error is: ', allowable_error)
    compare_errors(allowable_error, error_of_Closure_in)
    
def compare_errors(allowable_error, error_of_Closure_in):
    if allowable_error < error_of_Closure_in:
        print("Your measurements are inadequate and you must take new measurements before proceeding with Site Layout.")
    else:
        print("Your measurements are good and you may proceed with Site Layout.")

        x, y = df['POINT'], df['Adjusted Elevations']
        plt.scatter(x, y)

        plt.title('Adjusted Points', fontweight='black', fontsize=18)
        plt.xlabel('Points', fontweight='bold')
        plt.ylabel('Elevation (ft)', fontweight='bold')
        plt.show()

def finding_equation():
    print("What are your points being used for?")
    print("")
    print("1. Monument or Survey")
    print("2. Engineering or Research Project")
    print("3. Topography Map or Drainage Map")
    print("")
    equation = ""
    user_input = input("Pick 1, 2, or 3: ")
    if user_input == "1":
        equation = first_order_equation
    elif user_input == "2":
        equation = second_order_equation
    elif user_input == "3":
        equation = third_order_equation
    else:
        print("Invalid input, try again.")
    return equation
    
main()