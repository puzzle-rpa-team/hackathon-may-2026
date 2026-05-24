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

from excel_tools import get_sheet_names_excel, read_from_excel
import data_io.json as data_io_json
import dataframe_pandas
import files_and_folders
import lists

# generated
# Опишите эту функцию…
def readExcel(path, listName):
    # Присваивает переменной значение вставки
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #C:-UQ}=~[_a6t=*ZuV;D
    fileContent = read_from_excel.read_from_excel(file=(files_and_folders.get_executable_path(path,binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),sheet=listName,just_data=False,dtype=None,block_text="Прочитать из Excel",window_log=True, current_language="ru")

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Исполнить функцию')
    #L6JfgD|uGsqRvpjUwz06
    log(f"Read Excel", f"success", ''.join([str(x) for x in [f"file:", path, f"; list:", listName]]))

    log_process(block_text='Исполнить функцию')

    return dataframe_pandas.df_to_json(orient="records",df=fileContent,block_text="Преобразовать DataFrame в словарь",window_log=True, current_language="ru")

# Опишите эту функцию…
def readFile(path):
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #vZVdl0B$GeznZhE:2Fn;
    splitedPath = lists.create_list_from_string(path,'.',block_text="Сделать список из текста",window_log=True, current_language="ru")

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #j)h{/V3a#:ozdOuZNh56
    splitedPath = splitedPath[-1]

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Присвоить значение переменной')
    #[8Zzj8TOle0Fk2BEc5ag
    fileContent = ''

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Если – выполнить')
    #DLgtb{Y6@G3~19Ip~V0`
    if splitedPath == (f"xlsx") or splitedPath == (f"csv"):
        # Присваивает переменной значение вставки
        log_process(window_log=True,block_text='Присвоить значение переменной')
        #q|GxYA00N+p$OF$dVMXZ
        sheet_names = get_sheet_names_excel.get_sheet_names_excel((files_and_folders.get_executable_path(path,binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),block_text="Получить список имен листов",window_log=True, current_language="ru")

        log_process(block_text='Присвоить значение переменной')

        log_process(window_log=True,block_text='Присвоить значение переменной')
        #nqeQq_{,IL1=79i{^I$M
        fileContent = readExcel(path, sheet_names[0])

        log_process(block_text='Присвоить значение переменной')

    elif splitedPath == (f"json"):
        log_process(window_log=True,block_text='Присвоить значение переменной')
        #4HDw][6@lMO#yubKBSt]
        fileContent = readJSON(path)

        log_process(block_text='Присвоить значение переменной')

    else:
        log_process(window_log=True,block_text='Исполнить функцию')
        #f|o}Nj4/Z~Yl@NmC-i-!
        log(f"Read file", f"error", str(f"incorrect file type:") + str(splitedPath))

        log_process(block_text='Исполнить функцию')


    log_process(block_text='Если – выполнить')

    return fileContent

# Опишите эту функцию…
def readJSON(path):
    # Присваивает переменной значение вставки
    log_process(window_log=True,block_text='Присвоить значение переменной')
    #M)7)b=Y:+A6~:dBI+]]8
    fileContent = data_io_json.read_json_file('utf-8',(files_and_folders.get_executable_path(path,binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),block_text="Прочитать файл",window_log=True, current_language="ru")

    log_process(block_text='Присвоить значение переменной')

    log_process(window_log=True,block_text='Исполнить функцию')
    #ugDRjvl?}V^fc`L(PxLu
    log(f"Read JSON", f"success", str(f"file:") + str(path))

    log_process(block_text='Исполнить функцию')

    return fileContent


logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_FIleReader_proc():
        try:

            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_FIleReader_proc()