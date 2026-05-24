# !/usr/bin/python 
# -*- coding: utf8 -*- 
# Puzzle RPA version: 3.0.3 
# remote
from numbers import Number
import sys

sys.dont_write_bytecode = True

# storage:
from puzzle_logger import configure_logger, log_process, send_message_websocket
from trace_utils import format_traceback
from pathlib import Path

from web_automation_2 import init_web_automation_selenium
import csv_tools
import data_io.json as data_io_json
import files_and_folders
import find_numb
import puzzle_logger

# generated

logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_main_proc():
        try:
            # Присваивает переменной значение вставки
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #_IJt|YG#]vxeUr`~;W{b
            documents = data_io_json.read_json_file('utf-8','C:\\Users\\Влад\\Desktop\\Кейс\\Kейс2_СозданиеДокументов1С\\resource\\orders.json',block_text="Прочитать файл",window_log=True, current_language="ru")

            log_process(block_text='Присвоить значение переменной')

            log_process(window_log=True,block_text='Присвоить значение переменной')
            #U*F#jXosHiE`~tE$eGNg
            ok_count = 0

            log_process(block_text='Присвоить значение переменной')

            log_process(window_log=True,block_text='Присвоить значение переменной')
            #-Fo]B$Q]:}F}Y.i^7KW,
            err_count = 0

            log_process(block_text='Присвоить значение переменной')

            #l/yqw@z%jrfcLF,b4+X0
            csv_tools.create_csv('C:\\Users\\Влад\\Desktop\\Кейс\\Kейс2_СозданиеДокументов1С\\resource\\result.csv',';','utf-8','НомерДокумента;Статус;Сообщение',block_text="Создать csv-файл",window_log=True, current_language="ru")

            # Присваивает переменной значение вставки
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #.rxyTv`$X2tZZ7^N`|Z1
            web = init_web_automation_selenium(headless="FALSE",close="FALSE",extension_path=None,browser_type="google",user_profile=None,custom_user_agent="TRUE",block_text="Создать сессию браузера",window_log=True, current_language="ru")

            log_process(block_text='Присвоить значение переменной')

            #(O{7q/?B*631KA/u44[N
            web.open_url(url='https://demo1c.mkskom.ru/puzzle_buh_corp_8.3',new_tab="FALSE",block_text="Открыть страницу в браузере",window_log=True, current_language="ru")

            #7+Z3/6M}vvejn0hs~f$b
            web.authorization_1c(login='Команда2',password='7Eqppr6kkpoGUw',timeout=120,page_numb=0,block_text="Авторизация в 1C-веб",window_log=True, current_language="ru")

            log_process(window_log=True,block_text='Цикл для каждого элемента')
            #8HByjTQ(w~{UNx)0[wjJ
            for doc in documents:
                log_process(window_log=True,block_text='Обработка ошибки')
                try:
                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #sEg$kiP^Lon0PojPIx|K
                    number = doc['number']

                    log_process(block_text='Присвоить значение переменной')

                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #rivld1rHtWe,FQ`UhcaR
                    date = doc['date']

                    log_process(block_text='Присвоить значение переменной')

                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #_{0waKUwY2/acrf;Sgcc
                    counterparty = doc['counterparty']

                    log_process(block_text='Присвоить значение переменной')

                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #6N#}Tq50Kk(ULZK^^C=S
                    req_list = []

                    log_process(block_text='Присвоить значение переменной')

                    log_process(window_log=True,block_text='Добавить элемент в список')
                    #4Feo![bf-e,i!j+FoGP-
                    req_list.append({
                        'ИмяРеквизита': 'Номер',
                        'ТипЗначения': 'Строка',
                        'ЗначениеРеквизита': '{number}'
                    })

                    log_process(block_text='Добавить элемент в список')

                    log_process(window_log=True,block_text='Добавить элемент в список')
                    #tH8q#7HBYr@p?{My^E~L
                    req_list.append({
                        'ИмяРеквизита': 'Дата',
                        'ТипЗначения': 'Дата',
                        'ЗначениеРеквизита': '{date}'
                    })

                    log_process(block_text='Добавить элемент в список')

                    log_process(window_log=True,block_text='Добавить элемент в список')
                    #pH*b}maF?eKBMd(HOq8T
                    req_list.append({
                        'ИмяРеквизита': 'Контрагент',
                        'ТипЗначения': 'Строка',
                        'ЗначениеРеквизита': '{counterparty}'
                    })

                    log_process(block_text='Добавить элемент в список')

                    log_process(window_log=True,block_text='Добавить элемент в список')
                    #c*%eH]{s7w]954pC?]NS
                    req_list.append({
                        'ИмяРеквизита': 'СуммаДокумента',
                        'ЗначениеРеквизита': '{summa}'
                    })

                    log_process(block_text='Добавить элемент в список')

                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #l==m0#|#J!aYpr;)Y,Vw
                    row_list = []

                    log_process(block_text='Присвоить значение переменной')

                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #-o}qzSDo}_]A,VM]H%#o
                    items = doc['items']

                    log_process(block_text='Присвоить значение переменной')

                    log_process(window_log=True,block_text='Цикл для каждого элемента')
                    #E3|j8MMij_zN[RgCBw_t
                    for it in items:
                        log_process(window_log=True,block_text='Присвоить значение переменной')
                        #K2Q/D;nW-8rf}dE.+`QZ
                        row = []

                        log_process(block_text='Присвоить значение переменной')

                        log_process(window_log=True,block_text='Присвоить значение переменной')
                        #qaOtF^1pUVB$xRjDk|db
                        prod = it['product']

                        log_process(block_text='Присвоить значение переменной')

                        log_process(window_log=True,block_text='Присвоить значение переменной')
                        #L8iX)*?4o`kBDXp2RV0y
                        qty = it['quantity']

                        log_process(block_text='Присвоить значение переменной')

                        log_process(window_log=True,block_text='Присвоить значение переменной')
                        #dFiva^iuY)X,8IV%Xe5.
                        price = it['price']

                        log_process(block_text='Присвоить значение переменной')

                        log_process(window_log=True,block_text='Присвоить значение переменной')
                        #l`{:2.`yha[JwV5d[O+/
                        rowsum = it['sum']

                        log_process(block_text='Присвоить значение переменной')

                        log_process(window_log=True,block_text='Добавить элемент в список')
                        #D^n[B{lw6}-Z-V)=EYo-
                        row.append({
                            'ИмяРеквизита': 'Номенклатура',
                            'ТипЗначения': 'Строка',
                            'ЗначениеРеквизита': prod
                        })

                        log_process(block_text='Добавить элемент в список')

                        log_process(window_log=True,block_text='Добавить элемент в список')
                        #BPXEVAUYiTFVvED4:7fl
                        row.append({
                            'ИмяРеквизита': 'Количество',
                            'ЗначениеРеквизита': qty
                        })

                        log_process(block_text='Добавить элемент в список')

                        log_process(window_log=True,block_text='Добавить элемент в список')
                        #f^-M2R4:)%Eez(mvX`Xa
                        row.append({
                            'ИмяРеквизита': 'Цена',
                            'ЗначениеРеквизита': price
                        })

                        log_process(block_text='Добавить элемент в список')

                        log_process(window_log=True,block_text='Добавить элемент в список')
                        #LgP{ym%1{3eVI|lE[Bgk
                        row.append({
                            'ИмяРеквизита': 'Сумма',
                            'ЗначениеРеквизита': rowsum
                        })

                        log_process(block_text='Добавить элемент в список')

                        log_process(window_log=True,block_text='Добавить элемент в список')
                        #UXmfI3KvK3q?|Q8hRWya
                        row_list.append(row)

                        log_process(block_text='Добавить элемент в список')

                        #Q=_UTE9L,a1lbJ#K/*?(
                        web.button_click_1c(button_type=9,button_name='Добавить',button_numb=1,page_numb=0,additional_value=None,block_text="Кликнуть по кнопке 1C-веб",window_log=True, current_language="ru")

                        #DAxtQbO@[qK;$iFJ?|3-
                        web.input_1c(input_field='Номенклатура',button_type=0,input_text='{prod}',field_numb=1,repeat_position=1,page_numb=0,block_text="Ввод в 1C-веб",window_log=True, current_language="ru")

                        #PH~5IK*MS?VI0_!u92`d
                        web.input_1c(input_field='Количество',button_type=0,input_text='{qty}',field_numb=1,repeat_position=1,page_numb=0,block_text="Ввод в 1C-веб",window_log=True, current_language="ru")

                        #.-T7kiznCp*m[Q7=EHXg
                        web.input_1c(input_field='Цена',button_type=0,input_text='{price}',field_numb=1,repeat_position=1,page_numb=0,block_text="Ввод в 1C-веб",window_log=True, current_language="ru")


                    log_process(block_text='Цикл для каждого элемента')

                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #Nh(Yrf#w:V}9sc#bx!Rv
                    tovary = {
                        'ИмяТабличнойЧасти': 'Товары',
                        'Данные': row_list
                    }

                    log_process(block_text='Присвоить значение переменной')

                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #aCL]iE^]rnghvJ+D3Z9|
                    tch_list = [tovary]

                    log_process(block_text='Присвоить значение переменной')

                    log_process(window_log=True,block_text='Присвоить значение переменной')
                    #j07}Iv0#RF,z*u+zkbti
                    data_payload = {
                        'Реквизиты': req_list,
                        'ТабличныеЧасти': tch_list
                    }

                    log_process(block_text='Присвоить значение переменной')

                    #_I1M!GrLD4!J!ueo|t%H
                    # Взаимодействие с вкладкной 1С-веб
                    web.open_page_1c(event_type="open",conditions=(('http', 'e1cib/list/Документ.СчетНаОплатуПокупателю'),),page_numb=0,block_text="Открыть/переключиться на страницу 1C-веб",window_log=True, current_language="ru")
                    

                    #34i=NE[Sg,e0os%jL2uE
                    web.button_click_1c(button_type=7,button_name='Создать',button_numb=1,page_numb=0,additional_value=None,block_text="Кликнуть по кнопке 1C-веб",window_log=True, current_language="ru")

                    #q=BIZm*:}.!bn84*wkku
                    web.input_1c(input_field='Контрагент:',button_type=0,input_text=(f"{counterparty}"),field_numb=1,repeat_position=1,page_numb=0,block_text="Ввод в 1C-веб",window_log=True, current_language="ru")

                    #e9W64]ggt.7IT`?[)IhN
                    web.input_1c(input_field='Организация:',button_type=0,input_text=(f"{counterparty}"),field_numb=1,repeat_position=1,page_numb=0,block_text="Ввод в 1C-веб",window_log=True, current_language="ru")

                    #{E=vsDF:8+-bW`=3_*^4
                    web.input_1c(input_field='Договор:',button_type=0,input_text=(f"{counterparty}"),field_numb=1,repeat_position=1,page_numb=0,block_text="Ввод в 1C-веб",window_log=True, current_language="ru")

                    #GSm%iu:HjajqXuWswgHu
                    web.input_1c(input_field='Договор:',button_type=0,input_text=(f"{counterparty}"),field_numb=1,repeat_position=1,page_numb=0,block_text="Ввод в 1C-веб",window_log=True, current_language="ru")

                    #l*C![n-F,i4|n?+T6Osy
                    web.button_click_1c(button_type=26,button_name='Провести и закрыть',button_numb=1,page_numb=0,additional_value=None,block_text="Кликнуть по кнопке 1C-веб",window_log=True, current_language="ru")

                    log_process(window_log=True,block_text='Увеличить значение переменной')
                    #]TN?/1:p4^`-k#h{RpCl
                    ok_count = (ok_count if isinstance(ok_count, Number) else 0) + 1

                    log_process(block_text='Увеличить значение переменной')

                    #HN=!uI`)C_BZ9M0/xQ(_
                    puzzle_logger.write_log(puzzle_logger_path,(f"Создан документ № {number}"),log_level='info')

                    #EDH!-9=sGd(vIb3.gr?M
                    files_and_folders.append_txt_file(file_path='C:\\Users\\Влад\\Desktop\\Кейс\\Kейс2_СозданиеДокументов1С\\resource\\result.csv', data=(f"{number};Успех;"), encoding='utf-8',block_text="Дописать в файл",window_log=True, current_language="ru")

                
                except Exception as error_puzzle_1_0_3v:
                    error_description = find_numb.find_line_numb(error_puzzle_1_0_3v)
                    log_process(window_log=True,block_text='Увеличить значение переменной')
                    #RQ+[soXLBHD1eIry-~-=
                    err_count = (err_count if isinstance(err_count, Number) else 0) + 1

                    log_process(block_text='Увеличить значение переменной')

                    #ws7R@n1::(t5~p9}kXy/
                    puzzle_logger.write_log(puzzle_logger_path,(f"Ошибка документа № {number}: {error_description}"),log_level='error')

                    #H.*}X7~Jmqzy:VA:)3I_
                    files_and_folders.append_txt_file(file_path='C:\\Users\\Влад\\Desktop\\Кейс\\Kейс2_СозданиеДокументов1С\\resource\\result.csv', data=(f"{number};Ошибка;{error_description}\n"), encoding='utf-8',block_text="Дописать в файл",window_log=True, current_language="ru")

                

                log_process(block_text='Обработка ошибки')


            log_process(block_text='Цикл для каждого элемента')

            #rh#)E?X}MxvfCZK|bD}C
            puzzle_logger.write_log(puzzle_logger_path,(f"Обработка завершена. Успешно: {ok_count}, ошибок: {err_count}"),log_level='info')


            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_main_proc()