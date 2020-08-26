import math

import logging
logging.basicConfig(level=logging.INFO)
# pacakge for debug mode
# tutorial: https://titangene.github.io/article/python-logging.html

PREFERENCE_DICT = {
    "國際互動區":"I",
    "健康作息區":"H",
    "節能減碳區":"E",
    "整潔模範區":"C",
    "運動休閒區":"S",
    "一般區域":"G",
    math.nan: "G",
}


NATIONALITIES = \
    [
        "China",
        "India",
        "Indonesia",
        "Pakistan",
        "Bangladesh",
        "Japan",
        "Philippines",
        "Vietnam",
        "Turkey",
        "Iran",
        "Thailand",
        "Myanmar",
        "South Korea",
        "Iraq",
        "Afghanistan"
    ]

LOCAL_NATIONALITY = "Taiwan"

MAX_INT_STUD_PER_ROOM = 3
