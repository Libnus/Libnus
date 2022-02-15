import csv
from tabulate import tabulate
from os.path import exists
from datetime import datetime
import pickle


#def view_grades():

#def view_gpa():

#returns to main menu

global current_menu
global assignments
global current_class
current_menu = 'main'
current_class = ''

classes = []

#course class
class Course(object):
	def __init__(self, course_name, credits, categories, assignments):
		self.__course_name = course_name
		self.__credits = credits
		self.__assignments = assignments
		self.__categories = categories

	def get_class(class_input):
		for course in classes:
			if Course.course_name(course) == class_input:
				return course

	def course_name(self):
		return self.__course_name

	def credits(self):
		return self.__credits

	def assignments(self):
		return self.__assignments

	def remove_assign(self, assignment):
		print(self.__assignments)
		self.__assignments.remove(assignment)

	def append_assignments(self, assignment):
		self.__assignments.append(assignment)

	def categories(self):
		return self.__categories

class Assignment(object):
	def __init__(self, assignment_name, grade, total_points, category):
		self.__assignment_name = assignment_name
		self.__grade = grade
		self.__category = category
		self.__total_points = total_points

	def assignment_name(self):
		return self.__assignment_name

	def grade(self):
		return self.__grade

	def total_points(self):
		return self.__total_points

	def category(self):
		return self.__category

#open files
# classes = []
# file_exists = exists('classes.csv')
# if file_exists:
# 	classes = []
# 	with open('classes.csv', 'r') as myfile:
# 		csv_reader = csv.reader(myfile)
# 		classes = (list(csv_reader))
		
# else:
# 	classes = []

def parse_line(course):
	new_course = course.split(',')
	categories = new_course[2]
	print(categories)

def read_in():
	global classes
	f = open('classes.pickle', 'rb')
	classes = pickle.load(f)
	f.close()

def write_out():
	f = open('classes.pickle', 'wb')
	pickle.dump(classes, f)
	f.close()

def create_class(class_name, credits, categories, assignments):
	new_class = Course(class_name, credits, categories, assignments)
	classes.append(new_class)

def create_assignment(assignment_name, grade, total_points, category):
	new_assignment = Assignment(assignment_name, grade, total_points, category)
	print(new_assignment)

	Course.append_assignments(current_class, new_assignment)

	print(Course.get_assignments(current_class))

# removes an assignment from the assignments list for a given course
def remove_assignment(assignment_removed):
	assignments = Course.assignments(current_class)
	print('assignments', assignments)

	print('assignemnt_to be removed', next(x for x in assignments if Assignment.assignment_name(x) == assignment_removed))
	Course.remove_assign(current_class, [next(x for x in assignments if Assignment.assignment_name(x) == assignment_removed)])

#view classes
def view_classes():
	new_classes = []
	for course in classes:
		new_classes.append([Course.course_name(course), Course.credits(course)])
	print()
	print((tabulate(new_classes, headers=["Class Name", "Credits"], tablefmt="fancy_grid")))
	print()

def is_category(category):
	global current_class
	return any(c[0] == category for c in Course.categories(current_class))

def view_categories():
	categories = Course.categories(current_class)

	print(tabulate(categories, headers=['Category', 'Weight'], tablefmt='fancy_grid'))

#view assignments for a given class
def view_assignments():
	assignments = Course.assignments(current_class)

	readable_assignments = [(Assignment.assignment_name(x), Assignment.grade(x), Assignment.category(x)) for x in assignments]

	if assignments == None: 
		print("No assignments yet!")
	# huhj2@rpi.edu

	print(tabulate(readable_assignments, headers=["Assignment Name", "Grade", "Total Points", "Category"], tablefmt="fancy_grid"))

def change_menu(new_menu):
	global current_menu
	current_menu = new_menu
	print("==========================================================================================================================================================")
	print_menu()

