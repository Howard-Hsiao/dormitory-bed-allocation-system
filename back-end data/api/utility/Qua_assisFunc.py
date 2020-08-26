from .static.Qua_config import *
from random import sample
from jieba import cut_for_search, cut
from nltk import bigrams, word_tokenize
import nltk

# assistant func 

def countBedNum(DormList):
    BedNum = {'男性':0,'女性':0}
    for index, row in DormList.iterrows():
        if('男' in row['dormName'] and row['is_disability']==0):
            BedNum['男性'] += 1
        elif('女' in row['dormName'] and row['is_disability']==0):
            BedNum['女性'] += 1
    return BedNum

def get_id_dict(id_list):
    index_value   = 1
    id_dict       = dict()
    for i in range(len(id_list)):
        for j in id_list[i]:
            if(j not in id_dict.keys()):
                id_dict[j]   =  i+1
    return id_dict

# def get_audit_dict(id_dict):
#     audit_dict = dict()
#     for i in audit_list:
#         audit_dict[i] = id_dict[i]
#     return audit_dict

def get_id2int(id_dict, StudentList):
    id_index = [0 for i in range(len(StudentList))]
    id_name = [0 for i in range(len(StudentList))]
    for index, row in StudentList.iterrows():
        # check if have special identity_type & audit status
        for i in id_col_name:
            if(str(row[i])!='nan' and row[i] in id_dict.keys() and id_dict[row[i]]>id_index[index]):
                id_index[index] = id_dict[row[i]]
                id_name[index] = row[i]
        # no special identity_type, check the habitation
        idDictNum = max(id_dict.values()) if id_dict else 0
        if(id_index[index] == 0):
            if(row['戶籍地']=='桃園市'):
                id_index[index] = idDictNum + 2
                id_name[index] = '桃園'
            elif(row['戶籍地'] in last_order_habitation):
                id_index[index] = idDictNum + 3
                id_name[index] = '北北基'
            else:
                id_index[index] = idDictNum + 1
                id_name[index] = '北北基及桃園以外的縣市'
                
    StudentList['id_index'] = id_index
    StudentList['id_name'] = id_name
    return StudentList

def get_willing2int(StudentList):
    willing_index = [0 for i in range(len(StudentList))]
    for index, row in StudentList.iterrows():
        # willing_index assign
        if(str(row['校內外意願'])!='nan'):
            willing_index[index]   = willing_InOutCam[str(row['校內外意願'])]
    StudentList['校內外意願'] = willing_index
    return StudentList

def assign_qualificaiton(df,BedNumDict):
    bedNum = BedNumDict[df.at[0,'性別']]
    id_count = df.groupby('id_index')['id_index'].count().tolist()
    curI = 0
    while(bedNum>0 and len(id_count)>0):
        if(bedNum-id_count[0]>=0):
            for i in range(id_count[0]):
                if(df.at[curI+i,'資格']==0):
                    df.at[curI+i,'資格'] = 1
                    bedNum -= 1
        else:
            RandomOrder = sample([i for i in range(id_count[0])],k=id_count[0]) if(id_count[0]<bedNum) else sample([i for i in range(id_count[0])],k=bedNum)
            for i in RandomOrder:
                df.at[curI+i,'資格'] = 1
                bedNum -= 1
                if(bedNum ==0 ):
                    break
        curI = curI + id_count[0]
        id_count = id_count[1:] 

    return df

def dealWithPreference(df):
    PfCol = ['區域志願1', '區域志願2', '區域志願3']
    for i, row in df.iterrows():
        for j in PfCol:
            if(str(row[j])=='nan'):
                df.at[i,j] = '一般區域'
    return df

def OrderAssign(df):
    df = df.sort_values('id_index').reset_index(drop = True)
    id_count            = df.groupby('id_index')['id_index'].count().tolist()
    curI                = 0
    OnListNum           = 1
    for idC in id_count:
        RandomOrder     = sample([i for i in range(idC)],k=idC)
        for i in RandomOrder:
            df.at[curI+i,'順位序號'] = OnListNum
            OnListNum           += 1
        curI            = curI + idC
    return df

def Address2Nationality(AllAddress,countryDict):
    for addressI in range(len(AllAddress)):
        # Jieba
        tokenList = cut_for_search(AllAddress[addressI]) 
        ifFound = findCountryInDict(tokenList,countryDict)
        # bigram
        if(not ifFound):
            tokenList = bigrams(word_tokenize(AllAddress[addressI]))
            tokenList = [' '.join(i) for i in tokenList]
            ifFound = findCountryInDict(tokenList,countryDict)
        # trigram & 4-gram
        count = 3
        while(not ifFound):
            tokenList = bigrams(tokenList)
            tokenList = [(i[0],i[1].split()[-1])  for i in tokenList] 
            tokenList = [' '.join(i) for i in tokenList]
            ifFound = findCountryInDict(tokenList,countryDict)
            count += 1
            if(count>4):
                break
        # special for list of 'special'
        if(not ifFound):
            SpecialCountry = ['馬來西亞','澳門']
            for i in SpecialCountry:
                if (i in AllAddress[addressI] ):
                    ifFound = i
        if(ifFound):
            AllAddress[addressI] = countryDict[ifFound]
    return AllAddress
                
def findCountryInDict(tokenList, countryDict):
    for CN in tokenList:
        if CN != '' and ((ord(str(CN[0]))>=65 and ord(str(CN[0]))<=90) or \
          (ord(str(CN[0]))>=97 and ord(str(CN[0]))<=122))and not CN[0].islower():
            CN = CN.lower()
        if CN in countryDict.keys():
            return CN
    return False
    
    
def CreateNationDF(countryDf):
    countryDict = {}
    for i,r in countryDf.iterrows():
        rList = r.tolist()
        for CNI in range(len(rList)):
            if(CNI==0 and not rList[CNI].islower()):
                rList[CNI] = rList[CNI].lower()
            countryDict[rList[CNI]] = r['國家中文名']
    return countryDict
    

    