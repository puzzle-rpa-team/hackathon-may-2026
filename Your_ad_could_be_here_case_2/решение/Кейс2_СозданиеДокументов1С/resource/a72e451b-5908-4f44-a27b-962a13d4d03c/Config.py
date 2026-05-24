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


# generated
# Опишите эту функцию…
def get1CConfig():
    global LOG_ENABLE, my_1C_DB_PATH, my_1C_PASSWORD, my_1C_LOGIN
    return {
    '1C_DB_PATH': my_1C_DB_PATH,
    '1C_LOGIN': my_1C_LOGIN,
    '1C_PASSWORD': my_1C_PASSWORD
}

# Опишите эту функцию…
def getLogConfig():
    global LOG_ENABLE, my_1C_DB_PATH, my_1C_PASSWORD, my_1C_LOGIN
    return LOG_ENABLE

# Опишите эту функцию…
def initConfig():
    global LOG_ENABLE, my_1C_DB_PATH, my_1C_PASSWORD, my_1C_LOGIN
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #4tm`|`A[MGz%1:)WqHA)
    my_1C_DB_PATH = ''

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #k~[X6QVj8.82(Prb2~4p
    my_1C_LOGIN = ''

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #3Zaor8ZqDr!j:a|GrxN4
    my_1C_PASSWORD = ''

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #`]ziu]FS1ezbOtf;ikv`
    LOG_ENABLE = True

    log_process(block_text='Присвоить значение переменной')


# Опишите эту функцию…
def setupConfig(data):
    global LOG_ENABLE, my_1C_DB_PATH, my_1C_PASSWORD, my_1C_LOGIN
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #a%+s2:YO40~l{HhI}4*/
    my_1C_DB_PATH = data['DBPathInput']

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #jg7,/WW_q+Q8U$B|^?Ua
    my_1C_LOGIN = data['loginInput']

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #/wzsuC#xiZ?RC=!cnuX{
    my_1C_PASSWORD = data['passwordInput']

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #!aiFi2*y$rioZ9g,eIeD
    LOG_ENABLE = data['logCheckbox']

    log_process(block_text='Присвоить значение переменной')



logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_Config_proc():
        global LOG_ENABLE, my_1C_DB_PATH, my_1C_PASSWORD, my_1C_LOGIN
        try:

            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_Config_proc()