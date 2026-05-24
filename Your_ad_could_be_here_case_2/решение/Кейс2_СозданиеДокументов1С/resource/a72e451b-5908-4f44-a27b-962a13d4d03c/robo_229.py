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
from Config import get1CConfig

import tools_for_1c

# generated
# Опишите эту функцию…
def my_1CCreateDocument(data):
    # Присваивает переменной значение вставки
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #UiR)ut|,g0^h!B72fyBY
    response = tools_for_1c.send_request_1c(request_type=3,db_login=((get1CConfig())['1C_LOGIN']),db_password=((get1CConfig())['1C_PASSWORD']),db_path=((get1CConfig())['1C_DB_PATH']),no_verify='FALSE',record_mode='write',object_for_write=(data['object']),uniq_id='',object_data=(data['data']),block_text="Отправить запрос в 1С",window_log=True, current_language="ru")

    log_process(block_text='Присвоить значение переменной')

    return response


logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_robo_229_proc():
        try:

            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_robo_229_proc()