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
from ConfigFunctions import LoadConfig
from ConfigFunctions import ValidateConfig
from ConfigFunctions import PrepareEnvironment
from relay_930 import Open1cAndLogIn
from relay_930 import SearchDocuments
from ProcessDocument import ProcessDocuments
from FinishProcess import FinishProcess

from web_automation_pydoll import init_web_automation_pydoll
import current_date_mod
import puzzle_logger
import stop_robot

# generated

logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_main_proc():
        try:
            log_process(window_log=True,block_text='Группировка блоков')
            # Начало работы
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #?xok*XG_u[O95qT#z4?3
            start_time = current_date_mod.current_date_mod('%d.%m.%Y %H:%M:%S',block_text="Получить текущую дату",window_log=True, current_language="ru")
            log_process(block_text='Присвоить значение переменной')
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #kyYTO^fvcw9*#pevq[A|
            success_count = 0
            log_process(block_text='Присвоить значение переменной')
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #.|eU`(;s;T:*ZyN}a^cd
            error_count = 0
            log_process(block_text='Присвоить значение переменной')
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #9O?MZi8|]Ge?dIvM`f#K
            report_rows = []
            log_process(block_text='Присвоить значение переменной')
            #y$d-~^[{~yR]dM!A%$9`
            puzzle_logger.write_log(puzzle_logger_path,('Робот начал работу ' + str(start_time)),log_level='info')
            

            log_process(block_text='Группировка блоков')

            log_process(window_log=True,block_text='Группировка блоков')
            # Загрузка конфигурации
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #y2%I60s)1#x+;t5@F5Sx
            config = LoadConfig()
            log_process(block_text='Присвоить значение переменной')
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #dG6,b8Fk_X?os`}?Fp7g
            valide_array = ValidateConfig(config)
            log_process(block_text='Присвоить значение переменной')
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #DWH4PUM-{.NuhnlCD;NV
            is_config_valid = valide_array['Config status']
            log_process(block_text='Присвоить значение переменной')
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #gODUC`9,K=N42A4@h;Ln
            error_message = valide_array['Error message']
            log_process(block_text='Присвоить значение переменной')
            log_process(window_log=True,block_text='Если – выполнить')
            #~#zO:z8K0mqz$I)d$jB)
            if is_config_valid != True:
                #$onNF/{rjgMbZ/gm^NQ1
                puzzle_logger.write_log(puzzle_logger_path,error_message,log_level='error')

                #Y*7LASr=aMP{OK`#7Q}J
                stop_robot.stop_robot(logger, log_message_end='Робот завершил работу',block_text="Завершить работу",window_log=True, current_language="ru")

            log_process(block_text='Если – выполнить')
            

            log_process(block_text='Группировка блоков')

            log_process(window_log=True,block_text='Группировка блоков')
            # Подготовка папок
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #7p|iJ6n4V1Y8Av0{se~6
            folder_dictionary = PrepareEnvironment(config)
            log_process(block_text='Присвоить значение переменной')
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #IRIRg#!{Nbh_[3qiqrwu
            report_path = folder_dictionary['Report path']
            log_process(block_text='Присвоить значение переменной')
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #bcFn-@L=,snVx_XRY/#w
            summary_path = folder_dictionary['Summary path']
            log_process(block_text='Присвоить значение переменной')
            

            log_process(block_text='Группировка блоков')

            log_process(window_log=True,block_text='Группировка блоков')
            # Создание сессии и вход в 1с
            # Присваивает переменной значение вставки
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #Mmt{K%GLA@,-{EF@^QBO
            web_actions = init_web_automation_pydoll(headless="FALSE",close="FALSE",extension_path=None,browser_type="google",user_profile=None,custom_user_agent="TRUE",block_text="Создать сессию браузера",window_log=True, current_language="ru")
            log_process(block_text='Присвоить значение переменной')
            log_process(window_log=True,block_text='Исполнить функцию')
            #R}6:bcAri(xf,]9=3aM_
            Open1cAndLogIn(config, web_actions)
            log_process(block_text='Исполнить функцию')
            

            log_process(block_text='Группировка блоков')

            log_process(window_log=True,block_text='Группировка блоков')
            # Получение списка документов
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #nzg!{3QG@vagRpyobvRM
            documents_list = SearchDocuments(config, web_actions)
            log_process(block_text='Присвоить значение переменной')
            

            log_process(block_text='Группировка блоков')

            log_process(window_log=True,block_text='Группировка блоков')
            # Обработка документов
            log_process(window_log=True,block_text='Цикл для каждого элемента')
            #FK,/S}`z:Pi#Af)/#W6W
            for document in documents_list:
                log_process(window_log=True,block_text='Исполнить функцию')
                #[_N.dXnMF*{6sBlfk%Yg
                ProcessDocuments(document, web_actions, config)

                log_process(block_text='Исполнить функцию')

            log_process(block_text='Цикл для каждого элемента')
            

            log_process(block_text='Группировка блоков')

            log_process(window_log=True,block_text='Группировка блоков')
            # Формирование отчета и завершение работы
            log_process(window_log=True,block_text='Исполнить функцию')
            #X5~~lIIWOskZy;0P/Bak
            FinishProcess()
            log_process(block_text='Исполнить функцию')
            

            log_process(block_text='Группировка блоков')


            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_main_proc()