def print_menu():
	global courses
	if current_menu == 'main':
		print("\n\t\t\t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
		print("\t\t\t\t\t\tVIEW")
		print("\n\t\t\t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
		print("\t\t\t\t(1) View grades")
		print("\t\t\t\t(2) View GPA")
		print("\t\t\t\t(3) View Classes")
		print("\n\t\t\t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
		print("\t\t\t\t\t\tNEW")
		print("\n\t\t\t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
		print("\t\t\t\t(4) Create new class")
		print("\t\t\t\t(5) Edit grades in existing class")
		print("\t\t\t\t(6) Add new semester")

		user_input = input("\n\t\t\t\tWhat would you like to do? (type \'exit\' to exit) :: ")
		user_input = user_input.strip()

		while user_input.lower() != 'exit':
			if user_input == '1':
				view_grades()

			elif user_input == '2':
				view_gpa()

			elif user_input == '3':
				view_classes()
				change_menu('view')

			# 'new' functions
			elif user_input == '4':
				change_menu('create')

			elif user_input == '5':
				change_menu('class_view')

		print("GOODBYE!!")
		write_out()
		quit()

	elif current_menu == 'view':
		while True:
			user_input = input("Type \'!b\' to go back: ")
			if user_input == '!b':
				break
		change_menu('main')

	elif current_menu == 'class_view':
		global current_class
		view_classes()
		class_input = input("Please select a class (\'!b\' to go back): ")
		class_input = class_input.strip()
		if class_input == '!b':
			change_menu('main')
		current_class = Course.get_class(class_input)
		view_assignments()
		change_menu('assignment_view')

	elif current_menu == 'assignment_view':
		while True:
			print("(1) Add Assignment")
			print("(2) Edit Assignment (NOT FUNCTIONAL)")
			print("(3) Remove Assignment")
			user_input = input("Select (\'!b\' to go back) :: ")
			if user_input == '!b':
				current_class == None
				break

			elif user_input == '1':
				view_categories()
				assignment_name = input('\t\t\t\tAssignment Name: ')
				assignment_name.strip()
				grade = input('\t\t\t\tGrade (points i.e. 40/50 you would enter 40): ')
				total_points = input('\t\t\t\tTotal Points: ')
				try:
					grade = float(grade)
					total_points = int(total_points)
				except:
					print('\t\t\t\tGrade not a number!')
				category = input('\t\t\t\tCategory: ')
				category = category.strip()
				if is_category(category):
					print('\t\t\t\tAssignment added!')
				else:
					print('\t\t\t\tCategory entered not a category!')
				view_assignments()

			# TO-DO
			# elif user_input == '2':

			elif user_input == '3':
				if len(Course.assignments(current_class)) == 0:
					print('No assignments yet!')
					continue

				assignment_name = input('\t\t\t\tAssignment Name: ')
				assignment_name = assignment_name.strip()
				remove_assignment(assignment_name)

		change_menu('class_view')

	elif current_menu == 'create':
		print()
		class_name = input("\t\t\t\tName of class: ")
		class_name = class_name.strip()
		categories = []
		print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		print('\nCategories view: Please enter grading categories for this class! (enter -1 when done adding categories)')
		print('WARNING :: YOU CANNOT ADD CATEGORIES OR CHANGE THEM WHEN THE CLASS IS CREATED!')
		print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		while True:
			categories_0 = input("\nEnter a category name (a cateogry is grade category (ie \'Exam\' or \'Homework\')):")
			categories_0 = categories_0.strip()
			if categories_0 == '-1':
				break
			categories_1 = input("Enter the weight of that category: ")
			categories_1 = categories_1.strip()
			try:
				categories_1 = int(categories_1)
				categories.append((categories_0, categories_1))
			except:
				print("The weight you entered is not valid!")
		credits = input("Number of credits (must be whole number): ")

		try:
			credits = int(credits)
			if credits <= 0:
				print("\t\t\t\tError! Credits cannot be negative or 0!")

		except:
			print("\t\t\t\tError! Number is not accepted! Enter a whole number")

		create_class(class_name, credits, categories, [])

		print("\n\t\t\t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

		change_menu('main')

if __name__ == '__main__':
	read_in()
	date = str(datetime.today())[0:10]
	if date == '2021-10-31':
		print("""
				                      ███ 
				                    ███ 
				                   ██ 
				                  ██ 
				                 ███ 
				        █████████████████████ 
				     ███████████████████████████ 
				   ███████████████░███████████████ 
				 ██████████░██████░██████░█████████ 
				 █████████░░░█████░█████░░░█████████ 
				█████████░░░░░████░████░░░░░████████ 
				████████░░░░░░░███░███░░░░░░░████████ 
				██████████████████░██████████████████ 
				█████████████████░░░█████████████████ 
				████████░░░████████████████░░████████ 
				 ███████░░░░░░░░░░░░░░░░░░░░░███████ 
				  ████████░░░░░░░░░░░░░░░░░████████ 
				   ██████████████████████████████ 
				    ███████████████████████████


	   ▄██████▄   ▄█        ▄█      ███         ███        ▄████████    ▄████████ 
	  ███    ███ ███       ███  ▀█████████▄ ▀█████████▄   ███    ███   ███    ███ 
	  ███    █▀  ███       ███▌    ▀███▀▀██    ▀███▀▀██   ███    █▀    ███    ███ 
	 ▄███        ███       ███▌     ███   ▀     ███   ▀  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
	▀▀███ ████▄  ███       ███▌     ███         ███     ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
	  ███    ███ ███       ███      ███         ███       ███    █▄  ▀███████████ 
	  ███    ███ ███▌    ▄ ███      ███         ███       ███    ███   ███    ███ 
	  ████████▀  █████▄▄██ █▀      ▄████▀      ▄████▀     ██████████   ███    ███ 
	             ▀                                                     ███    ███ 

			""")
	else:
		print("""
			 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
			| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
			| |    ______    | || |   _____      | || |     _____    | || |  _________   | || |  _________   | || |  _________   | || |  _______     | |
			| |  .' ___  |   | || |  |_   _|     | || |    |_   _|   | || | |  _   _  |  | || | |  _   _  |  | || | |_   ___  |  | || | |_   __ \\    | |
			| | / .'   \\_|   | || |    | |       | || |      | |     | || | |_/ | | \\_|  | || | |_/ | | \\_|  | || |   | |_  \\_|  | || |   | |__) |   | |
			| | | |    ____  | || |    | |   _   | || |      | |     | || |     | |      | || |     | |      | || |   |  _|  _   | || |   |  __ /    | |
			| | \\ `.___]  _| | || |   _| |__/ |  | || |     _| |_    | || |    _| |_     | || |    _| |_     | || |  _| |___/ |  | || |  _| |  \\ \\_  | |
			| |  `._____.'   | || |  |________|  | || |    |_____|   | || |   |_____|    | || |   |_____|    | || | |_________|  | || | |____| |___| | |
			| |              | || |              | || |              | || |              | || |              | || |              | || |              | |
			| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
			 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 

			 									Welcome to Glitter!
			 									~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			 											The ultimate grading tool
	    	""")

	change_menu('main')

	

	
			
    