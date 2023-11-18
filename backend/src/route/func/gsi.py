import requests
import html_to_json
import sys

def format_class(rawtr):
    secdic = {}
    d = {
        "MO": 1,
        "TU": 2,
        "WE": 3,
        "TH": 4,
        "FR": 5
    }
    secn = 0
    for i in range(len(rawtr)):
        if 10 > len(rawtr[i]['td']) > 7:
            temp = {
                "day": [d[k] for k in rawtr[i]['td'][2]['nobr'][0]['font'][0]['_value'].replace("\r\n\t\t\t\t\t\t\t   \r\n\t\t\t\t\t\t\t\t\r\n\t\t\t                     ", " ").split()],
                "time": [f'{x}:00' for x in rawtr[i]['td'][3]['nobr'][0]['font'][0]['_value'].split("-")],
                "building": rawtr[i]['td'][4]['nobr'][0]['font'][0]['_value'],
                "Room": rawtr[i]['td'][5]['nobr'][0]['font'][0]['_value']
            }
            secdic[secn][rawtr[i]['td'][1]['nobr'][0]['font'][0]['_value']].append(temp)
        elif len(rawtr[i]['td']) > 9:
            if secn != int(rawtr[i]['td'][1]['nobr'][0]['font'][0]['_value']):
                secn += 1
                secdic[secn] = {
                    "LECT": [],
                    "LAB": []
                }
            temp = {
                "day": [d[k] for k in rawtr[i]['td'][3]['nobr'][0]['font'][0]['_value'].replace("\r\n\t\t\t\t\t\t\t   \r\n\t\t\t\t\t\t\t\t\r\n\t\t\t                     ", " ").split()],
                "time": [f'{x}:00' for x in rawtr[i]['td'][4]['nobr'][0]['font'][0]['_value'].split("-")],
                "building": rawtr[i]['td'][5]['nobr'][0]['font'][0]['_value'],
                "Room": rawtr[i]['td'][6]['nobr'][0]['font'][0]['_value']
            }
            secdic[secn][rawtr[i]['td'][2]['nobr'][0]['font'][0]['_value']].append(temp)
        else:
            if secn != int(rawtr[i]['td'][1]['nobr'][0]['font'][0]['_value']):
                secn += 1
                secdic[secn] = {
                    "LECT": [],
                    "LAB": []
                }
            temp = {
                "day": [d[k] for k in rawtr[i]['td'][1]['nobr'][0]['font'][0]['td'][1]['nobr'][0]['font'][0]['_value'].replace("\r\n\t\t\t\t\t\t\t   \r\n\t\t\t\t\t\t\t\t\r\n\t\t\t                     ", " ").split()],
                "time": [f'{x}:00' for x in rawtr[i]['td'][1]['nobr'][0]['font'][0]['td'][2]['nobr'][0]['font'][0]['_value'].split("-")],
                "building": rawtr[i]['td'][1]['nobr'][0]['font'][0]['td'][3]['nobr'][0]['font'][0]['_value'],
                "Room": rawtr[i]['td'][1]['nobr'][0]['font'][0]['td'][4]['nobr'][0]['font'][0]['_value']
            }
            secdic[secn][rawtr[i]['td'][1]['nobr'][0]['font'][0]['td'][0]['nobr'][0]['font'][0]['_value']].append(temp)
    return secdic

def gsi(c: str, y: int, se: int, sp='S'): #<======================================================================<<<<
    apiparm = {
        "courseno": c,
        "year": y,
        'semester': se,
        'studyProgram': sp
    }

    mainurl = 'https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.'

    params1 = {
                'examdateCombo': 'I2022128%2F11%2F1479',
                'studyProgram': apiparm['studyProgram'],
                'semester': int(apiparm['semester']),
                'acadyearEfd': apiparm['year'],
                'submit.x': 39,
                'submit.y': 13,
                'courseno': int(apiparm['courseno']),
                'coursename' : '',
                'examdate': '',
                'examstartshow': '',
                'examendshow': '',
                'faculty': int(apiparm['courseno'][:2]),
                'coursetype': '',
                'genedcode': '',
                'cursemester': int(apiparm['semester']),
                'curacadyear': apiparm['year'],
                'examstart': '', 
                'examend': '',
                'activestatus': 'OFF',
                'acadyear': apiparm['year'],
                'lang': 'T',
                'download': 'download'
            }

    params2 = {
        'courseNo': int(apiparm['courseno']),
        'studyProgram': apiparm['studyProgram']
    }

    headers = {
        "Cookie": "",
        "Host": "cas.reg.chula.ac.th"
        }

    s = requests.get(mainurl + 'CourseListNewServlet', params=params1, headers=headers)
    s.encoding = "TIS-620"

    headers = {
        "Cookie": str(s.cookies).split(" ")[1],
        "Host": "cas.reg.chula.ac.th"
        }

    s = requests.get(mainurl + 'CourseListNewServlet', params=params1, headers=headers)
    s = requests.get(mainurl + 'CourseScheduleDtlNewServlet', params=params2, headers=headers)
    s.encoding = "TIS-620"
    
    output_json = html_to_json.convert(s.text)
    table = output_json['html'][0]['body'][0]['form'][0]['table']
    m = {"ม.ค.": 1,"ก.พ.": 2,"มี.ค.": 3,"เม.ย.": 4,"พ.ค.": 5,"มิ.ย.": 6,"ก.ค.": 7,"ส.ค.": 8,"ก.ย.": 9,"ต.ค.": 10,"พ.ย.": 11,"ธ.ค.": 12}
    try:
        temp = table[3]['tr'][0]['td'][0]['nobr'][0]['font'][1]['_value'].split(" ")
        temp2 = [f"{x.zfill(5)}:00" for x in temp[4].split("-")]
        tempmid = [f'{int(temp[2])-543}-{m[temp[1]]}-{temp[0]}T{temp2[0]}', f' {int(temp[2])-543}-{m[temp[1]]}-{temp[0]}T{temp2[1]}']
    except:
        tempmid = ""
    try:
        temp = table[3]['tr'][0]['td'][0]['nobr'][0]['font'][3]['_value'].split(" ")
        temp2 = [f"{x.zfill(5)}:00" for x in temp[4].split("-")]
        tempfin = [f'{int(temp[2])-543}-{m[temp[1]]}-{temp[0]}T{temp2[0]}', f'{int(temp[2])-543}-{m[temp[1]]}-{temp[0]}T{temp2[1]}']
    except:
        tempfin = ""
    temp = {
        "subject_id": c,
        "subject_name": table[1]['tr'][3]['td'][0]['nobr'][0]['font'][1]['_value'],
        "midterm_exam": tempmid,
        "final_exam": tempfin,
        "class": format_class(table[4]['tr'][1]['tr'])
    }
    return temp



'''
return {
    subject_id: (str),
    subject_name: (str),
    midterm_exam: [datetime, datetime],
    final_exam: [datetime, datetime],
    class: {
        1: {
            "LECT": [
                {
                    "day": [](int),
                    "time": [
                        time(00:00:00),
                        time
                    ],
                    "building": "",
                    "Room": ""
                }
            ],
            "LAB": {}
        }...
    } 
}
'''