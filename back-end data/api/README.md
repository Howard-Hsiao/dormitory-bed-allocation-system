# API Directory Tree

```
|____handler
| |______init__.py
| |____student_handler.py
| |____room_handler.py
|____app
| |______init__.py
|____requirements.txt
|______init__.py
|____finalFemale.xlsx
|____finalMale.xlsx
|____main.py
|____utility
| |____int_match.py
| |____save_result.py
| |____match_helper.py
| |____Qua_mainFunc.py
| |____performanceIndex.py
| |______init__.py
| |____Qua_assisFunc.py
| |____init_helper.py
| |____static
| | |____config.py
| | |____Qua_config.py
| |____main_match.py
| |____loc_match.py
|____router
| |______init__.py
| |____router.py
```
# DORM MATCHING API DOCUMENT

### `[POST] /api/get_all_identities`
> get all identities from the given student file

Request
```
[
    [col1, col2, col3,...],
    [atr1, atr2, atr3,...].
    [atr1, atr2, atr3,...],
    ...
]
```

Response 200 OK Success
```
[
    identity1,
    identity2,
    identity3,
    identity4,
    ...
]
```
### `[POST] /api/match`
> return all matching results

Request
```
{
    "priority":[
        [identify1, identify2],
        [identify3],
        ...
    ],
    "student":[
        [col1, col2, col3,...],
        [atr1, atr2, atr3,...].
        [atr1, atr2, atr3,...],
    ],
    "beds":[
        [dormName, Room, Bed, Student_ID, is_disability,...],
        [atr1, atr2, atr3,...],
        [atr1, atr2, atr3,...],
    ]
}
```

Response 200 OK Success
```
{
    "men_campus_dorm": [
        [資格狀態,宿舍名稱,寢室,床位,系所名稱,學號,性別,姓名,身份別,校內外意願,區域志願1,區域志願2,區域志願3,戶籍地,國籍,是否需要安排身障房間],
        [atr1, atr2, atr3,...].
        [atr1, atr2, atr3,...],
        ...
    ],
    "women_campus_dorm": [
        [資格狀態,宿舍名稱,寢室,床位,系所名稱,學號,性別,姓名,身份別,校內外意願,區域志願1,區域志願2,區域志願3,戶籍地,國籍,是否需要安排身障房間],
        [atr1, atr2, atr3,...].
        [atr1, atr2, atr3,...],
        ...
    ],
    "men_BOT":[
        [順位序號,系所名稱,學號,性別,姓名,身份別,校內外意願,區域志願1,區域志願2,區域志願3,戶籍地,國籍,是否需要安排身障房間],
        [atr1, atr2, atr3,...].
        [atr1, atr2, atr3,...],
        ...
    ],
    "women_BOT":[
        [順位序號,系所名稱,學號,性別,姓名,身份別,校內外意願,區域志願1,區域志願2,區域志願3,戶籍地,國籍,是否需要安排身障房間],
        [atr1, atr2, atr3,...].
        [atr1, atr2, atr3,...],
        ...
    ]
}
```

## Backend Functions

### Main functions
Return all kinds of unique identities
input
```
def GetAllIdType(StudentList):
    ...
    return  AllIdType
```

Select dormatory qualification
input
```
def DivideDF(ordered_IdList, StudentList, DormList):
    ...
    return GirlQua, BoyQua, WaitDF
```

macthing students
```
 def matching(qualification_students):
     ...
     return matched_students
```
process data for frontend display use
```
def frontend_display_df(result):
    ...
    return display_result
```
> Campus

| 學號 | 資格 | 宿舍 | 房號 | 床位 | 性別 | id_name | 校內外意願 | 區域志願1 | 區域志願2 | 區域志願3 | 永久地址 | 是否需要安排身障房間 | 順位序號 |
| ---- | ---- | ---- | ---- | ---- | ---- | ------- | ---------- | --------- | --------- | --------- | -------- | -------------------- | -------- |
> BOT


| 性別 | 身份別 | 校內外意願 | 永久地址 | 是否需要安排身障房間 | 學號 | 順位序號 |
| ---- | ------ | ---------- | -------- | -------------------- | ---- | -------- |
process data for download use

```
def get_result_for_download():
    ...
    return campus_men, campus_women, bot_men, bot_woman
```
### Helper functions
merge the result back to the original dataframe
```
def matching_postprocess(qualification_students, waiting_students):
    ...
    return merged_result
```

### How to make executable from main.py
1. Install pyinstaller
2. Input the command:
```
pyinstaller main.spec
```

### ! The following document may be helpful if pyinstaller behaves oddly
* [If the executable starts up too slowly](https://stackoverflow.com/questions/9469932/app-created-with-pyinstaller-has-a-slow-startup)
* [If pyinstaller cannot successly handle "nltk_data"](https://stackoverflow.com/questions/54659466/nltk-hook-unable-to-find-nltk-data)
* [FileNotFoundError: [Errno 2] No such file or directory: '-': jmakitalo's answer](https://github.com/pyinstaller/pyinstaller/issues/4034)
