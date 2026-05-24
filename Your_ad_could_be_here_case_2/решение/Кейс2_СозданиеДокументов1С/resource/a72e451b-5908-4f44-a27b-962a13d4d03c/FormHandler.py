# !/usr/bin/python 
# -*- coding: utf8 -*- 
# Puzzle RPA version: 3.0.3 
# remote
import sys

sys.dont_write_bytecode = True

# storage:
from puzzle_logger import configure_logger, log_process, send_message_websocket
from trace_utils import format_traceback
from pathlib import Path
from Logger import log
from Config import setupConfig
from Logger import setupLogger
from Config import getLogConfig
from Config import get1CConfig

import dynamic_form
import files_and_folders
import find_numb
import lists

# generated
# Опишите эту функцию…
def clickSetup(data):
    global PERCENTAGE
    log_process(window_log=True,block_text='Исполнить функцию')
    #m/Ao68l^oJrQChHU{rU(
    setupConfig(data)

    log_process(block_text='Исполнить функцию')

    log_process(window_log=True,block_text='Исполнить функцию')
    #/o4}M|N03gr=`(BlR$t*
    setupLogger(getLogConfig())

    log_process(block_text='Исполнить функцию')

    log_process(window_log=True,block_text='Исполнить функцию')
    #G06NHG.J@qG2_Lg~.b?U
    log(f"Setup", f"success", ''.join([str(x) for x in [f"DBPath: ", (get1CConfig())['1C_DB_PATH'], f"; Login: ", (get1CConfig())['1C_LOGIN'], f"; Password: ", lists.create_string_from_list(([f"*"] * len((get1CConfig())['1C_PASSWORD'])),(f""),block_text="Сделать текст из списка",window_log=True, current_language="ru")]]))

    log_process(block_text='Исполнить функцию')


# Опишите эту функцию…
def showForm():
    global PERCENTAGE
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #*9GyvTdHx,),E9MLw}Ug
    data = {}

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Обработка ошибки')
    try:
        # Присваивает переменной значение вставки
        log_process(window_log=True,block_text='Присвоить значение переменной')
        #TqD[M(d`4}M=7!qB^)dH
        form_result = dynamic_form.show_form((files_and_folders.get_executable_path('forms\\mainForm.json',binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),fields_defaults=None,callback_context=None,block_text="undefined",window_log=True, current_language="ru")

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #K859Jas3:m]oI)N^;~`S
        data = form_result['selectedFiles']

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Исполнить функцию')
        #n$FL5g|]N3/vE]coxKnD
        log(f"Show form", f"success", f"")

        log_process(block_text='Исполнить функцию')

    
    except Exception as error_puzzle_1_0_3v:
        error_description = find_numb.find_line_numb(error_puzzle_1_0_3v)
        log_process(window_log=True,block_text='Исполнить функцию')
        #kUhXw+V*QNoFb+dVEEg/
        log(f"Show form", f"error", f"form closed")

        log_process(block_text='Исполнить функцию')

    

    log_process(block_text='Обработка ошибки')

    return data


logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_FormHandler_proc():
        global PERCENTAGE
        try:

            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_FormHandler_proc()