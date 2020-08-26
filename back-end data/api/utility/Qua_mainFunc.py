from .static.Qua_config import *
from .Qua_assisFunc import *
import pandas as pd
import numpy as np
from .main_match import main_match

# function 1

def GetAllIdType(StudentList):
    StudentList = pd.DataFrame(StudentList[1:], columns=StudentList[0])
    id_col_name  = ['身分別1','身分別2','身分別3','特殊身份別']
    column       = [str(x) for i in range(len(id_col_name)) for x in StudentList[id_col_name[i]].tolist() if str(x)!='None']
    return sorted(list(set(column)))


# function 2

def DivideDF(ordered_IdList, StudentList, DormList):
    StudentList = pd.DataFrame(StudentList[1:], columns=StudentList[0])
    StudentList['學號'] = [str(i) for i in range(len(StudentList))] # TODO: remove!
    DormList = pd.DataFrame(DormList[1:], columns=DormList[0])

    StudentList = StudentList.drop(columns = Ori_ColumnToBeDrop)
    BedNumDict = countBedNum(DormList)
    
    # get get_str2int
    id_dict = get_id_dict(ordered_IdList)
    # StudentList = get_str2int(id_dict, StudentList) # string contain id & willingness
    StudentList = get_id2int(id_dict, StudentList)
    StudentList = get_willing2int(StudentList)
    
    # divide in-out campus
    StudentList = StudentList.sort_values(by = '校內外意願').reset_index(drop = True)
    InCamNum = len(StudentList)-StudentList.groupby('校內外意願').count()['性別'][3]
    
    InCam_df = StudentList.iloc[:InCamNum,:]
    InCam_df = InCam_df.sort_values(by = '性別').reset_index(drop = True)
    InCam_df['資格'] = [2 if (row['id_index']==1 and row['是否需要安排身障房間']=='是') else 0 for index,row in InCam_df.iterrows()]
    
    # incampus divide boy-girl
    GirlInCamNum = InCam_df.groupby(['性別']).size()['女性']
    GirlInCam = InCam_df.iloc[:GirlInCamNum,:].sort_values(by='id_index').reset_index(drop=True)
    BoyInCam = InCam_df.iloc[GirlInCamNum:,:].sort_values(by='id_index').reset_index(drop=True)

    
    # WaitDF
    WaitDF = StudentList.iloc[InCamNum:,:]
    
    
    # get qualification of boy&girl df
    GirlInCam = dealWithPreference(assign_qualificaiton(GirlInCam,BedNumDict))
    BoyInCam = dealWithPreference(assign_qualificaiton(BoyInCam,BedNumDict))
    GirlInCam = GirlInCam.sort_values(by='資格').reset_index(drop=True)
    BoyInCam = BoyInCam.sort_values(by='資格').reset_index(drop=True)
    
        
    # All-Wait DF
    QuaGirlGroup = GirlInCam.groupby('資格').count()
    NoQuaGirlNum = QuaGirlGroup['性別'][0]
    QuaBoyGroup = BoyInCam.groupby('資格').count()
    NoQuaBoyNum = QuaBoyGroup['性別'][0]
    WaitAllDf = [GirlInCam.iloc[:NoQuaGirlNum,:],BoyInCam.iloc[:NoQuaBoyNum],WaitDF]
    WaitDF = pd.concat(WaitAllDf)
    
    
    # Output Girl&Boy df
    GirlInCam = GirlInCam.iloc[NoQuaGirlNum:,:].drop(columns = AlgorithmNeedDrop).sort_values(by='id_index').reset_index(drop=True)
    BoyInCam = BoyInCam.iloc[NoQuaBoyNum:,:].drop(columns = AlgorithmNeedDrop).sort_values(by='id_index').reset_index(drop=True)
    GirlInCam['永久地址'] = Address2Nationality(GirlInCam['永久地址'],countryDict)
    BoyInCam['永久地址'] = Address2Nationality(BoyInCam['永久地址'],countryDict)

    
    # organize Wait df
    WaitDF = WaitDF.drop(columns=Wait_Drop)
    return BoyInCam, GirlInCam, WaitDF
    
def list2df(beds):
    columns = beds[0]
    data = beds[1:]
    df = pd.DataFrame(data, columns = beds[0])
    return df

def Match(BoyInQua, GirlInQua, beds):
    beds_df = list2df(beds)
    BoyInQua, GirlInQua = main_match(BoyInQua, GirlInQua, beds_df)
    return BoyInQua, GirlInQua

