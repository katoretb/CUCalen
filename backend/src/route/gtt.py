from flask import request, jsonify
from copy import deepcopy
import sys

from route.func.gsi import gsi
from route.func.errmaker import errmaker


def main():
    try:
        freetime=(1,{'LECT':[],'LAB': []})

        req_data = request.get_json()
        subj_list = req_data["subj_list"]
        st_time = req_data["st_time"]
        ed_time = req_data["ed_time"]
        if req_data["freetime"] != "":
            freetime = req_data["freetime"]

        dataset = {}

        #=========================[ Load subject to dataset]=========================

        for i in range(len(subj_list)):
            x = subj_list[i].split("-")
            y, err = gsi(x[0], int(x[1]), int(x[2]))
            if err:
                return errmaker(500, f'Please contact owner')
            dataset[subj_list[i]] = y

        #=========================[ Define function & class]=========================

        def time_range(start, end):
            temp = []
            sl = start.split(":")
            el = end.split(":")
            for i in range(int(sl[0]), int(el[0])+1):
                for j in range(2):
                    temp.append(f'{i}-{j*30}')
                    temp.append(f'{i}-{j*30}')
            temp = temp[3:] if sl[1] != "00" else temp[1:]
            temp = temp[:-3] if el[1] == "00" else temp[:-1]
            return temp
        
        class timetable:
            def __init__(self, course_id, starter, start_time=8, end_time=16):
                #create default list of day
                self.days = []
                for i in range(7):
                    temp = []
                    for j in range(start_time, end_time+1):
                        for k in range(2):
                            temp.append(f'{j}-{k*30}')
                            temp.append(f'{j}-{k*30}')
                    self.days.append(temp)

                #set first course_id and section num
                self.cidlist = []
                self.add(course_id, starter)

            def add(self, course_id, section):
                #if it can add to timetable return true
                try:
                    #add course_id and section num
                    if course_id != "freetime":
                        self.cidlist.append((course_id, section[0]))

                    #remove occupied time(lect) from days list
                    for i in section[1]['LECT']:
                        tr = time_range(i['time'][0], i['time'][1])
                        for j in i['day']:
                            for k in tr:
                                self.days[j].remove(k)

                    #remove occupied time(lab) from days list
                    for i in section[1]['LAB']:
                        tr = time_range(i['time'][0], i['time'][1])
                        for j in i['day']:
                            for k in tr:
                                self.days[j].remove(k)
                    return True
                except:
                    return False
                
        #======================[ end Define function & class ]======================

        #Sort dataset from least section
        dataset = dict(sorted(dataset.items(), key=lambda item: len(item[1]['class'])))

        #Create starter subject
        possible = []
        first_subj = list(dataset.keys())[0]
        for first_subject_section in dataset[first_subj]['class'].items():
            x = timetable(first_subj, first_subject_section, start_time=st_time, end_time=ed_time)
            if x.add("freetime", freetime):
                possible.append(x)
            pass

        #Try filling all class
        for i in list(dataset.keys())[1:]:
            temp_possible = []
            for j in possible:
                for subject_section in dataset[i]['class'].items():#then loop every section
                    x = deepcopy(j)
                    if x.add(i, subject_section): #try method add to all section
                        temp_possible.append(x) #if can add to temp_possible
            possible = temp_possible #end section loop then possible = temp_possible

        #convert list of class to list of subject and section
        pos = []
        for i in possible:
            pos.append(i.cidlist)

        x = {
            "status_code": 200,
            "success": True,
            "message": "GTT success",
            "data": {
                "possible": pos,
                "dataset": dataset
            }
        }
        return jsonify(x)
    except Exception as error:
        print(error, file=sys.stderr)
        return errmaker(500, f'Please contact owner')