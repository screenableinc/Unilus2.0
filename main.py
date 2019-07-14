from bs4 import BeautifulSoup
import os
import requests
import urllib
import get_details
import json
print("starting")


# distance info
distance_time_t = "https://sms.unilus.ac.zm/ResidentialTimeTable/students/time.htm"
distance_tables_home = "https://sms.unilus.ac.zm/ResidentialTimeTable/students/"

ft_undergradTablesPage="https://sms.unilus.ac.zm/UndergradFullTimeTable/time.htm"
pt_undergradTablesPage="https://sms.unilus.ac.zm/UndergradPartTimeTable/time.htm"
postgradTablesPage="https://sms.unilus.ac.zm/PostGradPartTime/postgraduateparttimestudentsprograms.htm"

# remember to switch depending on task

rooms_url="https://sms.unilus.ac.zm/ResidentialTimeTable/Rooms/time.htm"

ft_tables_home = "https://sms.unilus.ac.zm/UndergradFullTimeTable/"
pt_tables_home="https://sms.unilus.ac.zm/UndergradPartTimeTable/"
pg_tables_home = "https://sms.unilus.ac.zm/PostGradPartTime/"
main_schema = {"postgraduate":{"parttime":{}},"undergraduate":{"fulltime":{},"parttime":{},"distance":{}}}
dotw_schema = {"Sunday":{},"Monday":{},"Tuesday":{},"Wednesday":{},"Thursday":{},"Friday":{},"Saturday":{}}
days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
times = ["08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:30"
         ,"18:30","19:30","20:30"]

undergrad_lect="https://sms.unilus.ac.zm/UndergraduateLecturers/time.htm"
# used to get list of lecturers
g_soup=BeautifulSoup(str(requests.get(undergrad_lect).text),"html5lib").find_all("a")
rooms={"Sunday":{},"Monday":{},"Tuesday":{},"Wednesday":{},"Thursday":{},"Friday":{},"Saturday":{}}
for i in days:
    for j in times:
        rooms[i][j]=[]

with open("./allCourses","r")as allcourses:
    courses=eval(allcourses.read())
    keys=courses["keys"]
    all_courses = courses["courses"]


class Rooms():
    def __init__(self):
        self.fulltime()



    def fulltime(self):
        strhtml = requests.get(rooms_url).text
        soup = BeautifulSoup(str(strhtml), "html5lib")
        # print(soup)
        table = soup.find_all("table")[1]

        anchors = table.find_all("a")
        for anchor in anchors:
            title = str(anchor.get("title"))
            if not title.lower().__contains__("fla"):
                campus = ""
                if title.lower().__contains__("lh"):
                    campus="Leopards Hill"
                    try:
                        title=title.lower().split("#",-1)[0].replace("lh","")
                        title=int(title)
                        title=str(title)
                    except:
                        title="New Hall"
                elif title.lower().__contains__("rm"):
                    campus="Main Campus"
                    title = title.lower().split("#", -1)[0].replace("rm","")
                    title = int(title)
                    title = str(title)


                if str(anchor.get_text()).lower().__contains__("capacity"):

                    link = "https://sms.unilus.ac.zm/undergraduateRooms/" + anchor.get("href")
                    self.parseTable(link, title, campus)

    def parseTable(self,link,title,campus):
        print(link)
        column_span = [0, 0, 0, 0, 0, 0, 0]
        soup = BeautifulSoup(str(requests.get(link).text), "html5lib")
        # get all table rows
        table = soup.find_all("table")[0]
        rows = table.find_all("tr")
        # remove the first one whic contians the course name
        rows.remove(rows[0])
        # remove time slot rows
        rows.remove(rows[0])
        row_count = 0
        iteration_count = 7
        # the first tabel tag

        for i in rows:

            columns = i.find_all("td")

            # save time slot.....ostgrad doest use row span like full time
            # remove the first column...ths has time slot
            tim_column = columns[0]
            columns.remove(columns[0])
            column_idx = 0
            for j in range(7):

                if column_span[column_idx] > 0:
                    columns.insert(column_idx, BeautifulSoup("<td></td>", "html.parser"))

                if not str(columns[j]) == "<td></td>":

                    text = columns[j].get_text()
                    rowspan = columns[j].get("rowspan")
                    day = days[column_idx]

                    if str(text).__len__() > 50 or str(text).lower().__contains__("reserved") or str(text).lower().__contains__("other"):

                        # time = str(tim_column.get_text()).replace("\n", "").replace(" ", "")


                        if rowspan == None:
                            rowspan = 1

                        column_span[column_idx] = int(rowspan)

                    elif str(text).__len__() < 50:
                        start = int(times[row_count].split(":")[0])
                        minute = times[row_count].split(":")[1]

                        rooms[days[column_idx]][times[row_count]].append(title+"("+campus+")")
                        print(title, days[column_idx], times[row_count])

                column_idx = column_idx + 1



                # print(column_span)
            for j in range(column_span.__len__()):
                column_span[j] = column_span[j] - 1
            row_count = row_count + 1



