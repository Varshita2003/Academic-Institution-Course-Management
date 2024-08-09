HOW TO RUN THE PYTHON CODE : 
1. In the code ,in line 124 change the password to that of the local host server . 
2. Save the file and run the following command on terminal :
	python3 dbms_assignment4.py
3. Make sure tkinter and mysql connector is installed before . If not run the following : 
	pip install mysql-connector
	sudo apt-install python3-tk



DETAILS ABOUT THE CODE :

	For the first part : Addition of courses 
	1. We take the department id, course id, teacher id and class room from the user as input  
	2. We verify if the department id is valid 
	3. We verify if the course id is present in the department (this automatically means that the course id is valid)
	4. We verify if the teacher id is valid
	5. We check if the teaching couple is already there in the teaching table in the even semester of 2006
	6. If all the validations are successful then we check if the teaching tuple is already present if not we add the course to the teaching table appropriately

	For the second part : Student enrollment 
	1. This part of the code can only executed if there is some courses was added since we are using the department id of the last course updated
	2. In this part we take the roll No and course Id from the user as input
	3. We check if the course is in the department of the last added course and also check if there is the course is there in the teaching of the even semester of 2006
	4. We verify if the roll No is valid
	5. We verify if the Student has successfully passed all the prerequisite courses of the input course id before the even semester of 2006
	6. We also check if the Student had done the course before or not :
		i. If the Student did the course before 2006 even semester and failed in it (i.e got an 'W' or 'U' grade) we add then add the enrollment tuple
		ii. If the Student passed the course before the 2006 even semester we don't add the course
	7. The grade of the added tuple in enrollment table is set to NULL by default

	For both the cases we have displayed appropriate error messages in case of the updation failure!
