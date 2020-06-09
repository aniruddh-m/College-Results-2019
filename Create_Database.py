import mysql.connector

# Connect to a database
mydb = mysql.connector.connect(host="localhost", user="root",passwd = "password")
mycursor = mydb.cursor()

departments = ["CV", "ME", "EE", "EC", "IM", "EI", "CH", "CS", "TE", "ISE", "BT", "ASE"]
semesters = ["First", "Third", "Fifth", "Seventh"]
for i in range(len(departments)):
    query = "CREATE DATABASE " + departments[i]
    mycursor.execute(query)

    query2 = "USE " + departments[i]
    mycursor.execute(query2)
    mydb.commit()

    for j in range(len(semesters)):
        table_query = "CREATE TABLE " + departments[i] + semesters[j] + "sem " + "(Sl_No INT AUTO_INCREMENT , Name VARCHAR(50), USN VARCHAR(12) PRIMARY KEY, "
        
        for k in range(1, 8):
            table_query = table_query + departments[i] + str(2*j+1) + str(k) + " VARCHAR(5), "

        table_query = table_query + "SGPA VARCHAR(4))"
        mycursor.execute(table_query)

print("Done")