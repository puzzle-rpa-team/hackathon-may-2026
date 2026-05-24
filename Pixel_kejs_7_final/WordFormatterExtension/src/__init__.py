import os
import re
import json
import time
import subprocess
import win32com.client as win32
from puzzle_logger import log_decorator, window_logger

@window_logger
@log_decorator

def replace_placeholders_manually(doc, placeholders_dict):
    # Ручная замена плейсхолдеров в каждом абзаце
    for para in doc.Paragraphs:
        text = para.Range.Text
        changed = False
        
        for placeholder, value in placeholders_dict.items():
            if placeholder in text:
                text = text.replace(placeholder, str(value))
                changed = True
        
        if changed:
            para.Range.Text = text

def format_document(source_path, output_path, font_name, font_size, placeholders, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    # Основная функция форматирования Word документа
    
    # Обработка значений по умолчанию
    if not source_path:
        raise ValueError("Не указан путь к исходному файлу")
    
    if not output_path:
        output_path = source_path
    
    if not font_name:
        font_name = "Times New Roman"
    
    if not font_size:
        font_size = 14
    
    # Преобразование плейсхолдеров
    placeholders_dict = {}
    if placeholders:
        if isinstance(placeholders, dict):
            placeholders_dict = placeholders
        elif isinstance(placeholders, str):
            try:
                placeholders_dict = json.loads(placeholders)
            except:
                # Простой формат: {{user_name}}: Баранова Софья
                parts = placeholders.split(',')
                for part in parts:
                    if ':' in part:
                        key, val = part.split(':', 1)
                        key = key.strip().strip('"\'{}')
                        val = val.strip().strip('"\'')
                        placeholders_dict[key] = val
    
    # Проверка, что файл существовует
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Файл не найден: {source_path}")
    
    # Создание папки для сохранения
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Работа с Word
    word = None
    doc = None
    
    try:
        # Подключение к Word
        word = win32.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False
        
        # Открытие документа
        doc = word.Documents.Open(source_path)
        
        # Замена плейсхолдеров
        if placeholders_dict:
            for para in doc.Paragraphs:
                text = para.Range.Text
                changed = False
        
                for placeholder, value in placeholders_dict.items():
                    if placeholder in text:
                        text = text.replace(placeholder, str(value))
                        changed = True
        
                if changed:
                    para.Range.Text = text
        
        # Удаление пустых абзацев
        # Удаляем 3 и более пустых строк подряд
        for _ in range(10):
            find_obj = doc.Content.Find
            find_obj.ClearFormatting()
            find_obj.Text = "^p^p^p"
            find_obj.Replacement.ClearFormatting()
            find_obj.Replacement.Text = "^p^p"
            if not find_obj.Execute(Replace=2):
                break
        
        # Удаляем 2 пустых строки подряд
        for _ in range(10):
            find_obj = doc.Content.Find
            find_obj.ClearFormatting()
            find_obj.Text = "^p^p"
            find_obj.Replacement.ClearFormatting()
            find_obj.Replacement.Text = "^p"
            if not find_obj.Execute(Replace=2):
                break
        
        # Удаляем абзацы, которые содержат только пробелы
        for para in doc.Paragraphs:
            text = para.Range.Text
            if text.strip() == '' or text.strip() == '\r' or text.strip() == '\r\n':
                para.Range.Delete()
        
        # Замена табуляций
        find_obj = doc.Content.Find
        find_obj.ClearFormatting()
        find_obj.Text = "^t"
        find_obj.Replacement.ClearFormatting()
        find_obj.Replacement.Text = " "
        find_obj.Execute(Replace=2)
        
        # Замена нескольких пробелов подряд
        for para in doc.Paragraphs:
            if para.Range.Text:
                text = para.Range.Text
                # Заменяем 2 и более пробелов на 1
                cleaned = re.sub(r' {2,}', ' ', text)
                if cleaned != text:
                    para.Range.Text = cleaned
        
        # Применяем шрифт
        doc.Content.Font.Name = font_name
        doc.Content.Font.Size = font_size
        
        # Стили Заголовков
        for para in doc.Paragraphs:
            text = para.Range.Text.strip()
            if not text:
                continue
            
            # Заголовок 2: "1.1. Текст"
            if re.match(r'^\d+\.\d+\.?\s', text):
                try:
                    para.Style = -3  # Заголовок 2
                    para.Range.Font.Bold = True
                except:
                    pass
            
            # Заголовок 1: "1. Текст" или "ВВЕДЕНИЕ", "ЗАКЛЮЧЕНИЕ"
            elif re.match(r'^\d+\.\s', text) or text in ['ВВЕДЕНИЕ', 'ЗАКЛЮЧЕНИЕ', 'ОСНОВНАЯ ЧАСТЬ']:
                try:
                    para.Style = -2  # Заголовок 1
                    para.Range.Font.Bold = True
                except:
                    pass
        
        # Таблицы
        for table in doc.Tables:
            table.Borders.OutsideLineStyle = 1
            table.Borders.InsideLineStyle = 1
            
            for row in table.Rows:
                for cell in row.Cells:
                    try:
                        cell.VerticalAlignment = 1
                        cell.Range.Paragraphs.Alignment = 1
                    except:
                        pass
            
            if table.Rows.Count > 0:
                for cell in table.Rows(1).Cells:
                    try:
                        cell.Range.Font.Bold = True
                        cell.Shading.BackgroundPatternColor = 14277081
                    except:
                        pass
        
        # Сохраняем
        doc.SaveAs(output_path)
        
    except Exception as e:
        raise Exception(f"Ошибка: {str(e)}")
    finally:
        if doc:
            try:
                doc.Close()
            except:
                pass
        if word:
            try:
                word.Quit()
            except:
                pass
        time.sleep(0.5)
        try:
            subprocess.run(['taskkill', '/f', '/im', 'WINWORD.EXE'], capture_output=True)
        except:
            pass