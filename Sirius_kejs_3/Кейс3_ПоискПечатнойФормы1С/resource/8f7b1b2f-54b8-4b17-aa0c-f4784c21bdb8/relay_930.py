# !/usr/bin/python 
# -*- coding: utf8 -*- 
# Puzzle RPA version: 3.0.3 
# remote
def downRange(start, stop, step):

    while start >= stop:
        yield start
        start -= abs(step)
def upRange(start, stop, step):

    while start <= stop:
        yield start
        start += abs(step)
import sys

sys.dont_write_bytecode = True

# storage:
from puzzle_logger import configure_logger, log_process, send_message_websocket
from trace_utils import format_traceback
from pathlib import Path

import control_delay
import find_nth_occurrence
import find_numb
import puzzle_logger
import stop_robot

# generated
# Опишите эту функцию…
def Open1cAndLogIn(config, web_actions):
    #F]5a~0BOYx6)J/~=4M)/
    web_actions.open_url(url=(config['base_url']),new_tab="FALSE",block_text="Открыть страницу в браузере",window_log=True, current_language="ru")

    log_process(window_log=True,block_text='Если – выполнить')
    #Es#t|@?vn|N=cDRY8ay)
    if web_actions.wait_for_element(el_type='XPATH',el_xpath=(f"//*[@id=\"authWindow_basic_login\"]"),timeout=10,page_numb=0,block_text="Ожидать появление элемента",window_log=True, current_language="ru"):
        #+j}vZ3~`CK;HvZ#Vm}^b
        web_actions.input_to_browser(el_type='XPATH',el_xpath=(f"//*[@id=\"authWindow_basic_login\"]"),text='Команда7',interval=0,checked='TRUE',page_numb=0,block_text="Ввод в веб-сайт",window_log=True, current_language="ru")

    else:
        #xyA/e_NT0:}ym~@`k4Y[
        stop_robot.stop_robot(logger, log_message_end='Ошибка доступа к 1С',block_text="Завершить работу",window_log=True, current_language="ru")


    log_process(block_text='Если – выполнить')

    log_process(window_log=True,block_text='Если – выполнить')
    #WdJH=pl@KMb9`q@[,EC:
    if web_actions.wait_for_element(el_type='XPATH',el_xpath=(f"//*[@id=\"authWindow_basic_password\"]"),timeout=10,page_numb=0,block_text="Ожидать появление элемента",window_log=True, current_language="ru"):
        #~WP{caV0B-~dCjMlg5u|
        web_actions.input_to_browser(el_type='XPATH',el_xpath=(f"//*[@id=\"authWindow_basic_password\"]"),text='%vedbTeRqiNfct',interval=0,checked='TRUE',page_numb=0,block_text="Ввод в веб-сайт",window_log=True, current_language="ru")

    else:
        #/lsD_bI{*(94SWJ{!;P(
        stop_robot.stop_robot(logger, log_message_end='Ошибка доступа к 1С',block_text="Завершить работу",window_log=True, current_language="ru")


    log_process(block_text='Если – выполнить')

    log_process(window_log=True,block_text='Если – выполнить')
    #Nu@1_cjA|Se}s`WQxOW2
    if web_actions.check_enabled_element(el_type='XPATH',el_xpath=(f"//*[@id=\"authWindow_basic_okButton\"]"),page_numb=0,block_text="Доступен ли элемент",window_log=True, current_language="ru"):
        #OLUVagB+P#:oVP4lO/(I
        web_actions.click_element(el_type='XPATH',el_xpath=(f"//*[@id=\"authWindow_basic_okButton\"]"),double_click='FALSE',right_click='FALSE',page_numb=0,block_text="Клик по Web-элементу",window_log=True, current_language="ru")

    else:
        #s*WSyi`r|}K9jL:;qD;#
        stop_robot.stop_robot(logger, log_message_end='Ошибка доступа к 1С',block_text="Завершить работу",window_log=True, current_language="ru")


    log_process(block_text='Если – выполнить')

    #kHmZez;ESz.*q$9?HUIf
    control_delay.delay(20,block_text="Задержка",window_log=True, current_language="ru")

    #.I)U(^PT^Fg`]z7mW5Qw
    web_actions.button_click_1c(button_type=24,button_name='Закрыть',button_numb=1,page_numb=0,additional_value=None,block_text="Кликнуть по кнопке 1C-веб",window_log=True, current_language="ru")


