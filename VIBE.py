"""Student Grade Calculator."""

from pathlib import Path


DATA_FILE = Path("student_grades.txt")


class Student:
	"""Store a student's identifying information and calculated grade."""

	def __init__(self, name, student_id, test1, test2, test3):
		self.name = name
		self.student_id = student_id
		self.test_scores = [float(test1), float(test2), float(test3)]
		self.average = sum(self.test_scores) / len(self.test_scores)
		self.grade = self.calculate_grade()

	def calculate_grade(self):
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	def to_file_format(self):
		scores = "|".join(f"{score:.2f}" for score in self.test_scores)
		return f"{self.name}|{self.student_id}|{scores}|{self.average:.2f}|{self.grade}"


def is_exit_command(value):
	"""Return whether input represents the requested ESC exit command."""
	return value.strip().upper() in {"ESC", "\x1b"}


def load_students(filename=DATA_FILE):
	"""Load student records, skipping malformed lines with a clear message."""
	students = []
	try:
		with filename.open("r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|")
				if len(fields) != 7:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				try:
					students.append(Student(fields[0], fields[1], *fields[2:5]))
				except ValueError:
					print(f"Skipping invalid scores on line {line_number}.")
	except FileNotFoundError:
		return students
	except OSError as error:
		print(f"Could not load student records: {error}")
	return students


def save_students(students, filename=DATA_FILE):
	"""Save all student records in the required pipe-delimited format."""
	try:
		with filename.open("w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_format() + "\n")
		print(f"Saved {len(students)} student record(s).")
		return True
	except OSError as error:
		print(f"Could not save student records: {error}")
		return False


def prompt_score(test_number):
	"""Prompt until a test score from 0 through 100 is entered."""
	while True:
		value = input(f"Test {test_number} score (0-100): ").strip()
		if is_exit_command(value):
			return None
		try:
			score = float(value)
			if 0 <= score <= 100:
				return score
		except ValueError:
			pass
		print("Please enter a number from 0 to 100, or type ESC to exit.")


def add_student(students):
	"""Prompt for and append one student record."""
	name = input("Student name (or ESC to cancel): ").strip()
	if is_exit_command(name):
		return False
	student_id = input("Student ID (or ESC to cancel): ").strip()
	if is_exit_command(student_id):
		return False

	scores = []
	for test_number in range(1, 4):
		score = prompt_score(test_number)
		if score is None:
			return False
		scores.append(score)

	student = Student(name, student_id, *scores)
	students.append(student)
	print(f"Added {student.name}. Average: {student.average:.2f}, Grade: {student.grade}")
	return True


def display_students(students):
	"""Display every student in a readable table."""
	if not students:
		print("No student records found.")
		return

	header = f"{'Name':<22} {'ID':<14} {'Test 1':>7} {'Test 2':>7} {'Test 3':>7} {'Average':>9} {'Grade':>5}"
	print("\n" + header)
	print("-" * len(header))
	for student in students:
		test1, test2, test3 = student.test_scores
		print(
			f"{student.name:<22.22} {student.student_id:<14.14} "
			f"{test1:>7.2f} {test2:>7.2f} {test3:>7.2f} "
			f"{student.average:>9.2f} {student.grade:>5}"
		)


def display_statistics(students):
	"""Display highest, lowest, and overall class averages."""
	if not students:
		print("No student records found.")
		return
	averages = [student.average for student in students]
	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	print(f"Highest average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest average: {lowest.average:.2f} ({lowest.name})")
	print(f"Class average: {sum(averages) / len(averages):.2f}")


def search_students(students):
	"""Display records whose names contain the search text."""
	search_term = input("Enter a student name to search (or ESC to cancel): ").strip()
	if is_exit_command(search_term):
		return
	matches = [student for student in students if search_term.casefold() in student.name.casefold()]
	if matches:
		display_students(matches)
	else:
		print("No matching students found.")


def display_menu():
	print("\nStudent Grade Calculator")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search by name")
	print("5. Save records")
	print("Type ESC to save and exit.")


def main():
	students = load_students()
	if students:
		print(f"Loaded {len(students)} student record(s).")
	else:
		print("No saved student records found.")

	while True:
		display_menu()
		choice = input("Choose an option: ").strip()
		if is_exit_command(choice):
			save_students(students)
			print("Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_students(students)
		elif choice == "5":
			save_students(students)
		else:
			print("Invalid choice. Select 1-5 or type ESC to exit.")


if __name__ == "__main__":
	main()