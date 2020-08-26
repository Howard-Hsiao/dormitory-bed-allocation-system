import numpy as np

import sys
from handler.room_handler import Room
from .static.config import MAX_INT_STUD_PER_ROOM, LOCAL_NATIONALITY, PREFERENCE_DICT


def get_freq(students_data, col):
    all_data = students_data[col].values
    unique_kind = np.unique(all_data)
    count = {}
    for kind in unique_kind:
        count[kind] =  np.count_nonzero(all_data == kind, axis=None)
    return count

def get_room_type_quota(students_data,roomNum):
    # all_prefs = np.concatenate( (students_data['pref_1'].values, np.concatenate( (students_data['pref_2'].values, students_data['pref_3'].values), axis=None)),axis=None)
    # only consider the first priority when deciding # of rooms for each type
    count = get_freq(students_data, col='pref_1')
    ratio ={key: round(count[key]/sum(count.values()),2) for key in count}
    result = {key: int(ratio[key] * roomNum) for key in ratio}
    #if there are one more or less room, modify the # of rooms of the first type
    if (sum(result.values()) > roomNum):
        result[list(result.keys())[0]] -= (sum(result.values()) - roomNum)
    elif (sum(result.values()) < roomNum):
        result[list(result.keys())[0]] += (roomNum - sum(result.values()))
    return result

def getIntRoomNum(int_stud):
    intRoomNum = len(int_stud)//MAX_INT_STUD_PER_ROOM
    locStudQuota = intRoomNum
    restIntStudNum = len(int_stud)%MAX_INT_STUD_PER_ROOM
    if(restIntStudNum!=0):
        intRoomNum+=1
    if (restIntStudNum == 1):
        locStudQuota+=3
    elif (restIntStudNum == 2):
        locStudQuota+=2
    return locStudQuota, intRoomNum

def separateInternational(Gendered_students):
    international = []
    local = []
    for stu in (Gendered_students):
        if stu.nationality != LOCAL_NATIONALITY:
            international.append(stu)
        else:
            local.append(stu)
    return international, local

def takeoutStudent(priority, preference, local_students):
    left_local_students = []
    targeted_students = []
    for student in local_students:
        if (student.preferences[0] == preference):
            targeted_students.append(student)
        else:
            left_local_students.append(student)
    return targeted_students, left_local_students

def selectLocIntRoomStuds(local_student_quota, local_students):
    #功能：決定國際房數量
    local_I = []
    #選住國際區的本地生
    for priority in range(3):
        local_students_I, local_students = takeoutStudent(priority, "I", local_students)
        if local_student_quota - len(local_students_I) > 0:
            local_I.extend(local_students_I)
            #更新 quota
            local_student_quota -= len(local_students_I) 
        else:
            #demand > supply for int rooms
            while(local_student_quota > 0):
                local_I.append(local_students_I.pop())
                local_student_quota -=1
            local_students = local_students_I+local_students
            break
    #still have quota
    while(local_student_quota > 0):
        local_I.append(local_students.pop())
        local_student_quota-=1

    return local_students, local_I

# Students: local_I, local_L
# Priority: 0, 1, 2
# preferenceArray = [I, H, E, C, S, G]
def categorize(students, priority):
    #功能：依志願分群
    group = {}
    for pref in PREFERENCE_DICT.values():
        group[pref] = []
    for student in students:
        p = student.getPref(priority)
        if (p == "I"):
            group["I"].append(student)
        elif (p == "H"):
            group["H"].append(student)
        elif (p == "E"):
            group["E"].append(student)
        elif (p == "C"):
            group["C"].append(student)
        elif (p == "S"):
            group["S"].append(student)
        elif (p == "G"):
            group["G"].append(student)
    return group

def type_room_dict(rooms):
    type2RoomDict = {}
    for room in rooms:
        if room.getType() not in type2RoomDict:
            type2RoomDict[room.getType()] = [room]
        else:
            type2RoomDict[room.getType()].append(room)
    type2RoomDict['finish'] = []
    return type2RoomDict

def split_loc_int_rooms(roomObjs, IntRoomsNum):
    return roomObjs[:IntRoomsNum], roomObjs[IntRoomsNum:]

def assign_room_type(roomObjs, room_quota):
    room_i = 0
    for _type in room_quota.keys():
        quota = room_quota[_type]
        while(quota >0):
            roomObjs[room_i].setType(_type)
            quota-=1
            room_i+=1
    return roomObjs