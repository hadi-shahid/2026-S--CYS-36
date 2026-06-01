Question_Bank = [{"Subject":"Physics","Q":"A car starts from rest and accelerates at 2m/s for 5 seconds. What distance does it cover?","A": 10 ,"B": 15, "C": 25 ,"D":50 ,"Ans": "C"},
                 {"Subject":"Physics","Q":"The SI unit of electric current is?","A": "Volt" ,"B": "Coulomb" ,"C": "Ampere" ,"D": "Ohm","Ans":"C"},
                 {"Subject":"Maths","Q":"If x^2 - 16 = 0, then the values of x are:","A": 4 ,"B": -4 ,"C" : 2 ,"D" : 0 ,"Ans":"C"},
                 {"Subject":"Maths","Q":"What is the value of sin 90∘ ?","A": 0 ,"B": 1 ,"C": 2 ,"D": -1,"Ans":"B"},
                 {"Subject":"Chemistry","Q":"Which gas is released when acids react with metals?","A": "Oxygen" ,"B": "Nitrogen" ,"C": "Hydrogen" ,"D": "Carbon dioxide","Ans":"C"},
                 {"Subject":"Chemistry","Q":"The atomic number of carbon is:","A": 4 ,"B": 6 ,"C": 8 ,"D": 12,"Ans":"B"},
                 {"Subject":"English","Q":"Choose the correct synonym of “Brave”:","A": "Cowardly" ,"B": "Fearful" ,"C": "Courageous" ,"D": "Weak","Ans":"C"},
                 {"Subject":"English","Q":"Choose the correct sentence:","A": "She do not like tea." ,"B": "She does not likes tea." ,"C": "She does not like tea." ,"D": "She not like tea.","Ans":"C"},
                 {"Subject":"Computer","Q":"Which of the following is an input device?","A": "Monitor" ,"B": "Printer" ,"C": "Keyboard" ,"D": "Speaker","Ans":"C"},
                 {"Subject":"Computer","Q":"In which programming language is this code written?","A": "Java" ,"B": "Python" ,"C": "C" ,"D": "C++","Ans":"B"},
                 {"Subject":"Computer","Q":"What was the 1st programming language ever?","A":"Java","B":"C","C":"Python","D":"C++","Ans":"B"},
                 {"Subject":"Computer","Q":"Where was C lanuage developed?","A":"Lahore","B": "AT & T Bell Lab","C": "Singapor","D": "Kroasia","Ans":"B"}]

import sys
#Correct Admin Credentials
username_Admin = "ecat_admin"
password_Admin = "ecat@2024"
#Correct Student Credentials
username_Student = "student"
password_Student = "student123"
Total_Result = []
def login (correct_user,correct_pass):
    max_attempts = 3
    while max_attempts > 0:
        u = input("Username :")
        p = input("Password :")
        if u == correct_user and p == correct_pass:
             print("Welcome Login Successful !")
             return True
        max_attempts -= 1
        print(f"Invalid Credentials\nAttempts Remaining : {max_attempts}")
    
    print("Maximum Number of Attempts Reached.\nAccount Locked.")
    sys.exit()

def grades(percentage):
    if percentage >= 80:
        return("Excellent")
    elif percentage >=65:
        return("Good")
    elif percentage >=50:
        return("Average")
    
    else:
        return("Below Average")
def add_questions():
    print("----Add New Questions----")
    subject = input("Enter Subject : ")
    q_text = input("Enter the Question : ")
    op_a = input("Enter Option A : ")
    op_b = input("Enter Option B : ")
    op_c = input("Enter Option C : ")
    op_d = input("Enter Option D : ")
    ans = input("Enter Correct Option : ").strip().upper()
    if ans not in ["A","B","C","D"]:
        print ("Invalid Choice ! Answer must be A / B / C / D.")
        return
    Question_Bank.append({"Subject":subject,"Q":q_text,"A":op_a,"B":op_b,"C":op_c,"D":op_d,"Ans":ans})
    print("\nQuestion has been Added !\n")

def delete_questoins():
    if not Question_Bank:
        print("Question Bank is Empty !")
        return
    print("\n----Delete Question----")
    for i,q in enumerate(Question_Bank,1):
        print(f"{i}.[{q["Subject"]}] {q["Q"]}")
    try:
        num = int(input("Enter Question Number to Delete : "))
        if 1 <= num <= len(Question_Bank):
            removed = Question_Bank.pop(num-1)
            print(f"Deleted Question : {removed["Q"]}")
        else:
            print("Invalid Number !")
    except ValueError:
        print("\nPlease enter a Valid Number !\n")

def class_stats():
    if not Total_Result:
        print("\nNo Students Results Yet !\n")
        return
    scores = [r["Score"] for r in Total_Result]
    percentages = [r["Percentage"] for r in Total_Result]
    highest = max(scores)
    lowest = min(scores)
    average = sum(scores)/ len(scores)
    pass_count = sum(1 for p in percentages if p >= 50)
    fail_count = len(percentages) - pass_count

    grades_count = {}
    for r in Total_Result:
        g = r["Grade"]
        grades_count[g] = grades_count.get(g,0) + 1

    print("\n----Class Result Statistics----\n")
    print(f"Total Students : {len(Total_Result)}")
    print(f"Highest Score :  {highest}")
    print(f"Lowest Score :  {lowest}")
    print(f"Average Score :  {average:.2f}")
    print(f"Pass Students :  {pass_count}")
    print(f"Fail Students :  {fail_count}")
    print(f"Grade Distribution : {grades_count}")