# Опишите эту функцию…
def SearchDocuments(config, web_actions):
    log_process(window_log=True,block_text='Группировка блоков')
    # Получение настроек из конфига
    log_process(window_log=True,block_text='Обработка ошибки')
    try:
        log_process(window_log=True,block_text='Присвоить значение переменной')
        #):Ej2PEkBZzi5[55XWD~
        documents_list = []

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #dPOM~KJbM;{15:v@4`2X
        mode = config['mode']

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #k^+kqpM)-!xzBRQ!CtA?
        counterparty = (config['search_criteria'])['counterparty']

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #dZ*q[e!D(Et3J0KLI{l+
        organization = (config['search_criteria'])['organization']

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #SMKx/:#9]2qTE=a2vhXG
        document_type = config['document_type']

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #6s96YI~+0=WoV/|R%gC6
        link_document = 'e1cib/list/' + str(document_type)

        log_process(block_text='Присвоить значение переменной')

    
    except Exception as error_puzzle_1_0_3v:
        errors = find_numb.find_line_numb(error_puzzle_1_0_3v)
        #/kf.AV*Ux)ig|.Qc4%r8
        puzzle_logger.write_log(puzzle_logger_path,'Конфигурация заполнена с ошибками',log_level='error')

        #Wjtl(0Q_3aW7VPJ0ZYn[
        stop_robot.stop_robot(logger, log_message_end='Робот завершил работу',block_text="Завершить работу",window_log=True, current_language="ru")

    
    log_process(block_text='Обработка ошибки')
    

    log_process(block_text='Группировка блоков')

    log_process(window_log=True,block_text='Группировка блоков')
    # Открытие страницы с нужным типом документа и параметрами
    #lhtUE}?8;hQ02qrB%B+O
    # Взаимодействие с вкладкной 1С-веб
    web_actions.open_page_1c(event_type="open",conditions=(('http', link_document),),page_numb=0,block_text="Открыть/переключиться на страницу 1C-веб",window_log=True, current_language="ru")
    #L*x,%0MeDUsBPj4p)Fia
    web_actions.input_1c(input_field='Контрагент:',button_type=0,input_text=counterparty,field_numb=1,repeat_position=1,page_numb=0,block_text="Ввод в 1C-веб",window_log=True, current_language="ru")
    #K!Uw*VwCU*6eg4o:pT#{
    web_actions.input_1c(input_field='Организация:',button_type=0,input_text=organization,field_numb=1,repeat_position=1,page_numb=0,block_text="Ввод в 1C-веб",window_log=True, current_language="ru")
    
    #gOixv-QvV.:!jkgm5J6D
    control_delay.delay(5,block_text="Задержка",window_log=True, current_language="ru")
    

    log_process(block_text='Группировка блоков')

    log_process(window_log=True,block_text='Группировка блоков')
    # Извлечение данных
    # Присваивает переменной значение вставки
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #@P-gqH_9U`Tc$5U~U}dQ
    extracted_data = web_actions.extract_data(tag_name='div',attrs={
        'class': 'gridLine'
    },page_numb=0,block_text="Извлечь данные",window_log=True, current_language="ru")
    log_process(block_text='Присвоить значение переменной')
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #wr3J+SI8$h[#9gc]%2bH
    count_of_doc = 1
    log_process(block_text='Присвоить значение переменной')
    log_process(window_log=True,block_text='Если – выполнить')
    #UL=,x7Ue*4^OhD*LlexZ
    if len(extracted_data) == 1:
        #,#%O#A;WZGt%ur^)rfvz
        puzzle_logger.write_log(puzzle_logger_path,'Документы по заданным параметрам не найдены',log_level='error')

        #u_yul27}vvOV5;vVTpc`
        stop_robot.stop_robot(logger, log_message_end='Робот завершил работу',block_text="Завершить работу",window_log=True, current_language="ru")

    log_process(block_text='Если – выполнить')
    log_process(window_log=True,block_text='Если – выполнить')
    #pl2kJYAM6!X09Y!%lcNi
    if mode == 'all':
        log_process(window_log=True,block_text='Присвоить значение переменной')
        #t:Q7)4wUK#}5O7DVi:Z`
        count_of_doc = len(extracted_data) - 1

        log_process(block_text='Присвоить значение переменной')

    log_process(block_text='Если – выполнить')
    log_process(window_log=True,block_text='Цикл по (от до с шагом)')
    #r-Ru.(QNveNQP/TQ?pW^
    for i in (1 <= count_of_doc) and upRange(1, count_of_doc, 1) or downRange(1, count_of_doc, 1):
        log_process(window_log=True,block_text='Присвоить значение переменной')
        #,`beW7Ke!?;sOTsy8FPt
        end_index = (find_nth_occurrence.find_nth_occurrence((extracted_data[i]),1,counterparty,block_text="Получить N-ое вхождение подстроки в тексте",window_log=True, current_language="ru")) - 1

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #Q+1uZx+ylZh^{|5Fm4`!
        date_number = (extracted_data[i])[ : int(end_index + 1)]

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #}ea*4X9tn)MQg~x1LPv/
        document_date = date_number[ : 10]

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #:;V9w1$9y/NPB0iJeZ-D
        document_number = date_number[10 : ]

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Добавить элемент в список')
        #,XqqQ7ekZQ9u}F=]1}Um
        documents_list.append({
            'Document date': document_date,
            'Document number': document_number
        })

        log_process(block_text='Добавить элемент в список')

    log_process(block_text='Цикл по (от до с шагом)')
    #Ev7jy`z!FPAi@q|C_BS*
    puzzle_logger.write_log(puzzle_logger_path,(''.join([str(x) for x in ['Обработка документов закончена, сохранено', count_of_doc, 'документов']])),log_level='info')
    #r~jDP@Ke%fZ(4Vd#3/7,
    stop_robot.stop_robot(logger, log_message_end='Робот завершил работу',block_text="Завершить работу",window_log=True, current_language="ru")
    

    log_process(block_text='Группировка блоков')

    return documents_list


logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_relay_930_proc():
        try:

            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_relay_930_proc()