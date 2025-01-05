from autofillqecteacher import autofiller3;
from autofillqecStudentcourse import autofiller2;
from autofillqeconlinelearingfeedback import autofiller1;

# Login credentials
Id = "230594"  # Replace with roll ID
Password = "pass"  # Replace password to your portal
Option = 3 # A = 1, B = 2, C = 3, D = 4
InstructorMessage = "Very good"
Coursemessage = "good not bad"
Totalteachers=9
totalcources=9

#made by https://github.com/milliyin

autofiller3(Id,Password,Option,InstructorMessage,Coursemessage,Totalteachers)
autofiller2(Id,Password,Option,InstructorMessage,totalcources)
autofiller1(Id,Password,Option,InstructorMessage,Totalteachers)