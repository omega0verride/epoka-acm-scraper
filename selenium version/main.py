from selenium import webdriver
import time
import math
import requests

php = 'http://acm.epoka.edu.al/Rankings.php?ofs='
nr = 1
sortMethod = '&SortMethod=2'
url = php + str(nr) + sortMethod


def checkLink():
    request = requests.get(url)
    if request.status_code == 200:
        print('Link Valid')
        return 1
    else:
        return 0


def setupSelenium(gui):
    DRIVER_PATH = 'chromedriver_win32\chromedriver.exe'
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    print("Emulating Selenium...")
    if gui:
        browser = webdriver.Chrome(executable_path=DRIVER_PATH)
    else:
        browser = webdriver.Chrome(options=op, executable_path=DRIVER_PATH)
    page = browser.get(url)
    return browser


def get_last_student():
    last_25_button = browser.find_element_by_xpath("//a[contains(text(),'Last 25')]")
    submit_data = str(last_25_button.get_attribute("href"))
    last_25 = [int(s) for s in submit_data.split() if s.isdigit()][0]
    return last_25

def getStudentsData():

    keys = ["Nr", "Name", "Accepts Cnt", "Rejects Cnt", "Group", "Level"]
    student = {
        "Nr": 0,
        "Name": 0,
        "Accepts Cnt": 0,
        "Rejects Cnt": 0,
        "Group": 0,
        "Level": 0,
    }

    for page in range(0, int(totalNrOfStudents / 25)):
        counter = 0
        student = {"Nr": 0, "Name": 0, "Accepts Cnt": 0, "Rejects Cnt": 0, "Group": 0, "Level": 0}

        url = php + str(nr + page * 25) + sortMethod
        print(url)
        page = browser.get(url)

        table_elements = browser.find_elements_by_class_name("paging")
        for i in range(0, len(table_elements)):
            student.update({keys[counter]: table_elements[i].text})
            if counter == 5:
                students.append(student)
                counter = 0
                student = {"Nr": 0, "Name": 0, "Accepts Cnt": 0, "Rejects Cnt": 0, "Group": 0, "Level": 0}
            else:
                counter = counter + 1

    if int(totalNrOfStudents % 25) != 0:
        offset = nr + int(totalNrOfStudents / 25) * 25

        counter = 0
        student = {"Nr": 0, "Name": 0, "Accepts Cnt": 0, "Rejects Cnt": 0, "Group": 0, "Level": 0, }
        url = php + str(last_25) + sortMethod
        print(url)
        page = browser.get(url)

        table_elements = browser.find_elements_by_class_name("paging")
        for i in range(0, len(table_elements)):
            student.update({keys[counter]: table_elements[i].text})
            if counter == 5:
                if int(student.get("Nr")) >= offset:
                    students.append(student)
                counter = 0
                student = {"Nr": 0, "Name": 0, "Accepts Cnt": 0, "Rejects Cnt": 0, "Group": 0, "Level": 0, }
            else:
                counter = counter + 1

if __name__ == '__main__':
    if checkLink():
        browsers = setupSelenium(gui=0)
        browser = browsers

        students = []
        last_25 = get_last_student()
        totalNrOfStudents = last_25 + 24
        print("Total nr of students on acm: ", totalNrOfStudents)
        getStudentsData()

        print(students)
        print(len(students))
        browser.quit()

        for s in students:
            if 'SWE20' == (s.get('Group')):
            # if '20' in (s.get('Group')):
                print(s)
    else:
        print("Link not valid/servers down.")