def run_exam (name,rollno):
    global Total_Result
    correct = 0
    wrong = 0
    skipped = 0
    my_answers = []
    print (f"Exam Starting for  \n\t\tName : {name}, Roll no. : {rollno}")
    print("\nEnter A/B/C/D to answer, \tor S to Skip Question. \tType Submit to end exam early.\n")
    ended = False
    
    for i,q in enumerate(Question_Bank,1):
        if ended:
              my_answers.append("S")
              skipped += 1
              continue
        print(f"Q{i}: [{q["Subject"]}]{q["Q"]}")
        print(f"A) {q['A']} B) {q['B']} C) {q['C']} D) {q['D']}")
        while True:
            answers = input("Answer : ").strip().upper()
            if answers == "SUBMIT":
                ended = True
                my_answers.append("S")
                skipped += 1
                break
            elif answers in ["A","B","C","D"]:
                my_answers.append(answers)
                if answers == q["Ans"]:
                    correct += 1
                else:
                    wrong += 1
                break
            elif answers == "S":
                my_answers.append("S")
                skipped += 1
                break
            else:
                print("Invalid Input ! Enter A/B/C/D, S or Submit")

    score = (correct * 4)-wrong
    score = max(0,score) # For no -ve values
    max_score = len(Question_Bank) * 4
    percentage = round((score / max_score)*100,1)
    your_grade = grades(percentage)
    print("\n Your Result !")
    print(f"Name : {name} | Roll no. : {rollno}")
    print(f"Correct : {correct} | Wrong : {wrong} | Skipped : {skipped}")
    print(f"Your Score : {score}/{max_score}")
    print(f"Percentage : {percentage}")
    print(f"Grade : {grades(percentage)}")
    
    print("ANSWER REVIEW :")
    
    Total_Result.append({"Name":name,"Roll no.":rollno ,"Score":score,"Percentage":percentage,"Grade":grades(percentage),"Answer":my_answers})
    print("\n\t\t Result Saved !")

    for i,q in enumerate(Question_Bank,1):
        given = my_answers[i-1]
        if given == "S":
            status = "Skipped"
        elif given == q["Ans"]:
            status = "Correct !"
        else:
            status = f"Wrong(Ans: {q["Ans"]})"

        print("Q"+str(i + 1)+" You : "+given+"-> "+status)
    
def view_results():
    if not Total_Result:
        print("\n----No Results Yet ! ----\n")
        return
    print("\n\t\t ----All Results----")
    for r in sorted(Total_Result,key=lambda x : x["Score"],reverse=True ):
        print(f"Name : {r["Name"]} | Roll no. : {r["Roll no."]} | Score : {r["Score"]} | Percentage : {r["Percentage"]} % | Grade : {r["Grade"]}")
    print( )

def main():
    while True:
        print ("==== Ecat Exam Application ====")
        print("1. Admin Portal")
        print("2. Student Portal")
        print("3. Exit Application")
        choice = (input("Select (1/2/3) : ")).strip()

        if choice == '1':
            print("Welcome Admin !")
            if login (username_Admin,password_Admin):
                while True:
                    print("----Admin Menu----")
                    print("1. Add New Question")
                    print("2. Delete a Question")
                    print("3. View Class Results")
                    print("4. View Questions")
                    print("5. View Student Results")
                    inp = input("Select (1/2/3/4/5/6) : ").strip( )

                    if inp == '1':
                        if not login():
                            print("Exting Portal...")
                            sys.exit()      
                        add_questions()
                    elif inp == '2':
                        delete_questoins()
                    elif inp == '3':
                        class_stats()
                    elif inp == '4':
                        for i,q in enumerate(Question_Bank,1):
                            
                            print(f"\nQ{i},[{q["Subject"]}] {q["Q"]}")
                            print(f"A) {q["A"]} B) {q["B"]} C) {q["C"]} D) {q["D"]}")
                            print(f"Answer : {q["Ans"]}")
                    elif inp == '5':
                        view_results()
                    elif inp == '6':
                        break
                    else:
                        ("Invalid Choice")
        elif choice == '2':
            print("Welcome Student !")
            if login(username_Student,password_Student):
                    name = input("Name : ")
                    roll_no = input("Roll no. : ").strip( )
                    if not name or not roll_no:
                        print("Name and Roll no. Can not be Empty !\n")
                        continue
                    while True:
                        print("----Student Menu----")
                        print("1. Exam Rules")
                        print("2. Start Exam")
                        print("3. Logout")
                        inp_2 = input("Select (1/2/3) : ")
                        if inp_2 == '1':
                            print("----Rules----") 
                            print("\t\t\n Test Rules : \n1. If you miss your allotted time/session. \n2. Retest is not allowed. \n3. No rechecking facility is available because the test is computerized. \n4. Registration fee is non-refundable and non-transferable. \n5. Reach the center at least 30 minutes before the exam starts.\n6. Grading : \nA-Grade if Grade >= 80 % \nB-Grade if Grade >= 70 % \nC-Grade if Grade >= 60 % \nD-Grade if Grade >= 50 % \nFail if Grade < 50 %")
                        elif inp_2 == '2':
                            run_exam(name,roll_no)
                            break
                        elif inp_2 == '3':
                            break
                        else:
                            ("Invalid Choice")
        elif choice == '3':
            print("Exiting Ecat Portal...")
            break
        else:
            print("\nInvalid Choice. Try Again \n")
if __name__ =="__main__":
    main ()







