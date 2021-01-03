import requests
from bs4 import BeautifulSoup as BS

php = 'http://acm.epoka.edu.al/Rankings.php?ofs='
nr = 1
sortMethod = '&SortMethod=2'
url = php + str(nr) + sortMethod


def checkLink():
    request = requests.get(url)
    if request.status_code == 200:
        print('Link Valid')
        page_source = request.text
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
    last_25_button = source.find_all("a", string=" Last 25 ")
    submit_data = str(last_25_button[0]['href'])
    last_25 = [int(s) for s in submit_data.split() if s.isdigit()][0]
    return last_25


def getStudentsData():
    keys = ["Nr", "Name", "Accepts Cnt", "Rejects Cnt", "Group", "Level"]
    student = {"Nr": 0, "Name": 0, "Accepts Cnt": 0, "Rejects Cnt": 0, "Group": 0, "Level": 0}

    for page in range(0, int(totalNrOfStudents / 25)):
        counter = 0
        student = {"Nr": 0, "Name": 0, "Accepts Cnt": 0, "Rejects Cnt": 0, "Group": 0, "Level": 0}

        url = php + str(nr + page * 25) + sortMethod
        print(url)
        request = requests.get(url)
        page_source = request.text
        page = BS(page_source, features="lxml")
        table_elements = page.findAll("td", {"class": "paging"})

        for i in range(0, len(table_elements)):
            data = table_elements[i].text.replace('\n', '').replace('\r', '').strip()
            student.update({keys[counter]: data})
            if counter == 5:
                students.append(student)
                students_file.write(str(student) + "\n")
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
        request = requests.get(url)
        page_source = request.text
        page = BS(page_source, features="lxml")
        table_elements = page.findAll("td", {"class": "paging"})

        for i in range(0, len(table_elements)):
            data = table_elements[i].text.replace('\n', '').replace('\r', '').strip()
            student.update({keys[counter]: data})
            if counter == 5:
                if int(student.get("Nr")) >= offset:
                    students.append(student)
                    students_file.write(str(student) + "\n")
                counter = 0
                student = {"Nr": 0, "Name": 0, "Accepts Cnt": 0, "Rejects Cnt": 0, "Group": 0, "Level": 0, }
            else:
                counter = counter + 1


if __name__ == '__main__':
    if checkLink():
        request = requests.get(url)
        page_source = request.text
        source = BS(page_source, features="lxml")

        students_file = open("All students data.txt", 'w+')
        filtered = open("Filtered data.txt", 'w+')

        students = []
        last_25 = get_last_student()
        totalNrOfStudents = last_25 + 24

        getStudentsData()

        print("Total nr of students on acm: ", totalNrOfStudents)
        print("Got ", len(students), "results")

        for s in students:
            if 'SWE20' == (s.get('Group')):
                # if '20' in (s.get('Group')):
                print(s)
                filtered.write(str(s) + "\n")

        students_file.close()
        filtered.close()

        input()
    else:
        print("Link not valid/servers down.")
