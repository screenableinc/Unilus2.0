import bs4

# with open("C:\\Users\Screenable\PycharmProjects\\unilus\\undergrad_all.html", "r") as html:
#     g_soup = bs4.BeautifulSoup(html,"html.parser")
#     g_soup=g_soup.find_all("a")

def details(string,link_text,soup,keys,courses_dict):

    response = {"time":"","program":"","room":"","lecturer":"","details":"","type":"","code":""}
    string = string.replace(str(link_text).lower().replace("\n",""),"")
    if str(link_text).lower().__contains__("tutorial"):
        response["type"]="Tutorial"
    else:
        response["type"]="Class"
    code = ""
    # keys is a list of program codes

    for key in keys:
        if str(link_text).lower().__contains__(str(key).lower()):
            code=key
            response["code"]=code
            break

    lect_list=[]
    for lect in soup:

        if str(lect).lower().__contains__("mr") or str(lect).lower().__contains__("ms") or str(lect).lower().__contains__("mrs") or str(lect).lower().__contains__("dr"):
            if lect.get_text().__len__()<50:
                lect_list.append(str(lect.get_text()).split(":",-1)[1])
    lect_list.append("TBA")

    for i in lect_list:
        if string.__contains__(str(i).lower()):
            response["lecturer"]=i
            break


    # print(string)
    # parse to get program
    def last_resort(link_text):
        finalstr=""
        link_text = str(link_text)
        if link_text.__contains__("#"):
            found_hashtag = False
            for i in link_text:

                if i =="#":
                    found_hashtag=True
                if found_hashtag==True:
                    try:
                        int(i)
                    except:

                        finalstr = finalstr+i
            finalstr = finalstr.replace("#","").replace("\n","").replace("  ","")
        else:
            finalstr=link_text.replace("\n","").replace("  ","")
        response["program"]=finalstr
    response["details"]=string.replace("\n","")

    # for room
    string = str(string).lower()
    prefix=""
    if string.__contains__("flamingo"):
        prefix="(Flamingo Site)"
    elif string.__contains__("leopard"):
        prefix = "(Leopards Hill)"
    elif string.__contains__("pioneer") or string.__contains__("knowledge") or string.__contains__("main"):
        prefix = "(Main Campus)"
    else:
        prefix = "(Main Campus)"
    if string.__contains__("room"):
        new = string.split("room",-1)
        found_first_int=False
        roomnumber=""
        for i in new[1]:
            try:
                int(i)
                roomnumber = roomnumber+i
                found_first_int=True

            except:
                if found_first_int==True:
                    break

                continue

        response["room"]=roomnumber+prefix

        try:
            response["program"]=courses_dict[code]
        except KeyError:
            last_resort(link_text)
    elif string.__contains__("lhnexh"):
        response["room"] = "New Hall(Leopards Hill)"
        try:
            response["program"]=courses_dict[code]
        except KeyError:
            last_resort(link_text)

    return response

# print(details("HRM100BTT#125 Management Theory and Practice Group B Tutorial#125TUT003 Mr HandembaRM05#125 ROOM5 @Pioneer Campus Lecture Room 5 Ground Floor Knowledge Fields Capacity #125".lower(),g_soup))
