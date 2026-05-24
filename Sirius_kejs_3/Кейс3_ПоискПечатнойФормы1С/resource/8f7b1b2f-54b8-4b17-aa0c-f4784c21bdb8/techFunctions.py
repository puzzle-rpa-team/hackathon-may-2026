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

import click_on_picture
import expect_screen_images
import files_and_folders

# generated
# Опишите эту функцию…
def ClosePromoWindow():

    log_process(window_log=True,block_text='Если – выполнить')
    #HtQ.MO%2n7}!`fXsY=+g
    if expect_screen_images.expect_screen_images((files_and_folders.get_executable_path('auth_window.png',binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),0.8,10,"FALSE",block_text="Ожидать изображение на экране",window_log=True, current_language="ru"):
        #m?V+jRXOjs#!XD1+Ius~
        click_on_picture.click_on_picture_2((files_and_folders.get_executable_path('close_btn.png',binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),0.8,0,"FALSE",block_text="Клик по картинке",window_log=True, current_language="ru")


    log_process(block_text='Если – выполнить')



logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_techFunctions_proc():
        try:

            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_techFunctions_proc()