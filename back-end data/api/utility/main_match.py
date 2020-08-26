from .match_helper import separateInternational, getIntRoomNum, selectLocIntRoomStuds, get_room_type_quota, assign_room_type, split_loc_int_rooms
from .init_helper import df2object_student, df2object_rooms, preprocess_df,find_studs, splitDisability, objs2df_studs
from .loc_match import loc_match
from .int_match import get_country_by_pop, student_by_nation_df, int_match
from .static.config import PREFERENCE_DICT, logging

#relative import issue
#https://napuzba.com/a/import-error-relative-no-parent/p4

import pandas as pd

'''Main'''
#input
#DataFrame1 (男生)
# ID, gender, 校內外意願, 區域志願1, 區域志願2, 區域志願3, 永久地址（國籍）, id_index(身障身==1)
#DataFrame2 (女生)
# ID, gender, 校內外意願, 區域志願1, 區域志願2, 區域志願3, 永久地址（國籍）, id_index(身障身==1)
#output
# ID, gender, 校內外意願, 區域志願1, 區域志願2, 區域志願3, 永久地址（國籍）, id_index(身障身==1), 宿舍, 房號, 床位

def main_match(stud_df_male, stud_df_female, room_df, debug = False):
        #TODO move logging here set debug mode
        # if (not debug):
        #         logging.basicConfig(level=logging.WARNING)
        '''Split by gender'''
        studDataMale = preprocess_df(stud_df_male)
        studDataFemale = preprocess_df(stud_df_female)
        logging.info("Students: {}/{} (male/female)".format(len(studDataMale), len(studDataFemale)))
        
        '''Rooms'''
        maleRooms, femaleRooms = df2object_rooms(room_df)
        maleRooms = sorted(maleRooms, reverse=True)
        femaleRooms = sorted(femaleRooms, reverse=True)
        logging.info("Rooms: {}/{} (male/female)".format(len(maleRooms), len(femaleRooms)))

        '''Student'''
        #init stud and room objs
        studObjsMale = df2object_student(studDataMale, gender=1)
        studObjsMale, male_disability_studs_lis = splitDisability(studObjsMale)
        studObjsFemale = df2object_student(studDataFemale, gender=0)
        studObjsFemale, female_disability_studs_lis = splitDisability(studObjsFemale)

        '''Matching'''
        male_studs_lis = _match(studDataMale, studObjsMale, maleRooms, gender=1)
        female_studs_lis = _match(studDataFemale, studObjsFemale,femaleRooms, gender=0)

        '''Merging'''
        males = male_studs_lis+male_disability_studs_lis
        females = female_studs_lis+female_disability_studs_lis

        result_male_df = objs2df_studs(males)
        result_female_df = objs2df_studs(females)

        final_male = pd.merge(left = stud_df_male, right=result_male_df, on="學號", how="outer")
        final_female = pd.merge(left = stud_df_female, right=result_female_df, on="學號", how="outer")
        # final_male.astype({'房號':'int64'})
        # final_female.astype({'房號':'int64'})
        # final_male.to_excel("finalMale.xlsx")
        # final_female.to_excel("finalFemale.xlsx")
        return final_male, final_female



def _match(studData, studObjs, roomObjs, gender):
        intStuds, locStuds = separateInternational(studObjs)
        #calculate num of int rooms  and num of loc studs in int rooms
        locIntRoomStudQuota, INTROOMNUM = getIntRoomNum(intStuds)
        #select loc studs in int rooms
        locLocRoomStuds, locIntRoomStuds = selectLocIntRoomStuds(locIntRoomStudQuota, locStuds)
        #split int and loc rooms
        intRoomsObjs, locRoomsObjs = split_loc_int_rooms(roomObjs,INTROOMNUM)

        allIntRoomStuds = intStuds+locIntRoomStuds
        TOTOALROOMNUM = len(roomObjs)
        LOCROOMNUM = TOTOALROOMNUM - INTROOMNUM

        g = "Male"
        if(gender==0):
                g = "Female"
        logging.info("——————{}——————".format(g))
        logging.info("  Rooms")
        logging.info("          Int {}".format(INTROOMNUM))
        logging.info("          Loc {}".format(LOCROOMNUM))
        logging.info("  Students")
        logging.info("          Int {}".format(len(allIntRoomStuds)))
        logging.info("                  int studs {}".format(len(intStuds)))
        logging.info("                  loc studs {}".format(len(locIntRoomStuds)))
        logging.info("          Loc {}".format(len(locLocRoomStuds)))

        ''' IntRoom matching'''
        #trasform stud objs back to df
        int_room_stud_df = find_studs(studData, allIntRoomStuds)
        #get type quota of the int rooms 
        roomTypeQuota = get_room_type_quota(int_room_stud_df, INTROOMNUM)
        # logging.info("Type: {}".format(roomTypeQuota))
        #assign types to int rooms
        intRoomsObjs = assign_room_type(intRoomsObjs, roomTypeQuota)
        #get country list ordered by its popularity
        sortedNations = get_country_by_pop(int_room_stud_df)
        # logging.info(sortedNations)
        #student by nationality df
        studentByNationDF = student_by_nation_df(int_room_stud_df, gender, sortedNations)

        arranged_int_studs_lis, all_int_rooms_objs = int_match(sortedNations, intRoomsObjs, studentByNationDF)

        # '''locRoom'''
        loc_room_stud_df = find_studs(studData, locLocRoomStuds)
        roomTypeQuota = get_room_type_quota(loc_room_stud_df, LOCROOMNUM)
        # logging.info("Loc Rooms: {}".format(roomTypeQuota))
        locRoomsObjs = assign_room_type(locRoomsObjs, roomTypeQuota)
        arranged_loc_studs_lis, all_loc_rooms_objs = loc_match(locRoomsObjs, locLocRoomStuds)

        logging.info("——————Results——————")
        logging.info("  Rooms")
        logging.info("          Int {}/{} (arranged/all)" \
                .format(len(all_int_rooms_objs), INTROOMNUM))
        
        logging.info("          Loc: {}/{} (arranged/all)" \
                .format(len(all_loc_rooms_objs), LOCROOMNUM))
        
        logging.info("  Students")
        logging.info("          Int: {}/{} (arranged/all)" \
                .format(len(arranged_int_studs_lis), len(int_room_stud_df)))        
        logging.info("          Loc: {}/{} (arranged/all)" \
                .format(len(arranged_loc_studs_lis), len(loc_room_stud_df)))

        return arranged_loc_studs_lis+arranged_int_studs_lis


# stud_df_male = pd.read_excel("../BoyQua.xlsx")
# stud_df_female = pd.read_excel("../GirlQua.xlsx")
# room_df = pd.read_excel("../DormRoom.xlsx")
# main_match(stud_df_male, stud_df_female, room_df)