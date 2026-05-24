# !/usr/bin/python 
# -*- coding: utf8 -*- 
# Puzzle RPA version: 3.0.3 
# remote
from os import path
import json
import os
import shutil
import sys

sys.dont_write_bytecode = True

# storage:
from puzzle_logger import configure_logger, log_process, send_message_websocket
from trace_utils import format_traceback
from pathlib import Path

import current_date_mod
import data_io.json as data_io_json
import files_and_folders
import is_there_way

# generated
# Опишите эту функцию…
def getLogFile():
    global SHOW_LOGS
    return files_and_folders.get_executable_path('logs.json',binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")

# Опишите эту функцию…
def initLogger():
    global SHOW_LOGS
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #aqHjGA953/+uE?=(w|*y
    SHOW_LOGS = True

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Если – выполнить')
    #{{gT^q%e1PPk[bHH@TZ:
    if is_there_way.is_there_way((getLogFile()),block_text="Существует путь?",window_log=True, current_language="ru"):
        #@QU0o(3QawbK,,LD/5;k
        files_and_folders.delete_file((getLogFile()),block_text="Удалить файл/папку",window_log=True, current_language="ru")


    log_process(block_text='Если – выполнить')

    #1ktN(ZKKyXKG%-[j~zfP
    files_and_folders.create_json((getLogFile()),'utf-8',{
        'logs': []
    },block_text="Создать json-файл",window_log=True, current_language="ru")


# Опишите эту функцию…
def log(operation, status, message):
    global SHOW_LOGS
    log_process(window_log=True,block_text='Если/вернуть')
    #O|jkdG,Dqds`i?JEQqi4
    if not SHOW_LOGS:
        return

    log_process(block_text='Если/вернуть')

    # Присваивает переменной значение вставки
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #tZS^#{F+|+d/HJ8{{r`r
    file_content = data_io_json.read_json_file('utf-8',(getLogFile()),block_text="Прочитать файл",window_log=True, current_language="ru")

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Добавить элемент в список')
    #o$tGg~DcWn=9|ri,ejOl
    (file_content['logs']).append({
        'operation': operation,
        'status': status,
        'message': message,
        'time': (current_date_mod.current_date_mod('%d.%m.%Y %H:%M:%S',block_text="Получить текущую дату",window_log=True, current_language="ru"))
    })

    log_process(block_text='Добавить элемент в список')

    #g6N{%](v3r,z71C)MX|1
    files_and_folders.append_txt_file(file_path=(getLogFile()), data=file_content, encoding='utf-8',block_text="Дописать в файл",window_log=True, current_language="ru")


# Опишите эту функцию…
def setupLogger(showLogs):
    global SHOW_LOGS
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #cg|i$|3NYF-QB|;;;wNX
    SHOW_LOGS = showLogs

    log_process(block_text='Присвоить значение переменной')



logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_Logger_proc():
        global SHOW_LOGS
        try:

            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_Logger_proc()