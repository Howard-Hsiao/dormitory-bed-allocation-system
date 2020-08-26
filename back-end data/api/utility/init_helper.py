import sys
import random
from handler.student_handler import Student
from handler.room_handler import Room
from .static.config import PREFERENCE_DICT, NATIONALITIES, LOCAL_NATIONALITY, logging
from .static.Qua_config import countryDict
import pandas as pd

def preprocess_df(df):
    df = df.rename({'學號':"ID",'性別':'gender', '校內外意願': 'OnCampus', '區域志願1': 'pref_1','區域志願2':'pref_2','區域志願3':'pref_3','戶籍地':'address', '永久地址':'nationality','id_index':'identity', '資格':'disability'}, axis="columns")
    logging.debug(df.columns)
    #replace preference columns with symbols
    df.replace(PREFERENCE_DICT, inplace=True)
    df.loc[df["address"] != "境外", 'nationality']= LOCAL_NATIONALITY
    df.replace({"男性":1, "女性":0}, inplace=True)
    
    #only for debug
    new_nationalities = []
    for stud_index in range(len(df)):
        nationality = df.iloc[stud_index]['nationality']
        if (countryDict.get(nationality) or nationality == LOCAL_NATIONALITY):          
            new_nationalities.append(nationality)
        else:
            #if the nationality is wrong
            new_nationalities.append("國籍缺漏")

    df["nationality"] = new_nationalities
    return df

def df2object_student(df, gender):
    studs_lis = []
    for i in range(len(df)):
        attris = dict(df.iloc[i])
        #disable
        if int(attris['disability']) == 2:
            s = Student(_id=int(attris['ID']),nationality = attris['nationality'], preferences = [attris['pref_1'], attris['pref_2'], attris['pref_3']], gender=gender, disability = True)
        else:
            s = Student(_id=int(attris['ID']),nationality = attris['nationality'], preferences = [attris['pref_1'], attris['pref_2'], attris['pref_3']], gender=gender)
        studs_lis.append(s)
    return studs_lis

def splitDisability(studs):
    studs_lis = []
    disable_studs_lis = []
    for stud in studs:
        if (stud.isDisable()):
            disable_studs_lis.append(stud)
        else:
            studs_lis.append(stud)
    return studs_lis, disable_studs_lis


def df2object_rooms(room_df):
    male_rooms_dict = {}
    female_rooms_dict = {}
    for index in range(len(room_df)):
        gender = 1
        container = male_rooms_dict
        if ("女" in room_df.loc[index]['dormName']):
            container = female_rooms_dict
            gender = 0
        room_num = room_df.loc[index]['Room']
        if (room_df.loc[index]['is_disability']==0):
            # add bed into the existing room
            if (container.get(room_num)):
                if (container[room_num].getDorm() == room_df.loc[index]['dormName']):
                    container[room_num].setAvail(room_df.loc[index]['Bed'])
            # add s new room
            else:
                r = Room(gender=gender, room_num=room_df.loc[index]['Room'], _type = '', available_beds=room_df.loc[index]['Bed'], dorm=room_df.loc[index]['dormName'])
                container[r.getNum()] = r
    return list(male_rooms_dict.values()), list(female_rooms_dict.values())


def find_studs(studData, objs):
    IDs = []
    for obj in objs:
        IDs.append(str(obj._id))
    return studData[studData["ID"].isin(IDs)]

def objs2df_studs(studs):
    df = pd.DataFrame()
    ids = []
    beds = []
    dorms = []
    rooms = []
    for stud in studs:
        _id = stud.getID()
        bed = stud.getBed()
        dorm = stud.getDorm()
        room = stud.getRoom()
        ids.append(str(_id))
        beds.append(bed)
        dorms.append(dorm)
        rooms.append(int(room))
        #TODO add data into lis and insert as new columns
    df['學號'] = ids
    df['宿舍'] = dorms
    df['房號'] = rooms
    df["床位"] = beds
    return df
    