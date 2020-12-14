# Vertical Measurements Program
*This is a demo project for "CE-UY 3013 Computing In Civil Engineering". It's purpose is to check the adequacy of Vertical Measurements taken before a Site Layout.
* 

This program is intended to run when there is a CSV file that is uploaded with 5 columns and 6 rows. This means it is limited to a survey that has only 4 points, like in this case A through D. The first column has the names of the points, this can be letters or specific names. For instance, instead of point A, a surveyer could indicate point A to be an item like a tree or some sort of permanent monument to indicate where it was taken. The second solumn, abbreviated as BS (+) is the Backsight, and this is the first sight taken with a leveling staff, there is only one backsight and the rest of the values are zero for backsight afterwards. The next column is the H.I. which is the height of the instrument, which is constant throughout the experiment. The F.S. is the Fore Sight, which is the last staff reading taken (There is a minus because Foresight is considered "minus sight"). The last column in this CSV file is the Length of the Course, which is the distance between the point and the one right before it.

Inputs:
* CSV File with a 5x6 Table of the inputes with specific Column Names
* Know what type of project these points are for (Monument, Survey, Research, Engineering, etc. )

Outputs:
* New CSV file with adjusted elevations
* Adequacy of selected measurements
* Graph of the selected points if they are adequate


## How to use the program

If this task was done on Microsoft Excel, here is how some of it would appear. This method was very tedious and took hours to complete because it involved tedious manipulation of each column. Furthermore, it only derived the Error of Closure and did not compare with the Allowable Error for the type of Project this program will be used for. This program will do all the checks and simply output whether the points are adequate or inadequate for the type of Project they are intended for. If they are inaequate, the surveyer would need to re-do their Vertical Measurements so that the Error of Closure is less than the Allowable Error of Closure. 

![Screenshot of Excel Sample](https://user-images.githubusercontent.com/69228228/102020387-eb52a880-3d46-11eb-8e75-94027ca8d8ed.png) 

