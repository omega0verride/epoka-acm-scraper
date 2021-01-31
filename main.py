import requests
from bs4 import BeautifulSoup as BS
import json
import time

php = 'http://acm.epoka.edu.al/Rankings.php?ofs='
nr = 1
sortMethod = '&SortMethod=2'
url = php + str(nr) + sortMethod


def sortByGroups(students):
    groups = [
        ['sprendi20', 'tkondakciu20', 'asula20', 'alndoci20', 'rkurti20', 'dlleshi20', 'eshkurti20', 'amilo20',
         'llera20', 'ssaraci20', 'xlushaj20', 'sdosku20', 'knito20'],
        ['ehoxha20', 'fspata20', 'ghaveri20', 'ebici20', 'edaci20', 'acenga20', 'etoska20', 'qsinaj20', 'ameta20',
         'irrucaj20', 'nkolnikaj20', 'klkasa20', 'shbevapi20'],
        ['abreshanaj20', 'adikolli20', 'amustafa20', 'euzun', 'tkarabina20', 'dsheshori20', 'dhyseni20', 'ejakupi20',
         'rcanaj20', 'eroci20', 'ecupi20', 'flluri20', 'mjovani20'],
        ['akamberi20', 'kxhina20', 'ggjoka20', 'hkryemadhi20', 'ibreti20', 'jhamzallari20', 'kebushi20', 'rspahija20',
         'dqorri20', 'kmerdhoci20', 'raga20', 'elicaj20']]
    groups_data = []
    for i in range(0, len(groups)):
        groups_data.append([])
    group_nr = 0
    for group in groups:
        group_nr += 1
        for gr in group:
            for cnt in range(0, len(students)):
                if gr.replace('0', 'o') == students[cnt].get("Name"):
                    students[cnt]["SWE_GR"] = group_nr
                    groups_data[students[cnt].get("SWE_GR") - 1].append(students[cnt])
                    break
    return groups_data


def checkLink():
    request = requests.get(url)
    if request.status_code == 200:
        print('Link Valid')
        page_source = request.text
        return 1
    else:
        return 0


def get_last_student():
    last_25_button = source.find_all("a", string=" Last 25 ")
    submit_data = str(last_25_button[0]['href'])
    last_25 = [int(s) for s in submit_data.split() if s.isdigit()][0]
    return last_25


def saveToDatabase(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path)
    filename = time.strftime("%Y-%m-%d-%H")
    json.dump(students, open(os.path.join(path, filename+'.json'), 'w+'))

def getStudentsData():
    students_data = []
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
                students_data.append(student)
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
                    students_data.append(student)
                counter = 0
                student = {"Nr": 0, "Name": 0, "Accepts Cnt": 0, "Rejects Cnt": 0, "Group": 0, "Level": 0, }
            else:
                counter = counter + 1
    return students_data


def create_unsorted_table(data):
    table = ""
    table += '{:3} {:15} {:3} \t {:11}    {:17} {:6} {:15}'.format("Nr", "Name", "SWE_GR", "Accepts Cnt", "Rejects Cnt",
                                                                   "Group", "Level") + "\n"
    table += "-" * 100 + "\n"

    for gr in data:
        total_a = 0
        total_r = 0
        for s in gr:
            table += '{:3} {:15} {:3} \t {:11}    {:17} {:6} {:15}'.format(s.get("Nr"), s.get("Name"), s.get("SWE_GR"),
                                                                           s.get("Accepts Cnt"), s.get("Rejects Cnt"),
                                                                           s.get("Group"), s.get("Level")) + "\n"
            total_a += int(s.get("Accepts Cnt"))
            total_r += int(s.get("Rejects Cnt"))

        table += '{:<28} {:<14} {:<4}'.format("Total:", total_a, total_r) + "\n"
        table += "-" * 100 + "\n"
    return table


def create_sorted_table(data):
    groups_sorted = data
    for g in range(0, len(groups_sorted)):
        arr = groups_sorted[g]
        for i in range(0, len(arr)):
            for j in range(i, len(arr)):
                a = int(arr[i].get("Accepts Cnt"))
                b = int(arr[j].get("Accepts Cnt"))
                if a < b:
                    arr[j], arr[i] = arr[i], arr[j]
        groups_sorted[g] = arr
    return create_unsorted_table(groups_sorted)


def save_as_file(name, tmp_students):
    ans = input("Save as file? [Y/N]").lower()
    if ans == "y" or ans == "yes" or ans == str(1):
        filtered = open("%s.txt" % name, 'w+')
        print(type(tmp_students))
        try:
            filtered.write(tmp_students)
        except:
            for s in tmp_students:
                filtered.write(str(s) + "\n")
        filtered.close()
    elif ans == "n" or ans == "no" or ans == str(0):
        pass
    else:
        print("Please enter yes/no, 1/0, y/n lowercase or uppercase!")
        save_as_file(name, tmp_students)


def select_option(students):
    print("Select an option: ")
    print("[0] Exit")
    print("[1] Print data for all ACM competitors.")
    print("[2] Print data for year 2020 ACM competitors.")
    print("[3] Print data for SWE students.")
    print("[4] Print data for SWE students, by groups.")
    print("[5] Print data for SWE students, by groups, sorted by Accepted Cnt.")
    try:
        val = int(input())
    except:
        print("Please enter the number of one of the given options!")
        select_option(students)
    if val == 0:
        exit()
    elif val == 1:
        for s in students:
            print(s)
        save_as_file("All students data", students)
        print("-" * 100)
    elif val == 2:
        tmp_students = []
        for s in students:
            if '20' in (s.get('Group')):
                print(s)
                tmp_students.append(s)
        save_as_file("2020 ACM Competitors", tmp_students)
        print("-" * 100)
    elif val == 3:
        tmp_students = []
        for s in students:
            if 'SWE20' in (s.get('Group')):
                print(s)
                tmp_students.append(s)
        save_as_file("SWE20 ACM Competitors", tmp_students)
        print("-" * 100)
    elif val == 4:
        tmp_students = []
        for s in students:
            if 'SWE20' in (s.get('Group')):
                tmp_students.append(s)
        groups_data = sortByGroups(tmp_students)
        table = create_unsorted_table(groups_data)
        print(table)
        save_as_file("SWE20 ACM By Groups", table)
        print("-" * 100)
    elif val == 5:
        tmp_students = []
        for s in students:
            if 'SWE20' in (s.get('Group')):
                tmp_students.append(s)
        groups_data = sortByGroups(tmp_students)
        table = create_sorted_table(groups_data)
        print(table)
        save_as_file("SWE20 ACM By Groups - Sorted", table)
        print("-" * 100)
    else:
        print("Please enter the number of one of the given options!")
        select_option(students)


if __name__ == '__main__':
    if checkLink():
        request = requests.get(url)
        page_source = request.text
        source = BS(page_source, features="lxml")

        last_25 = get_last_student()
        totalNrOfStudents = last_25 + 24

        students = getStudentsData()
        print("Total nr of students on acm: ", totalNrOfStudents)
        print("Got ", len(students), "results")
        print('Saving data to "Database" folder to use it later for analysis...')
        saveToDatabase("Database")

        while 1:
            select_option(students)
    else:
        print("Link not valid/servers down.")
