import os
import bs4
import urllib.request as request
path = "C:\\Users\Wise\Documents\\unilus\schools\\"
schools_path =path+ "schools.html"
program_path = path+"program_ex.html"

schools_url="https://www.unilus.ac.zm/Schools.aspx"

keys = []
courses={}
def remove_spaces(string):

    while str(string).startswith(" "):
        string=string[1:]

    while str(string).endswith(" "):
        string = string[:-1]

    return string




# with open(program_path,"r",encoding="utf-8") as file:

#                 print(course_name,code)

def traverse_program(link):

    if not link.__contains__(".aspx"):
        return
    soup = bs4.BeautifulSoup(request.urlopen(link).read(), "html.parser")
    tables = soup.find_all("table")

    for table in tables:
        if str(table).lower().__contains__("first semester"):
            for li in table.find_all("li"):
                text = str(li.get_text())
                code = text.split(" ",-1)[0]
                course_name ="         "+ text.replace(code,"")
                course_name = remove_spaces(course_name)
                code=remove_spaces(code)

                if not keys.__contains__(code):
                    keys.append(code)
                courses[code]=course_name


def traverse_school(link):
    soup =bs4.BeautifulSoup(request.urlopen(link).read(),"html.parser")
    a_tags = soup.find_all("a")
    for tag in a_tags:
        if str(tag).lower().__contains__("bachelor of") and not str(tag).lower().__contains__("whispers"):
            href = tag.get("href")
            traverse_program("https://www.unilus.ac.zm/"+href)


def begin():
    import requests

    file = bs4.BeautifulSoup(requests.get(schools_url).text,"html.parser")
    anchors = file.find_all("a")
    for anchor in anchors:
        if str(anchor).lower().__contains__("school of"):
            link = "https://www.unilus.ac.zm/" +anchor.get("href")
            print(link)

            traverse_school(link)

    with open("./allCourses","w")as cfile:
        cfile.write(str({"courses":courses,"keys":keys}))

    return "success"

