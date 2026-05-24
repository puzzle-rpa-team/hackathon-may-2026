# !/usr/bin/python 
# -*- coding: utf8 -*- 
# Puzzle RPA version: 3.0.3 
# remote
import os
import sys

sys.dont_write_bytecode = True

# storage:
from puzzle_logger import configure_logger, log_process, send_message_websocket
from trace_utils import format_traceback
from pathlib import Path

import data_io.json as data_io_json
import files_and_folders
import find_nth_occurrence
import find_numb
import puzzle_logger
import sootv_str
import stop_robot

# generated
# Опишите эту функцию…
def LoadConfig():
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #57tDH;LOA:pa#T@e|k7n
    config = []

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Обработка ошибки')
    try:
        # Присваивает переменной значение вставки
        log_process(window_log=True,block_text='Присвоить значение переменной')
        #7.|k$z+erA_$?-}d+Z$A
        config = data_io_json.read_json_file('utf-8',(files_and_folders.get_executable_path('config.json',binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),block_text="Прочитать файл",window_log=True, current_language="ru")

        log_process(block_text='Присвоить значение переменной')

    
    except Exception as error_puzzle_1_0_3v:
        error_description = find_numb.find_line_numb(error_puzzle_1_0_3v)
        #$onNF/{rjgMbZ/gm^NQ1
        puzzle_logger.write_log(puzzle_logger_path,'Ошибка чтения JSON конфигурации  ',log_level='error')

        #](n70b!?2iQmcyQXkPmj
        stop_robot.stop_robot(logger, log_message_end='Робот завершил работу',block_text="Завершить работу",window_log=True, current_language="ru")

    

    log_process(block_text='Обработка ошибки')

    return config

# Опишите эту функцию…
def PrepareEnvironment(config):
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #y}_N`9~=Lu~o3::C{Tu;
    print_form_path = config['output_path']

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #Gvg~cIjv5$BixUS@P3Nd
    result_print_form_path = print_form_path[int(find_nth_occurrence.find_first_occurrence(print_form_path,'/',block_text="Получить первое вхождение подстроки в тексте",window_log=True, current_language="ru")) : ]

    log_process(block_text='Присвоить значение переменной')

    #Y;mG2X,:B@/Hv[:*qlHy
    files_and_folders.create_folder((files_and_folders.get_executable_path('',binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),result_print_form_path,block_text="Создать папку",window_log=True, current_language="ru")

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #D/5NRufMhoS,~@^}4L*]
    report_path = 'resource/report.csv'

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #EL!G}q_w]Fd6Hf(Uo}dL
    summary_path = 'resource/summary.txt'

    log_process(block_text='Присвоить значение переменной')

    #y$d-~^[{~yR]dM!A%$9`
    puzzle_logger.write_log(puzzle_logger_path,'Папки подготовлены',log_level='info')

    return {
    'Report path': report_path,
    'Summary path': summary_path
}

# Опишите эту функцию…
def ValidateConfig(config):
    log_process(window_log=True,block_text='Если – выполнить')
    #8ab*J]MG=h|4,2u6Ihh^
    if (config['document_type']) == '':
        log_process(window_log=True,block_text='Присвоить значение переменной')
        #tVA!-K(xz3FrOM#+}5MC
        is_config_valid = False

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #w(_W*4Q;W`]u@7M]yFD)
        error_message = 'В конфигурации отсутствует document_type'

        log_process(block_text='Присвоить значение переменной')

    else:
        log_process(window_log=True,block_text='Если – выполнить')
        #@D#1,4WPk],wGoYa%p]s
        if (config['mode']) != 'first_only' and (config['mode']) != 'all':
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #z[m3d%*F]=vWvYBXE?YD
            is_config_valid = False

            log_process(block_text='Присвоить значение переменной')

            log_process(window_log=True,block_text='Присвоить значение переменной')
            #V0MgCP~,=T[ip`R#je)=
            error_message = 'В конфигурации отсутствует mode'

            log_process(block_text='Присвоить значение переменной')

        else:
            log_process(window_log=True,block_text='Если – выполнить')
            #d{/~+g(i2$h86/bK`Y.C
            if (config['output_path']) == '':
                log_process(window_log=True,block_text='Присвоить значение переменной')
                ##r#5SYdTyKT=yfTM2^dj
                is_config_valid = False

                log_process(block_text='Присвоить значение переменной')

                log_process(window_log=True,block_text='Присвоить значение переменной')
                #cHCe`#n*oUu,W`k(UsPC
                error_message = 'В конфигурации отсутствует output_path'

                log_process(block_text='Присвоить значение переменной')

            else:
                log_process(window_log=True,block_text='Присвоить значение переменной')
                #pG17*%#%le=Q~8RVT:jY
                forbidden = [':', '*', '?', '>', '<', '|', '"', '\\']

                log_process(block_text='Присвоить значение переменной')

                log_process(window_log=True,block_text='Присвоить значение переменной')
                #So:QvTDF!#8UF*_{E(~p
                has_forbidden = False

                log_process(block_text='Присвоить значение переменной')

                log_process(window_log=True,block_text='Цикл для каждого элемента')
                #SK!xX,^aB?,Nto*8lL7a
                for j in forbidden:
                    log_process(window_log=True,block_text='Если – выполнить')
                    #oJ*aVqX-sdGn|F+!n:@3
                    if sootv_str.sootv_str((config['output_path']),j,block_text="Содержит ли строка подстроку",window_log=True, current_language="ru"):
                        log_process(window_log=True,block_text='Присвоить значение переменной')
                        #NSc~rz}gN.?:2oD8YWD5
                        has_forbidden = True

                        log_process(block_text='Присвоить значение переменной')


                    log_process(block_text='Если – выполнить')


                log_process(block_text='Цикл для каждого элемента')

                log_process(window_log=True,block_text='Если – выполнить')
                #Gcvi-;y+KF!+,mWs5rLl
                if has_forbidden == True:
                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #S.y#]X.0xtCsUGvOhS=d
                    is_config_valid = False

                    log_process(block_text='Присвоить значение переменной')

                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #43LLL[-El-6FALrPhq/v
                    error_message = 'output_path содержит недопустимый символ'

                    log_process(block_text='Присвоить значение переменной')

                else:
                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #2SY]*|+lBgD37)Q@]FV~
                    is_config_valid = True

                    log_process(block_text='Присвоить значение переменной')

                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #%JU;$a[H?d3?=5Q|VtRf
                    error_message = 'Конфигурация корректна'

                    log_process(block_text='Присвоить значение переменной')


                log_process(block_text='Если – выполнить')


            log_process(block_text='Если – выполнить')


        log_process(block_text='Если – выполнить')


    log_process(block_text='Если – выполнить')

    return {
    'Config status': is_config_valid,
    'Error message': error_message
}


logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_ConfigFunctions_proc():
        try:

            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_ConfigFunctions_proc()