# function4
def GetOutputDF(id_orderList, BoyQua, GirlQua, StudentList, WaitDF):
    # BoyQua = pd.DataFrame(BoyQua[1:], columns=BoyQua[0])
    # GirlQua = pd.DataFrame(GirlQua[1:], columns=GirlQua[0])
    StudentList = pd.DataFrame(StudentList[1:], columns=StudentList[0])
    StudentList['學號'] = [str(i) for i in range(len(StudentList))] # TODO: remove!
    # WaitDF = pd.DataFrame(WaitDF[1:], columns=WaitDF[0])

    # Divide WaitDF => campus,BOT
    WaitDF = WaitDF.sort_values('校內外意願')
    WillGroupNum = WaitDF.groupby('校內外意願')
    CampusNum = WillGroupNum.count()['性別'][1] + WillGroupNum.count()['性別'][2]
    NotBotNum = len(WaitDF) - WillGroupNum.count()['性別'][2] - WillGroupNum.count()['性別'][3]
    
    Campus = WaitDF.iloc[:CampusNum,:].drop(columns = CampusWait_Drop_AsQua).sort_values('性別')
    Bot = WaitDF.iloc[NotBotNum:,:]
    
    # organize Campus
    Campus['資格'] = [0 for i in range(len(Campus))]
    CampusGirlNum = Campus.groupby('性別')['性別'].count().tolist()[0]
    CampusBoy = OrderAssign(Campus.iloc[CampusGirlNum:])
    CampusGirl = OrderAssign(Campus.iloc[:CampusGirlNum])
    
    BoyQua['順位序號'] = [0 for i in range(len(BoyQua))]
    GirlQua['順位序號'] = [0 for i in range(len(GirlQua))]
    
    CampusBoy = pd.concat([BoyQua,CampusBoy]).sort_values(by='順位序號')
    CampusGirl = pd.concat([GirlQua,CampusGirl]).sort_values(by='順位序號')
    
    # get get_id2int
    id_dict = get_id_dict(id_orderList)
    # audit_dict = get_audit_dict(id_dict)
    StudentList = get_id2int(id_dict, StudentList)

    # drop and merge
    CampusBoy = CampusBoy.drop(columns=Qua_Drop)
    CampusGirl = CampusGirl.drop(columns=Qua_Drop)
    StudentListMergeWithCampus = StudentList.drop(columns = Ori_DfDropForICampus)
    CampusBoy = pd.merge(CampusBoy,StudentListMergeWithCampus,on=['學號']).reset_index(drop=True)
    CampusGirl = pd.merge(CampusGirl,StudentListMergeWithCampus,on=['學號']).reset_index(drop=True)
    
    # BOT drop & merge & Divide => BotBoy, BotGirl
    Bot = Bot.sort_values('性別')
    BotGirlNum = Bot.groupby('性別')['性別'].count().tolist()[0]
    BotBoy = OrderAssign(Bot.iloc[BotGirlNum:]).sort_values(by='順位序號')
    BotGirl = OrderAssign(Bot.iloc[:BotGirlNum]).sort_values(by='順位序號')
    
    StudentListMergeWithBot = StudentList.drop(columns = StudentList_Drop_ForMapBot)
    BotBoy = BotBoy.drop(columns=Bot_Drop_ForOutput).reset_index(drop=True)
    BotBoy = pd.merge(BotBoy,StudentListMergeWithBot,on=['學號'])
    BotGirl = BotGirl.drop(columns=Bot_Drop_ForOutput).reset_index(drop=True)
    BotGirl = pd.merge(BotGirl,StudentListMergeWithBot,on=['學號'])
    
    CampusGirl.replace(np.nan, 0, inplace=True)
    CampusGirl[['順位序號','房號']] = CampusGirl[['順位序號','房號']].astype(int)
    CampusBoy.replace(np.nan, 0, inplace=True)
    CampusBoy[['順位序號','房號']] = CampusBoy[['順位序號','房號']].astype(int)
    BotBoy.replace(np.nan, 0, inplace=True)
    BotBoy[['順位序號']] = BotBoy[['順位序號']].astype(int)
    BotGirl.replace(np.nan, 0, inplace=True)
    BotGirl[['順位序號']] = BotGirl[['順位序號']].astype(int)

    CampusBoy = CampusBoy.fillna('None')
    CampusGirl = CampusGirl.fillna('None')

    # remove nan
    BotBoy = BotBoy.fillna('None')
    BotGirl = BotGirl.fillna('None')

    Campus_col = CampusBoy.columns.tolist()
    Bot_col = BotBoy.columns.tolist()

    # to list
    CampusBoy = CampusBoy.values.tolist()
    CampusBoy.insert(0, Campus_col)
    CampusGirl = CampusGirl.values.tolist()
    CampusGirl.insert(0, Campus_col)
    BotBoy = BotBoy.values.tolist()
    BotBoy.insert(0, Bot_col)
    BotGirl = BotGirl.values.tolist()
    BotGirl.insert(0, Bot_col)
    
    # print result len
    print('CampusBoy', len(CampusBoy))
    print('CampusGirl', len(CampusGirl))
    print('BotBoy', len(BotBoy))
    print('BotGirl', len(BotGirl))
    
    return CampusBoy, CampusGirl, BotBoy, BotGirl
    
