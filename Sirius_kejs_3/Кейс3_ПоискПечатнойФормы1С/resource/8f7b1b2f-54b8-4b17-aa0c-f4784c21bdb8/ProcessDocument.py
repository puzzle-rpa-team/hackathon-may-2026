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

import control_delay
import files_and_folders
import find_numb
import puzzle_logger
import user_notice_2
import web_download_file

# generated
# Опишите эту функцию…
def GenerateFileName(config, document_number, document_date):
    log_process(window_log=True,block_text='Обработка ошибки')
    try:
        log_process(window_log=True,block_text='Присвоить значение переменной')
        #vx+=9~o(A/C)J[Rg^Z_5
        file_name = ''.join([str(x) for x in [config['output_path'], '/', 'документ_.pdf', document_number, '_', document_date, '.', config['document_format']]])

        log_process(block_text='Присвоить значение переменной')

        #BJrxsvCXFck+v$JvON$b
        puzzle_logger.write_log(puzzle_logger_path,('Имя файла успешно сгенерировано для документа' + str(document_number)),log_level='info')

    
    except Exception as error_puzzle_1_0_3v:
        error_description = find_numb.find_line_numb(error_puzzle_1_0_3v)
        #k=lv3CM0Nwv_5)VcIB^@
        puzzle_logger.write_log(puzzle_logger_path,(''.join([str(x2) for x2 in ['Ошибка генерации имени файла для документа', document_number, 'Будет использован стандартный шаблон']])),log_level='warning')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #w3$~$tg)daYSwXQ`AzIE
        file_name = 'Печатная форма документа.pdf'

        log_process(block_text='Присвоить значение переменной')

    

    log_process(block_text='Обработка ошибки')

    return file_name

# Опишите эту функцию…
def GetPrintForm(document_number, document_date, config, web_actions):
    log_process(window_log=True,block_text='Обработка ошибки')
    try:
        #I+1g:g9pEuFr$Hf:yPnn
        web_actions.button_click_1c(button_type=0,button_name='Печать',button_numb=1,page_numb=0,additional_value=None,block_text="Кликнуть по кнопке 1C-веб",window_log=True, current_language="ru")

        #?Q^((z~Z)z;n+}I83(tv
        web_actions.button_click_1c(button_type=0,button_name='Счет покупателю',button_numb=1,page_numb=0,additional_value=None,block_text="Кликнуть по кнопке 1C-веб",window_log=True, current_language="ru")

        log_process(window_log=True,block_text='Если – выполнить')
        #.+6W(q^DYHL;tYvyNyG;
        if web_actions.check_exists_element(el_type='XPATH',el_xpath=(f"//*[@id=\"form7_КнопкаПечатьКоманднаяПанель\"]"),page_numb=0,block_text="Существует ли элемент",window_log=True, current_language="ru"):
            #Yd?IA57q(m;!d2R73qS*
            web_actions.click_element(el_type='XPATH',el_xpath=(f"//*[@id=\"form7_КнопкаПечатьКоманднаяПанель\"]"),double_click='FALSE',right_click='FALSE',page_numb=0,block_text="Клик по Web-элементу",window_log=True, current_language="ru")

            #RW23Xq02EtT7~J{z,*ye
            control_delay.delay(10,block_text="Задержка",window_log=True, current_language="ru")

        else:
            #MJSYhN!D#,ErBwFd4QrC
            puzzle_logger.write_log(puzzle_logger_path,'Ошибка получения печатной формы',log_level='error')


        log_process(block_text='Если – выполнить')

        #7*q-!0OnuHp,W18#]qT/
        control_delay.delay(10,block_text="Задержка",window_log=True, current_language="ru")

    
    except Exception as error_puzzle_1_0_3v:
        error_description = find_numb.find_line_numb(error_puzzle_1_0_3v)
        #uv5:~TU;R~+G(3G5M`nO
        puzzle_logger.write_log(puzzle_logger_path,'Ошибка получения печатной формы',log_level='error')

    

    log_process(block_text='Обработка ошибки')


# Опишите эту функцию…
def ProcessDocuments(document, web_actions, config):
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #-r2b8lWjH%?37Q`/vNq0
    document_number = document['Document number']

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #Hup!Arrup^mcuxTE;Azp
    document_date = document['Document date']

    log_process(block_text='Присвоить значение переменной')

    #ZKNrQv]-)*qNSYa^S=)w
    # Взаимодействие с вкладкной 1С-веб
    web_actions.open_page_1c(event_type="open",conditions=(('http', document_number),),page_numb=0,block_text="Открыть/переключиться на страницу 1C-веб",window_log=True, current_language="ru")
    log_process(window_log=True,block_text='Исполнить функцию')
    #MsSh.)?]hwv9N$CLpN-]
    GetPrintForm(document_number, document_date, config, web_actions)
    log_process(block_text='Исполнить функцию')
    log_process(window_log=True,block_text='Исполнить функцию')
    #ZdS$3gs:z#^3N@4EeVy;
    SavePrintForm(config, document_number, document_date)
    log_process(block_text='Исполнить функцию')
    #DNoGT);BC34.idc7j4LD
    puzzle_logger.write_log(puzzle_logger_path,('Успешное сохранение формы для документа' + str(document_number)),log_level='info')
    #_dQY-7I=NYEmNKB+;8nm
    web_actions.close_tab(page_numb=1,block_text="Закрыть вкладку браузера",window_log=True, current_language="ru")
    
    
    


# Опишите эту функцию…
def SavePrintForm(config, document_number, document_date):
    log_process(window_log=True,block_text='Обработка ошибки')
    try:
        # Присваивает переменной значение вставки
        log_process(window_log=True,block_text='Присвоить значение переменной')
        #G03eBewt~28YcKYc3O4U
        tab_info = web_actions.get_current_tab_info(return_type="url",block_text="Получить информацию о текущей вкладке",window_log=True, current_language="ru")

        log_process(block_text='Присвоить значение переменной')

        #Z1X{xItW|Mno1!#;w|kp
        user_notice_2.user_notice((str(tab_info) + '     '),None,block_text="Уведомление пользователя",window_log=True, current_language="ru")

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #?)Q`2[YV.H1+IG2AHPUB
        file_name = GenerateFileName(config, document_number, document_date)

        log_process(block_text='Присвоить значение переменной')

        #D}hPK=J5DT-~[/3nzx/c
        web_download_file.web_download_file_2(tab_info,(files_and_folders.get_executable_path(file_name,binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),"FALSE",block_text="Скачать файл",window_log=True, current_language="ru")

    
    except Exception as error_puzzle_1_0_3v:
        error_description = find_numb.find_line_numb(error_puzzle_1_0_3v)
        #WN]]MOaeEQPeDGG,y*jJ
        puzzle_logger.write_log(puzzle_logger_path,'Ошибка сохранения печатной формы',log_level='error')

    

    log_process(block_text='Обработка ошибки')



logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_ProcessDocument_proc():
        try:

            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_ProcessDocument_proc()