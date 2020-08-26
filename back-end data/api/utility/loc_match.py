from .match_helper import categorize, type_room_dict
import logging
arranged_studs_lis = []

def groupRoommateWithTypes(group, type2RoomDict):
    global arranged_studs_lis
    for _type in group.keys():
        # See if there are still 4 people left in a type.
        while(len(group[_type]) >= 4):
            # Check if there is still a room with that type
            if (len(type2RoomDict[_type]) > 0):
                room = type2RoomDict[_type][-1]
                while (not room.isFull()):
                    student = group[_type].pop()
                    room.addDweller(student)          
                    arranged_studs_lis.append(student)
                    logging.debug("success arrange one student!")
                type2RoomDict[_type].pop()
                type2RoomDict['finish'].append(room)
            # no more that type of room
            else:
                break
    return group

def loc_match(rooms, students):
    global arranged_studs_lis
    type2RoomDict = type_room_dict(rooms)
    roomPointer = 0
    rest = students
    arranged_studs_lis = []
    for priority in range(3):
        group = categorize(rest, priority)
        group = groupRoommateWithTypes(group, type2RoomDict)
        rest = []
        for _type in group:
            rest.extend(group[_type])
    
    #if there is still some students left
    if (len(rest) > 0):
        for _type in type2RoomDict.keys():
            if (_type != 'finish'):
                while(len(type2RoomDict[_type])>0 and len(rest) > 0):
                    room = type2RoomDict[_type][-1]
                    while (not room.isFull() and len(rest) > 0):
                        student = rest.pop()
                        room.addDweller(student)          
                        arranged_studs_lis.append(student)       
                        logging.debug("success arrange one student!")
                    #remove room
                    type2RoomDict[_type].pop()
                    type2RoomDict['finish'].append(room)

    res=""
    for room in type2RoomDict['finish']:
        # print("matching Room:{}, Type:{}".format(room.getNum(), room.getType()))
        for dweller in room.getDweller():
            res+=(str(dweller))
            res+="\n"
        res+="\n"
    # with open("loc_match_result.txt", 'w') as f1:
    #     f1.write(res)
    
    return arranged_studs_lis, type2RoomDict['finish']
