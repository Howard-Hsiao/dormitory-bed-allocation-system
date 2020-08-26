import sys
sys.path.insert(0, '../utility/')
from static.config import PREFERENCE_DICT

from munkres import Munkres
import random
seed = 30
random.seed(seed)

ROOMNUM = 1516//4
all_room_types_symbol = list(PREFERENCE_DICT.values())
all_rooms = [ [random.choices(all_room_types_symbol)+"_"+str(i)+"_"+str(bed) for i in ROOMNUM] for bed in range(4) ]

#first choice, second choice, third choice, not my choice
cost_table = [1, 5, 10, 100]

def compute_cost_matrix(students):
    cost_matrix = []
    for i in range(len(students)):
        prefs_lis = list(students.iloc[i][2:5])
        #init a student's cost_lis with no matching costs
        cost_lis = [cost_table[3] for i in range(len(all_room_types_symbol))]
        for j in range(len(prefs_lis)):
            if prefs_lis[j] == all_room_types_symbol[0]:
                cost_lis[0] = cost_table[j]
            elif prefs_lis[j] == all_room_types_symbol[1]:
                cost_lis[1] = cost_table[j]
            elif prefs_lis[j] == all_room_types_symbol[2]:
                cost_lis[2] = cost_table[j]
            elif prefs_lis[j] == all_room_types_symbol[3]:
                cost_lis[3] = cost_table[j]
            elif prefs_lis[j] == all_room_types_symbol[4]:
                cost_lis[4] = cost_table[j]
            elif prefs_lis[j] == all_room_types_symbol[5]:
                cost_lis[5] = cost_table[j]
        cost_matrix.append(cost_lis)
    return cost_matrix


def loc_match_test(students):
    m = Munkres()

    cost_matrix = compute_cost_matrix(students)
    indexes = m.compute(cost_matrix)
    print_matrix(cost_matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        value = cost_matrix[row][column]
        total += value
        print ("(%d, %d) -> %d"%(row, column, value))
    print ("total cost: %d"% (total))
