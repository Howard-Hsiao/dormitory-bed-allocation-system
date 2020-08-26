# assume the key-in data
# create dataframe
import pandas as pd

# key-in data
# if it is the single room index, change it to the range (eg. range(135,136))

# 男一舍
# 101-161
# 身障房（兩床）：135, 146-153 
# 201-262
# 301-362
# 401-462
# 大一女
# 201-238
# 301-348
# 400-443, 445-448
# 501-548


# dict{'dormName': [list(dormRoom),list(disability)}
boy_dormRoom = [[101,161],[201,262],[301,362],[401,462]]
boy_disability = [[135,136],[146,153]]
girl_dormRoom = [[201,238],[301,348],[400,443],[445,448],[501,548]]



totalRow = {'男一舍':[boy_dormRoom,boy_disability]
                  ,'大一女':[girl_dormRoom]}

df = pd.DataFrame(columns=('dormName','Room','Bed','Student_ID'))


# QQQQ: which bed is for disability(index)
Bed_index = ['A','B','C','D']

for name in totalRow.keys():
    for i in totalRow[name][0]:
        for j in range(i[0],i[1]):
            for z in Bed_index:
                newRow = pd.Series({'dormName'     :name
                                   ,'Room'         :j
                                   ,'Bed'          :z
                                   ,'Student_ID'   :''
                                   ,'is_disability':0})

                df = df.append(newRow, ignore_index=True)
    if len(totalRow[name])>1:
        for i in totalRow[name][1]:
            for j in range(i[0],i[1]):
                for z in Bed_index:
                    index = df.loc[(df['dormName']==name) & (df['Room']==j) & (df['Bed']==z)].index
                    if z in Bed_index[:2]:
                      df.loc[index,'is_disability'] = 1
                    elif z in Bed_index[2:]:
                      df.drop(index,inplace = True)
                    
df.reset_index()
df.to_excel('DormRoom.xlsx')