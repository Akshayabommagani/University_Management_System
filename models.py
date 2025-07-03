class person:
    def __init__(self, branch: str, name: str):
        self.branch = branch
        self.name = name

    def __str__(self) -> str:
        return f"Name: {self.name} | Branch: {self.branch}"

class student(person):
    def __init__(self, rollno, name, branch):
        super().__init__(branch, name)
        self.rollno = rollno

    def __str__(self) -> str:
        return f"Rollno: {self.rollno} | {super().__str__()}"

class teacher(person):
    def __init__(self, branch, name, subject):
        super().__init__(branch, name)
        self.subject = subject

    def __str__(self) -> str:
        return f"subject: {self.subject} | {super().__str__()}"
    
class college:
    def __init__(self, cname):
        self.cname = cname
        self.students = []
        self.teachers = []

    def add_student(self, s: student):
        self.students.append(s)

    def add_teacher(self, t: teacher):
        self.teachers.append(t)