class TimeTables():
    found=0
    def __init__(self):
        self.fulltime()
        self.parttime()
        self.postgrad()
        # self.distance()

        with open("./free_classes.json","w")as fc:
            json.dump(rooms,fc)

        with open("./programs_scheds.json","w")as fc:
            json.dump(main_schema,fc)

        # import converge

    def distance(self):

        strhtml = requests.get(distance_time_t).text
        soup = BeautifulSoup(str(strhtml), "html5lib")
        # print(soup)
        table = soup.find_all("table")[1]

        anchors = table.find_all("a")
        for anchor in anchors:
            title = anchor.get_text()
            if str(title).lower().__contains__("bachelor") or str(title).lower().__contains__("acca"):
                link = distance_tables_home + anchor.get("href")
                self.parseTable(link, str(title).split(":")[0], "distance", "undergraduate")

    def postgrad(self):
        strhtml = requests.get(postgradTablesPage).text
        soup = BeautifulSoup(str(strhtml), "html5lib")
        # print(soup)
        table = soup.find_all("table")[1]

        anchors = table.find_all("a")
        for anchor in anchors:
            title = anchor.get_text()
            if str(title).lower().__contains__("master"):
                link = pg_tables_home + anchor.get("href")
                self.parseTable(link, str(title).split(":")[0], "parttime","postgraduate")

    def parttime(self):
        strhtml = requests.get(pt_undergradTablesPage).text
        soup = BeautifulSoup(str(strhtml), "html5lib")
        # print(soup)
        table = soup.find_all("table")[1]

        anchors = table.find_all("a")
        for anchor in anchors:
            title = anchor.get_text()
            if str(title).lower().__contains__("bachelor") or str(title).lower().__contains__("acca"):
                link = pt_tables_home + anchor.get("href")
                self.parseTable(link, str(title).split(":")[0].replace("- PT",""), "parttime","undergraduate")



    def fulltime(self):

        strhtml = requests.get(ft_undergradTablesPage).text
        soup = BeautifulSoup(str(strhtml),"html5lib")
        # print(soup)
        table = soup.find_all("table")[1]

        anchors = table.find_all("a")
        for anchor in anchors:
            title = anchor.get_text()
            if str(title).lower().__contains__("bachelor") or str(title).lower().__contains__("acca"):
                link = ft_tables_home + anchor.get("href")
                self.parseTable(link,str(title).split(":")[0],"fulltime","undergraduate")
    def parseTable(self,link,title,mode,level):

        column_span = [0, 0, 0, 0, 0, 0, 0]
        print(link)
        soup = BeautifulSoup(str(requests.get(link).text), "html5lib")
        table = soup.find("table")
        rows = table.find_all("tr")


        main_schema[level][mode][title] = {"Sunday": [], "Monday": [], "Tuesday": [], "Wednesday": [],
                                                "Thursday": [], "Friday": [], "Saturday": []}

        # remove the first one whic contians the course name
        rows.remove(rows[0])
        # remove time slot rows
        rows.remove(rows[0])
        row_count = 0
        iteration_count = 7
        # the first tabel tag


        for i in rows:

            columns = i.find_all("td")


            # remove the first column...ths has time slot
            # if level=="postgraduate":
            #     columns.remove(columns[columns.__len__()-1])

            col1=columns[0]
            columns.remove(columns[0])
            column_idx = 0

            for j in range(iteration_count):

                if column_span[column_idx] > 0:
                    columns.insert(column_idx, BeautifulSoup("<td></td>", "html.parser"))
                # print(print(col1.get_text()))
                # try:
                rowspan = columns[j].get("rowspan"); fortime = columns[j].get("rowspan")
                # except:
                #     if str(title).__contains__("BACT32"):
                #         return
                text = str(columns[j].get_text())
                day = days[column_idx]
                day_programs = main_schema[level][mode][title][day]

                if text.__len__() > 50:
                    start = int(times[row_count].split(":")[0])
                    minute = times[row_count].split(":")[1]
                    if rowspan == None:
                        starth=int(col1.get_text().split("-",-1)[0].split(":",-1)[0])
                        endh = int(col1.get_text().split("-", -1)[1].split(":",-1)[0])
                        print(starth , endh)
                        # redundant though
                        fortime="2"
                        rowspan = "1"

                    ed_hr = start + int(fortime)
                    time = str(start) + ":" + minute + "-" + str(ed_hr) + ":" + minute
                    link_text = columns[j].find("b")

                    if link_text == None:
                        break
                    else:
                        link_text = link_text.get_text()
                    json_of_details = get_details.details(str(columns[j].get_text()).replace("\n", "").lower(),
                                                          link_text, g_soup, keys, all_courses)

                    json_of_details["time"] = time.replace("8:00-", "08:00-")
                    room = json_of_details["room"]
                    # get start and ends time
                    split_time = str(json_of_details["time"]).split(":", -1)
                    start_time = split_time[0]
                    end_time = split_time[1].split("-", -1)[1]
                    for t in range(int(end_time) - int(start_time)):
                        curr_time = int(start_time) + t
                        min2appen = ":00"
                        if curr_time >= 17:
                            min2appen = ":30"
                        if curr_time < 10:
                            curr_time = "0" + str(curr_time)

                        curr_time = str(curr_time) + min2appen
                        print(room)

                        if rooms[day][curr_time].__contains__(room):
                            rooms[day][curr_time].remove(room)
                            print("removed", room, day, time)
                            self.found=self.found+1

                    day_programs.append(json_of_details)
                    column_span[column_idx] = int(rowspan)
                column_idx = column_idx + 1


            for l in range(iteration_count):
                column_span[l] = column_span[l] - 1

                # print(column_span)
            row_count = row_count + 1




Rooms()
TimeTables()