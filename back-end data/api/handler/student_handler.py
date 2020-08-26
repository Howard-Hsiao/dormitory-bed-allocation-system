class Student:
    def __init__(self, _id, preferences, nationality, gender, disability=False):
        super().__init__()
        self._id = _id
        #1x3 array of preferences (e.g. [“I”, “H”, “E”])
        self.preferences = preferences
        #string
        self.nationality = nationality
        #int (0:girl; 1:boy)
        self.gender = gender
        #dorm 
        self.dorm = ''
        #room number
        if(disability):
            self.room = 0
        else:
            self.room = -1
        #bed ABCD
        self.bed = ''

        self.arranged = False
        
        self.disability = disability
        
    def isDisable(self):
        return self.disability

    def getID(self):
        return self._id

    def getPref(self, priority):
        return self.preferences[priority]

    def setDorm(self, dorm):
        self.dorm = dorm
    
    def getDorm(self):
        return self.dorm

    def getRoom(self):
        return self.room

    def setRoom(self, room):
        self.room = room

    def getBed(self):
        return self.bed

    def setBed(self, bed):
        self.bed = bed
    
    def setArranged(self, signal):
        self.arranged = signal

    def isArranged(self):
        return self.arranged

    def __gt__(self, other):
        if (self._id > other._id):
            return True
        else:
            return False
        
    def __lt__(self, other):
        if (self._id < other._id):
            return True
        else:
            return False

    def __eq__(self, other):
        if (self._id == other._id):
            return True
        else:
            return False

    def __str__(self):
        gender = "Male"
        if (self.gender==0):
            gender = "Famale"
        return "id: {}, nationality: {}, gender: {}, preferences: {}".format(self._id, self.nationality, self.gender, self.preferences)