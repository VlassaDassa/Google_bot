# GOOGLE
from google_sheets.Spreadsheet import Spreadsheet

# CONFIG
import config as cfg

# DATABASE
from database.sqlite_client import Database_client

# GRAPH
import matplotlib.pyplot as plt

# CALENDAR
import calendar

# STATISTIC
from statistics import mean

# NUMPY
import numpy as np

# WARNINGS
import warnings

# OS
import os



# CREATE OBJECT DB
path_db = cfg.PATH_DB
db = Database_client(path_db)

# CREDENTIALS
credentials = cfg.PATH_CREDENTIALS

warnings.filterwarnings("ignore")








# FIND REPEAT VALUES
def most_frequent(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i
    return num










# В аргументы добавить число записей
message_list = {}
def create_graph(args_dict):
    fig, ax = plt.subplots()
    ax.plot(args_dict['days'], args_dict['score'], color='#008000', linewidth=5.0)
    ax.set_title('График состояния', fontsize=20)

    ax.set_xlabel(args_dict['month_name'], fontsize=15)
    ax.set_ylabel('Оценка', fontsize=15)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)



    if args_dict['count_rows'] == 10:
        ax.set_yticks(np.arange(0, 6, 1))
        ax.set_xticks(np.arange(0, len(args_dict['all_count_rows']), 1))

    if args_dict['count_rows'] == 30:
        ax.set_yticks(np.arange(0, 6, 1))
        ax.set_xticks(np.arange(0, len(args_dict['all_count_rows']), 3))

    if args_dict['count_rows'] == 'all':
        ax.set_yticks(np.arange(0, 6, 1))
        ax.set_xticks(np.arange(0, len(args_dict['all_count_rows']), 5))



    # SAVE/SEND/REMOVE
    path = os.path.abspath('google_sheets/graph_img/')
    name = '1'
    fig.savefig(path + name +'.jpg')
    args_dict['path'] = path + name + '.jpg'





    if args_dict['count_rows'] == 'all':
        if args_dict['mood'] == 'Bad':
            message_list['mood'] = f'за всё время преобладает <b>плохое</b> настроение ☹'

        if args_dict['mood'] == 'Normal':
            message_list['mood'] = f'за всё время преобладает <b>нормальное</b> настроение 😐'

        if args_dict['mood'] == 'Great':
            message_list['mood'] = f'за всё время преобладает <b>отличное</b> настроение 😁'

    else:

        if args_dict['mood'] == 'Bad':
            message_list['mood'] = f'за {args_dict["count_rows"]} дней преобладает <b>плохое</b> настроение ☹'

        if args_dict['mood'] == 'Normal':
            message_list['mood'] = f'за {args_dict["count_rows"]} дней преобладает <b>нормальное</b> настроение 😐'

        if args_dict['mood'] == 'Great':
            message_list['mood'] = f'за {args_dict["count_rows"]} дней преобладает <b>отличное</b> настроение 😁'



    message_list['average'] = args_dict['average']
    message_list['path'] = args_dict['path']


def return_message_list():
    return message_list

def clear_message_list():
    message_list.clear()









# CHECKING FOR 10 ROWS
list_10 = []
def exist_rows(count_rows, spreadsheetId):


    ss = Spreadsheet(credentials, spreadsheetId)
    sheet_title = ss.get_sheet_title(0)
    read_spreadsheet = ss.service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                              range=f"{sheet_title}!A1:C").execute()

    for i in range(2):
        read_spreadsheet['values'].pop(0)

    user_rows = read_spreadsheet['values']



    filter_rows = []
    a = 0
    for i in user_rows:
        if 'Пусто' not in i:
            filter_rows.append(user_rows[a])
        a += 1

    if count_rows == 'all':
        if len(filter_rows) < 30:
            list_10.append(False)
        else:
            list_10.append(True)
    else:
        if len(filter_rows) < count_rows:
            list_10.append(False)
        else:
            list_10.append(True)

    filter_rows.clear()


async def return_answer_exist():
    return list_10[0]

async def remove_list():
    list_10.clear()








# CREATE GRAPH 10
def create_graph_(count_rows, spreadsheetId):

    ss = Spreadsheet(credentials, spreadsheetId)
    sheet_title = ss.get_sheet_title(0)
    read_spreadsheet = ss.service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                              range=f"{sheet_title}!A1:C").execute()



    # REMOVE HEADER
    for i in range(2):
        read_spreadsheet['values'].pop(0)


    if count_rows == 'all':
        user_rows = []
        for i in range(len(read_spreadsheet['values'])):
            user_rows.append(read_spreadsheet['values'][i])
    else:
        user_rows = []
        for i in range(count_rows):
            user_rows.append(read_spreadsheet['values'][i])

    # CLEAR
    filter_rows = []
    a = 0
    for i in user_rows:
        if 'Пусто' not in i:
            filter_rows.append(user_rows[a])
        a += 1

    # SCORE
    score = []
    for i in filter_rows:
        score.append(int(i[1]))


    # DATE
    date = []
    for i in filter_rows:
        date.append(i[0])


    # DAYS
    need_date = []
    for i in date:
        bk_sl = '\\'
        need_date.append(f'{str(i.split(bk_sl)[0])}.{str(i.split(bk_sl)[1])}')



    # MONTH NAME
    month = []
    for i in date:
        month.append(i.split('\\')[1])



    number_month = most_frequent(month)
    month_name = calendar.month_name[int(number_month)]


    # AVERAGE
    average = mean(score)

    args_dict = {'days': need_date,
                 'score': score,
                 'month_name': month_name,
                 'average': average,
                 'count_rows': count_rows,
                 'all_count_rows': user_rows
                 }


    # DEFINITION OF MOOD
    if (average >= 1) and (average <= 2,5):
        args_dict['mood'] = 'Bad'

    if (average > 2,5) and (average <= 3,5):
        args_dict['mood'] = 'Normal'

    if (average > 3,5) and (average <= 5):
        args_dict['mood'] = 'Great'



    filter_rows.clear()
    create_graph(args_dict)





