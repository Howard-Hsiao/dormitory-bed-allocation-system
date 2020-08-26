import pandas as pd

def genderal_performance(df):
    satisfied_room=0
    groupbyroom = list(df.groupby("房號"))
    for rommNum,studs in groupbyroom:
        pref_1_set = set(studs.groupby('區域志願1').count()['Unnamed: 0'])
        #if 境外 is inside, 3 matches are enough
        if ('境外' in studs['戶籍地']):
            if (pref_1_set=={1,3}):
                satisfied_room+=1
        #4 matches
        else:
            if(pref_1_set=={4}):
                satisfied_room+=1

    return satisfied_room, len(groupbyroom)


def _checkIsIntStudsinRoom(df, loc_intRoom_stud_room):
    return '境外' in set(df[df['房號']==loc_intRoom_stud_room]['戶籍地'])

def prefSatisfationRate(df):
    groupbypref = list(df.groupby("區域志願1"))
    pref_satisfication = {}
    for pref, studs in groupbypref:
        satisfied_studs = 0
        pref_all_room = list(studs.groupby("房號"))
        for room_num, room_studs in pref_all_room:
            #if 境外 is inside, 3 matches are enough. The other one is a random loc stud
            if ('境外' in room_studs['戶籍地']):
                if (len(room_studs)==3):
                    satisfied_studs+=3
            
            #local studs
            elif (len(room_studs)==4):
                satisfied_studs+=4
                
            #local studs whose pref_1 is 國際互動區 
            #loc studs with 境外 studs are counted as satisfied
            if(pref=='國際互動區' and len(room_studs)==1):
                isSatisfied = _checkIsIntStudsinRoom(df, room_studs['房號'].iloc[0])
                if (isSatisfied):
                    satisfied_studs+=1
        
        pref_satisfication[pref] = (satisfied_studs, len(studs) )
    return pref_satisfication


    
        



male = pd.read_excel("finalMale.xlsx")
female = pd.read_excel("finalFemale.xlsx")
male_satisfied_rooms, male_all_rooms = genderal_performance(male)
female_satisfied_rooms, female_all_rooms = genderal_performance(female)
male_pref_satisfication = prefSatisfationRate(male)
female_pref_satisfication = prefSatisfationRate(female)

print("General Room Satisfication: {}%, {}/{}".format(\
    round(100*(male_satisfied_rooms+female_satisfied_rooms)/(male_all_rooms+female_all_rooms),2),
    male_satisfied_rooms+female_satisfied_rooms, \
    male_all_rooms+female_all_rooms))
for key in male_pref_satisfication.keys():
    print("{}: {}%, {}/{}".format(key, \
        round(100*(male_pref_satisfication[key][0]+female_pref_satisfication[key][0])/(male_pref_satisfication[key][1]+female_pref_satisfication[key][1]),2),
        male_pref_satisfication[key][0]+female_pref_satisfication[key][0], \
        male_pref_satisfication[key][1]+female_pref_satisfication[key][1]))