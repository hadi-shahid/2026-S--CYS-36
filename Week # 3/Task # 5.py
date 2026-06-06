def calculate_gpa(subjects):
    total_grade_point = 0
    total_credit_hours = 0
    for i in range(subjects):
        grade_point = float(input(f"Enter Grade Point for Subjects {i+1} : "))
        credit_hour = float(input(f"Enter Credit Hours for Subjects {i+1} : "))
        total_grade_point += grade_point * credit_hour
        total_credit_hours += credit_hour
    gpa = total_grade_point / total_credit_hours
    return gpa

num_subjects = int(input("Enter The Number of Subjects in The Semester : "))
gpa = calculate_gpa(num_subjects)
print(f"Your GPA for The Semester is : {gpa}")