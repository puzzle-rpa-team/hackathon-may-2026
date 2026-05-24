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
from Config import initConfig
from Logger import initLogger
from FormHandler import showForm
from FIleReader import readFile
from Logger import log

from web_automation_pydoll import init_web_automation_pydoll
import click_on_picture
import control_delay
import expect_screen_images
import files_and_folders
import user_notice_2

# generated

logger = configure_logger()
puzzle_logger_path = Path(__file__).absolute()
logger.info(f'Старт робота: {puzzle_logger_path}')

if __name__ == "__main__":
    def main_Main_proc():
        try:
            # Присваивает переменной значение вставки
            log_process(window_log=True,block_text='Присвоить значение переменной')
            #K!:06n#,qGjjluk?.N6p
            web_actions = init_web_automation_pydoll(headless="FALSE",close="FALSE",extension_path=None,browser_type="google",user_profile=None,custom_user_agent="TRUE",block_text="Создать сессию браузера",window_log=True, current_language="ru")

            log_process(block_text='Присвоить значение переменной')

            log_process(window_log=True,block_text='Группировка блоков')
            # Группировка блоков
            #hB2*.T/YGQxh~aWIT!Tk
            web_actions.open_url(url='https://demo1c.mkskom.ru/puzzle_buh_corp_8.3',new_tab="FALSE",block_text="Открыть страницу в браузере",window_log=True, current_language="ru")
            #_YDpHTk0:$+sQ#GoAky%
            web_actions.input_to_browser(el_type='XPATH',el_xpath=(f"//*[@id=\"authWindow_basic_login\"]"),text='Команда4',interval=50,checked='TRUE',page_numb=0,block_text="Ввод в веб-сайт",window_log=True, current_language="ru")
            #5QqsuE+R~b~.GU1ZaIX.
            control_delay.delay(0.5,block_text="Задержка",window_log=True, current_language="ru")
            #LWb%P@[,6=@A?bo]$x/M
            web_actions.input_to_browser(el_type='XPATH',el_xpath=(f"//*[@id=\"authWindow_basic_password\"]"),text='!n%PAbfub3y!N4',interval=50,checked='TRUE',page_numb=0,block_text="Ввод в веб-сайт",window_log=True, current_language="ru")
            #/,f`JNDK+7Dfwm5v^F}-
            control_delay.delay(0.5,block_text="Задержка",window_log=True, current_language="ru")
            #bx-@Khg$K={p+#,:X].h
            web_actions.click_element(el_type='XPATH',el_xpath=(f"//*[@id=\"authWindow_basic_okButton\"]"),double_click='FALSE',right_click='FALSE',page_numb=0,block_text="Клик по Web-элементу",window_log=True, current_language="ru")
            log_process(window_log=True,block_text='Если – выполнить')
            #@xAZI|B2]`I^0|Cv+;Nz
            if expect_screen_images.expect_screen_images((files_and_folders.get_executable_path('mvsrc/google_pass_close_btn.png',binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),0.8,8,"FALSE",block_text="Ожидать изображение на экране",window_log=True, current_language="ru"):
                #oP2dQ=D69]PI%w0;^UK2
                click_on_picture.click_on_picture_2((files_and_folders.get_executable_path('mvsrc/google_pass_close_btn.png',binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),0.8,0,"FALSE",block_text="Клик по картинке",window_log=True, current_language="ru")

            log_process(block_text='Если – выполнить')
            log_process(window_log=True,block_text='Если – выполнить')
            #gL88E7O~1Ln%DV39K9LG
            if expect_screen_images.expect_screen_images((files_and_folders.get_executable_path('mvsrc/1с_ready_window.png',binary_path='TRUE',block_text="Относительный путь",window_log=True, current_language="ru")),0.8,40,"FALSE",block_text="Ожидать изображение на экране",window_log=True, current_language="ru"):
                #VuPpCbT9Dj+CFGzJEESf
                web_actions.button_click_1c(button_type=1,button_name='Продажи',button_numb=1,page_numb=0,additional_value='Счета покупателям',block_text="Кликнуть по кнопке 1C-веб",window_log=True, current_language="ru")

                #?rB*BC)JTi`#peQ9zIP$
                control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                #[AmO:TdbVjIu*9(@(dQ-
                web_actions.click_element(el_type='XPATH',el_xpath=(f"//*[@id=\"form5_ФормаСоздать\"]"),double_click='FALSE',right_click='FALSE',page_numb=0,block_text="Клик по Web-элементу",window_log=True, current_language="ru")

                #r1ddRIZ[_`%:gWEkO?1@
                control_delay.delay(5,block_text="Задержка",window_log=True, current_language="ru")

                #9a)gp[!klgMkOAJ%u|jL
                web_actions.input_to_browser(el_type='XPATH',el_xpath=(f"//*[contains(@id, \"_Контрагент_i0\")]"),text='Кафе "Аполлон"',interval=50,checked='TRUE',page_numb=0,block_text="Ввод в веб-сайт",window_log=True, current_language="ru")

                #8N,;wx:4:rRF-Kno5kc2
                control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                #jY^tc$L77L9vliq^OY-^
                web_actions.hot_keys_2(el_type="active_element",el_xpath=(f""),keys='Enter',page_numb=0,checked="FALSE",block_text="Ввод горячих клавиш в веб-сайт",window_log=True, current_language="ru")

                #e^}!lkHtFh5[Un5i4hRL
                control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                #-IQXH0)qElW=}-v-?4rb
                web_actions.input_to_browser(el_type='XPATH',el_xpath=(f"//*[@id=\"form6_Организация_i0\"]"),text='Магазин №23',interval=50,checked='TRUE',page_numb=0,block_text="Ввод в веб-сайт",window_log=True, current_language="ru")

                #5rMg9JU4UZr4PaEam;bg
                control_delay.delay(3,block_text="Задержка",window_log=True, current_language="ru")

                #i6sT328d$CweniZ7ZZ13
                web_actions.hot_keys_2(el_type="active_element",el_xpath=(f""),keys='Enter',page_numb=0,checked="FALSE",block_text="Ввод горячих клавиш в веб-сайт",window_log=True, current_language="ru")

                #A/G,hbfy{3x$VqLZHD(G
                control_delay.delay(3,block_text="Задержка",window_log=True, current_language="ru")

                log_process(window_log=True,block_text='Цикл повторить n-раз')
                #|hS`|=D,OD4CJGqTLbE1
                for count in range(2):
                    #._kb2x]1p=KLKc!l.~il
                    web_actions.click_element(el_type='XPATH',el_xpath=(f"//*[@id=\"form6_ТоварыДобавить\"]"),double_click='FALSE',right_click='FALSE',page_numb=0,block_text="Клик по Web-элементу",window_log=True, current_language="ru")

                    #C`H;%2ti07[b99anE*mZ
                    control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                    #DBdb2q_K.Zy-mkxU@SKx
                    web_actions.input_to_browser(el_type='XPATH',el_xpath=(f"//*[@id=\"form6_ТоварыНоменклатураИнтерактивная_i0\"]"),text='Печенье шоколадное',interval=50,checked='TRUE',page_numb=0,block_text="Ввод в веб-сайт",window_log=True, current_language="ru")

                    #ac)@ne^-9#]Nr{^MT(gq
                    control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                    #vije0q;S=L~sJyxcIi7o
                    web_actions.hot_keys_2(el_type="active_element",el_xpath=(f""),keys='Enter',page_numb=0,checked="FALSE",block_text="Ввод горячих клавиш в веб-сайт",window_log=True, current_language="ru")

                    #s:y:.NufWd96?4[Z|20B
                    control_delay.delay(3,block_text="Задержка",window_log=True, current_language="ru")

                    #e)*Q^vIKL^lW|HXfMO+p
                    web_actions.click_element(el_type='XPATH',el_xpath=(f"//*[@id=\"form6_ТоварыКоличество_i0\"]"),double_click='TRUE',right_click='FALSE',page_numb=0,block_text="Клик по Web-элементу",window_log=True, current_language="ru")

                    #zSHj#x#J,LRd~?Slo-V1
                    control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                    #qctQ$_z-,e3rX5cU*D25
                    web_actions.input_to_browser(el_type='XPATH',el_xpath=(f"//*[@id=\"form6_ТоварыКоличество_i0\"]"),text='100',interval=50,checked='TRUE',page_numb=0,block_text="Ввод в веб-сайт",window_log=True, current_language="ru")

                    #Al=3!iL)G178wyKlPc-[
                    control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                    #AG1+A:h)_V/E?T%p0UYy
                    web_actions.hot_keys_2(el_type="active_element",el_xpath=(f""),keys='Enter',page_numb=0,checked="FALSE",block_text="Ввод горячих клавиш в веб-сайт",window_log=True, current_language="ru")

                    #v_B%;_98l%7~.z$k.[U(
                    control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                    #bSH8y6Su4JM$_g{Nf/T~
                    web_actions.click_element(el_type='XPATH',el_xpath=(f"//*[@id=\"form6_ТоварыЦена_i0\"]"),double_click='FALSE',right_click='FALSE',page_numb=0,block_text="Клик по Web-элементу",window_log=True, current_language="ru")

                    #aUZhuAsTV[R$CYmKu9_a
                    control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                    #!@?eiMRzpM=f(1K*/~o`
                    web_actions.input_to_browser(el_type='XPATH',el_xpath=(f"//*[@id=\"form6_ТоварыЦена_i0\"]"),text='120',interval=50,checked='TRUE',page_numb=0,block_text="Ввод в веб-сайт",window_log=True, current_language="ru")

                    #5iZb]LAcqBZ=C/_kDiz6
                    control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                    #za#h7vBb.BOkMgi!C#rJ
                    web_actions.hot_keys_2(el_type="active_element",el_xpath=(f""),keys='Enter',page_numb=0,checked="FALSE",block_text="Ввод горячих клавиш в веб-сайт",window_log=True, current_language="ru")

                    #`gc;DXHftwAl{/rq-izB
                    control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                    #83A4:R7Drg!gse23[~2c
                    web_actions.hot_keys_2(el_type="active_element",el_xpath=(f""),keys='Insert',page_numb=0,checked="FALSE",block_text="Ввод горячих клавиш в веб-сайт",window_log=True, current_language="ru")


                log_process(block_text='Цикл повторить n-раз')

                #yzgM=VP%-#7x.xW_/{J8
                control_delay.delay(2,block_text="Задержка",window_log=True, current_language="ru")

                #oFnry0L0xC?[N$1V_5b+
                web_actions.hot_keys_2(el_type="active_element",el_xpath=(f""),keys='Ctrl + s',page_numb=0,checked="FALSE",block_text="Ввод горячих клавиш в веб-сайт",window_log=True, current_language="ru")

            log_process(block_text='Если – выполнить')
            #,0ju2R?97J.J1Ev:H=wU
            user_notice_2.user_notice('end',None,block_text="Уведомление пользователя",window_log=True, current_language="ru")
            

            log_process(block_text='Группировка блоков')


            logger.info(f'Завершение работы робота: {puzzle_logger_path}')
            send_message_websocket(message_type="python_end")
        except Exception as error_puzzle:
            logger.error(f'{puzzle_logger_path} ' + f'Ошибка: {error_puzzle}')
            error_puzzle_format=format_traceback(error_puzzle)
            send_message_websocket(message_type="python_error", message=error_puzzle_format)
            raise Exception(error_puzzle)
    main_Main_proc()