#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
import csv
import codecs
import datetime
import os
import pandas as pd

from dotenv import load_dotenv


load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_URL = os.getenv('AWS_URL')
KEY_FILE = 'data.csv'

# s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
#                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# data = s3.get_object(AWS_STORAGE_BUCKET_NAME, KEY_FILE)

# for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"])):
#     print(row[1])

s3 = boto3.resource(
    service_name='s3',
    region_name='eu-north-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
s3_object = s3.Object(AWS_STORAGE_BUCKET_NAME, KEY_FILE)

data = s3_object.get()['Body'].read().split(b'\n')
csv_data = csv.DictReader(data)


users_type = {
    1: 'пользователь',
    2: 'пользователя',
    3: 'пользователя',
    4: 'пользователя'
}
day_type = {
    0: 'дней',
    1: 'день',
    2: 'дня',
    3: 'дня',
    4: 'дня',
}
for days in range(5, 10000):
    day_type[days] = 'дней'


# remove txt file
def remove():
    path = os.getcwd() + '/Статистика.txt'
    os.remove(path)


# write data to csv
def statistics(user_id, command):
    data = datetime.datetime.today().strftime("%Y-%m-%d")
    with open(data, 'a', newline="", encoding='UTF-8') as fil:
        print(fil)
        wr = csv.writer(fil, delimiter=';')
        wr.writerow([data, user_id, command])


# make report
def analysis(bid):
    season = int(bid[1])
    df = pd.read_csv(data, delimiter=';', encoding='utf8')
    print(df)
    number_of_users = len(df['id'].unique())
    number_of_days = len(df['data'].unique())

    message_to_user = 'Статистика использования бота за %s %s: \n' % (
        season,
        day_type.get(season, day_type[season]))
    message_to_user += 'Всего статистика собрана за %s %s: \n\n' % (
        number_of_days,
        day_type.get(season, day_type[season]))
    if season > number_of_days:
        season = number_of_days
        message_to_user += 'Указанное вами количество дней больше, чем имеется\n' \
                           'Будет выведена статистика за максимальное возможное время\n\n'

    df_user = df.groupby(['data', 'id']).count().reset_index().groupby('data').count().reset_index()
    list_of_dates_in_df_user = list(df_user['data'])
    list_of_number_of_user_in_df_user = list(df_user['id'])
    list_of_dates_in_df_user = list_of_dates_in_df_user[-season:]
    list_of_number_of_user_in_df_user = list_of_number_of_user_in_df_user[-season:]
    df_command = df.groupby(['data', 'command']).count().reset_index()
    unique_commands = df['command'].unique()
    commands_in_each_day = []
    list_of_dates_in_df_command = list(df_command['data'])
    list_of_number_of_user_in_df_command = list(df_command['id'])
    list_of_name_of_command_in_df_command = list(df_command['command'])
    commands_in_this_day = dict()
    for i in range(len(list_of_dates_in_df_command)):
        commands_in_this_day[list_of_name_of_command_in_df_command[i]] = list_of_number_of_user_in_df_command[i]
        if i + 1 >= len(list_of_dates_in_df_command) or list_of_dates_in_df_command[i] != list_of_dates_in_df_command[i + 1]:
            commands_in_each_day.append(commands_in_this_day)
            commands_in_this_day = dict()
    commands_in_each_day = commands_in_each_day[-season:]

    if 'пользователи' in bid:
        message_to_user += 'За всё время бота использовало: ' + '%s' % number_of_users \
                   + ' %s ' % users_type.get(number_of_users, 'пользователей') + '\n' \
                                                                                 'Пользователей за последние %s %s: \n' % (
                       season, day_type.get(season, day_type[season]))
        for days, number, comm_day in zip(
            list_of_dates_in_df_user,
            list_of_number_of_user_in_df_user,
            commands_in_each_day):
            message_to_user += 'Дата: %s Количество: %d. Из них новых: %s\n\n' % (days, number, comm_day.get('/start', 0))
    if 'команды' in bid:
        message_to_user += 'Статистика команд за последние %s %s: \n' % (
            season,
            day_type.get(season, day_type[season]))
        for days, commands in zip(
            list_of_dates_in_df_user,
            commands_in_each_day):
            message_to_user += 'Дата: %s\nИспользованные команды:\n' % days
            for i in unique_commands:
                if i in commands:
                    message_to_user += '[%s] - %s раз\n' % (i, commands.get(i))
                else:
                    message_to_user += '[%s] - 0 раз\n' % i

    if 'txt' in bid or 'тхт' in bid:
        with open('Статистика.txt', 'w', encoding='UTF-8') as fil:
            fil.write(message_to_user)
            fil.close()
    else:
        return message_to_user
