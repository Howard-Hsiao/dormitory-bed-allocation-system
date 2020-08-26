class Room:
    MAXROOMCAPACITY = 4
    def __init__(self, gender, room_num, _type, available_beds,  dorm):
        super().__init__()
        #int (0:girl;1:boy)
        self.gender = gender
        #string
        self.dorm = dorm
        #int
        self.room_num = room_num
        #type: string (e.g. “I”, “H”, “E”, “C”)
        self.room_type = _type
        #dict: key is bed number and value is student objects
        self.dwellers = {}
        #list: available beds. e.g. ["A", "B", "C", "D"]
        self.available_beds = [available_beds]
    
    def addDweller(self, student):
        student.setRoom(self.room_num)
        student.setBed(self.available_beds.pop())
        student.setDorm(self.dorm)
        self.dwellers[student.getBed()] = student

    def getDweller(self):
        return list(self.dwellers.values())
    
    #return an array of dwellers’ nationalities
    def getDwellerNationality(self):
        if (len(self.dwellers)==0):
            return None
        else:
            return [dweller.nationality for dweller in list(self.dwellers.values())]

    def getDwellerPreference(self):
        if (len(self.dwellers)==0):
            return None
        else:
            return [dweller.preference for dweller in list(self.dwellers.values())]
    
    def setType(self, _type):
        self.room_type = _type

    def getType(self):
        return self.room_type

    def getNum(self):
        return self.room_num
        
    def setAvail(self, bed):
        self.available_beds.append(bed)

    def isFull(self):
        return len(self.available_beds)==0

    def getMemberNum(self):
        return len(self.dwellers)

    def getDorm(self):
        return self.dorm

    def getGender(self):
        return self.gender

    def __getitem__(self, bed):
        if(len(self.dwellers)==0):
            return IndexError
        else:
            return self.dwellers[bed]
    
    def __gt__(self, other):
        if (len(self.available_beds) > len(other.available_beds)):
            return True
        else:
            return False

    def __lt__(self, other):
        if (len(self.available_beds) < len(other.available_beds)):
            return True
        else:
            return False

    def __eq__(self, other):
        return len(self.available_beds) == len(other.available_beds)

    def __str__(self):
        return "Dorm: {}\n\tRoom Number: {}\n\tRoom Type: {}\n\tBeds: {}".format(self.dorm, self.room_num, self.room_type, self.available_beds)
