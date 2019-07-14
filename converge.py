import json
j={}
with open("./programs_scheds.json", "r")as fc:
    myjson = eval(fc.read())
    myjson["undergraduate"]["distance"]=myjson["undergraduate"]["distance"]
    j=myjson

with open("./programs_scheds.json", "w")as fc:
    json.dump(j, fc)


