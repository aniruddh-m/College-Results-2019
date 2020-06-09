from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import mysql.connector
import time

def setup_DB(dept):
    # Setup the database
    mydb = mysql.connector.connect(host="127.0.0.1", user="root",passwd = "password", database = dept)
    mycursor = mydb.cursor()
    return(mydb, mycursor)

def gotoResultSheet(driver, USN):
    driver.find_element_by_xpath('//*[@id="envelope"]/form/input[1]').clear()
    driver.find_element_by_xpath('//*[@id="envelope"]/form/input[1]').send_keys(USN)
    question = driver.find_element_by_xpath('//*[@id="envelope"]/form/label[2]').text
    driver.find_element_by_xpath('//*[@id="envelope"]/form/input[2]').clear()
    driver.find_element_by_xpath('//*[@id="envelope"]/form/input[2]').send_keys(int(question[8]) + int(question[12]))
    driver.find_element_by_xpath('//*[@id="submit"]').click()
    time.sleep(0.5)

    while((driver.current_url) != "http://results.rvce.edu.in/viewresult2.php"):
        driver.get("http://results.rvce.edu.in/")
        driver.find_element_by_xpath('//*[@id="envelope"]/form/input[1]').clear()
        driver.find_element_by_xpath('//*[@id="envelope"]/form/input[1]').send_keys(USN)
        question = driver.find_element_by_xpath('//*[@id="envelope"]/form/label[2]').text
        driver.find_element_by_xpath('//*[@id="envelope"]/form/input[2]').clear()
        driver.find_element_by_xpath('//*[@id="envelope"]/form/input[2]').send_keys(int(question[8]) + int(question[12]))
        driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(0.5)

def getGrades(driver, USN, mydb, mycursor, dept, file_res):
    try:
        name = driver.find_element_by_xpath('//*[@id="no-more-tables"]/table[1]/tbody/tr/td[3]').text
        sem = driver.find_element_by_xpath('//*[@id="no-more-tables"]/table[1]/tbody/tr/td[4]').text
        sgpa = driver.find_element_by_xpath('//*[@id="no-more-tables"]/table[1]/tbody/tr/td[5]/b').text

    except:
        file_res.write(USN + " not found." + '\n')
        print(USN + " not found.")  
        driver.back()
        return

    sub1 = ""
    sub2 = ""
    sub3 = ""
    sub4 = ""
    sub5 = ""
    sub6 = ""
    sub7 = ""

    try:
        sub1 = driver.find_element_by_xpath('//*[@id="no-more-tables"]/table[2]/tbody/tr[1]/td[3]').text
        sub2 = driver.find_element_by_xpath('//*[@id="no-more-tables"]/table[2]/tbody/tr[2]/td[3]').text
        sub3 = driver.find_element_by_xpath('//*[@id="no-more-tables"]/table[2]/tbody/tr[3]/td[3]').text
        sub4 = driver.find_element_by_xpath('//*[@id="no-more-tables"]/table[2]/tbody/tr[4]/td[3]').text
        sub5 = driver.find_element_by_xpath('//*[@id="no-more-tables"]/table[2]/tbody/tr[5]/td[3]').text
        sub6 = driver.find_element_by_xpath('//*[@id="no-more-tables"]/table[2]/tbody/tr[6]/td[3]').text
        sub7 = driver.find_element_by_xpath('//*[@id="no-more-tables"]/table[2]/tbody/tr[7]/td[3]').text
        writeToDB(name, USN, int(sem), sub1, sub2, sub3, sub4, sub5, sub6, sub7, sgpa, dept, mydb, mycursor)
    except:
        pass
    driver.back()

def writeToDB(name, USN, sem, sub1, sub2, sub3, sub4, sub5, sub6, sub7, sgpa, dept, mydb, mycursor):
    semesters = ["First", "Third", "Fifth", "Seventh"]

    sql = """INSERT INTO """ + dept + semesters[(sem-1)//2] + """sem VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    print(sql)
    val = (name, USN, sub1, sub2, sub3, sub4, sub5, sub6, sub7, sgpa)
    mycursor.execute(sql, val)
    mydb.commit()

if __name__ == "__main__":

    file_res = open(r'D:\Aniruddh\Nerdy Stuff\Python\Selenium\results.txt','w')

    # Setup Web driver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path = r"D:\Aniruddh\Nerdy Stuff\Selenium\Drivers\chromedriver.exe", chrome_options = chrome_options)
    driver.get("http://results.rvce.edu.in/")

    departments = ["CV", "ME", "EE", "EC", "IM", "EI", "CH", "CS", "TE", "ISE", "BT", "ASE"]
    departments_USN = ["CV", "ME", "EE", "EC", "IM", "EI", "CH", "CS", "TE", "IS", "BT", "AS"]

    for year in range(16, 19):
        for dept in range(len(departments)):
            mydb, mycursor = setup_DB(departments[dept])
            for i in range(1, 10):
                USN = "1RV" + str(year) + departments_USN[dept] + "00" + str(i)
                gotoResultSheet(driver, USN)
                getGrades(driver, USN, mydb, mycursor, departments[dept], file_res)

            for i in range(10, 100):
                USN = "1RV" + str(year) + departments_USN[dept] + "0" + str(i)
                gotoResultSheet(driver, USN)
                getGrades(driver, USN, mydb, mycursor, departments[dept], file_res)

            for i in range(100, 200):
                USN = "1RV" + str(year) + departments_USN[dept] + str(i)
                gotoResultSheet(driver, USN)
                getGrades(driver, USN, mydb, mycursor, departments[dept], file_res)

    driver.close()
    file_res.close()
    print("Done")