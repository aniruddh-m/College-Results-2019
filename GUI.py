from tkinter import *
import mysql.connector
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def setup_DB():
    # Setup the database
    mydb = mysql.connector.connect(host="127.0.0.1", user="root",passwd = "password")
    mycursor = mydb.cursor()
    return(mydb, mycursor)

class Home:
    def __init__(self, db, cursor):
        # All initialisations 
        self.window = Tk()
        self.window.geometry("500x400") # Set the size of the window
        self.window.title("RESULTS RVCE") # Set the title
        self.window.configure(background = 'black')
        self.mydb = db
        self.mycursor = cursor

        # First Half
        # Create Label
        source_label = Label(self.window, text="Enter USN", fg = "white", bg = "black")
        source_label.config(font=('helvetica', 15))
        source_label.place(relx = 0.38, rely = 0.1)
        # Create Text Entry Box
        self.USN_Box = Entry(self.window)
        self.USN_Box.place(relx = 0.365, rely = 0.2)
        # Create Button
        button1 = Button(text = "Get Results", bg = 'white', fg = 'black', font = ('helvetica', 12, 'bold'), command = self.getResult)
        button1.place(relx = 0.38, rely = 0.3)

        # Second Half
        departments = ["CV", "ME", "EE", "EC", "IM", "EI", "CH", "CS", "TE", "ISE", "BT", "ASE"]
        semesters = ["First", "Third", "Fifth", "Seventh"]

        # Text
        Dept_label = Label(self.window, text="Select Dept", fg = "white", bg = "black")
        Dept_label.config(font=('helvetica', 15))
        Dept_label.place(relx = 0.18, rely = 0.55)
        # Options Menu
        self.tkvar1 = StringVar(self.window)
        self.tkvar1.set("CV")
        self.deptOption = OptionMenu(self.window, self.tkvar1, *departments)
        self.deptOption.config(width = 10)
        self.deptOption.place(relx=0.38, rely=0.65, anchor='ne')

        # Text
        Sem_label = Label(self.window, text="Select Semester", fg = "white", bg = "black")
        Sem_label.config(font=('helvetica', 15))
        Sem_label.place(relx = 0.53, rely = 0.55)
        # Options Menu
        self.tkvar2 = StringVar(self.window)
        self.tkvar2.set("First")
        self.SemOption = OptionMenu(self.window, self.tkvar2, *semesters)
        self.SemOption.config(width = 10)
        self.SemOption.place(relx=0.78, rely=0.65, anchor='ne')

        # Create Button
        button2 = Button(text = "Get Batch Stats", bg = 'white', fg = 'black', font = ('helvetica', 12, 'bold'), command = self.getBatchStats)
        button2.place(relx = 0.35, rely = 0.8)
        self.window.mainloop()

    def getResult(self):
        # Get the result of an individual
        usn = self.USN_Box.get()
        dept = usn[5:7] 

        if((dept == "as") or (dept == "is")):
            dept += 'e'

        # Use the appropriate table
        useQ = "USE " + dept
        self.mycursor.execute(useQ)
        self.mydb.commit()

        for i in range(4):
            sems = ["first", "third", "fifth", "seventh"]
            # Query to search for the requested USN
            search = "SELECT * FROM " + dept + sems[i] + "sem" + " WHERE USN = '" + usn + "'"
            self.mycursor.execute(search)
            details = mycursor.fetchall()

            if(len(details) > 0):
                # If USN is present
                result = "Name :" + details[0][1] + '\nYour grades are\n'
                for j in range(3, len(details[0])-1):
                    result += details[0][j] + '\n'
                result += "SGPA = " + details[0][-1]
                messagebox.showinfo("RESULT OF" + usn.upper(), result)
                return

        # If USN is not present, display an error message
        messagebox.showerror("ERROR", "USN not present.\nEnter a valid USN")

    def getBatchStats(self):
        dept = self.tkvar1.get()
        sem = self.tkvar2.get()

        # Select the database
        database = "USE " + dept
        self.mycursor.execute(database)
        self.mydb.commit()

        semesters = ["First", "Third", "Fifth", "Seventh"]
        sem_int = 2*semesters.index(sem) + 1

        # Select columns of all the subjects
        sql = "SELECT "
        for i in range(1, 8):
            if(i != 7):
                sql = sql + dept + str(sem_int) + str(i) + ", "
            else:
                sql = sql + dept + str(sem_int) + str(i) + " "
        
        sql = sql + "FROM " + dept + sem + "sem"
        mycursor.execute(sql)

        # Get distribution of grades
        grades = mycursor.fetchall()
        grades2in = {'S': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'NSAR': 7, 'NSSR': 8, 'AB': 9, 'X': 10, 'I': 11, 'NE': 12}
        sub = [[0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0]]

        for i in range(len(grades)):
            for j in range(len(grades[i])):
                if(grades[i][j] != ""):
                    sub[j][grades2in[grades[i][j]]] += 1
        
        # Get the highest score
        getTopper = "SELECT MAX(SGPA) " + "FROM " + dept + sem + "sem"
        self.mycursor.execute(getTopper)
        topperScore = self.mycursor.fetchall()

        getDetails = "SELECT NAME, USN, SGPA " + "FROM " + dept + sem + "sem" + " WHERE SGPA = " + str(topperScore[0][0])
        self.mycursor.execute(getDetails)
        topperDetails = self.mycursor.fetchall()

        # Create a new window
        b = BatchStats(sem, sem_int, dept, topperDetails, sub)

class BatchStats:
    def __init__(self, sem, sem_int, branch, topperDetails, sub):
        # All initialisations
        self.window = Tk()
        self.window.geometry("1000x600") # Set the size of the window
        title = "Details of " + sem + "sem, " + branch.upper()
        self.window.title(title) # Set the title
        self.window.configure(background = 'black')
        self.displayStats(sem, sem_int, branch, topperDetails, sub)
        self.window.mainloop()

    
    def displayStats(self, sem, sem_int, branch, topperDetails, sub):

        count = 0
        subjects = ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'NSAR', 'NSSR', 'AB', 'X', 'I', 'NE']
        
        for i in range(len(sub)):
            if(sum(sub[i]) != 0):
                count += 1
        # Print the results- Grade distributions
        for i in range(count):
            head = "SUBJECT CODE: " + branch.upper() + str(sem_int) + str(i+1) + ""
            Dept_label = Label(self.window, text=head, fg = "white", bg = "black")
            Dept_label.config(font=('helvetica', 12))
            Dept_label.pack()

            result = ""
            for j in range(len(subjects)):
                result += subjects[j] + ": " + str(sub[i][j]) + "\t"
            result += "\n"
            Dept_label = Label(self.window, text=result, fg = "white", bg = "black")
            Dept_label.config(font=('helvetica', 12))
            Dept_label.pack()

        # Print the topper deatils
        topper = "The topper(s) is/are:\n"
        for i in range(len(topperDetails)):
            topper += topperDetails[i][0] + " (" + topperDetails[i][1] + ")" + ": " + str(topperDetails[i][2]) + "\n"
        Dept_label = Label(self.window, text=topper, fg = "white", bg = "black")
        Dept_label.config(font=('helvetica', 12))
        Dept_label.pack()


if __name__ == "__main__":
    mydb, mycursor = setup_DB()
    h = Home(mydb, mycursor)