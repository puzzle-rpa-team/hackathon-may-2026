# -*- coding: utf-8 -*-
"""
Блок форматирования Word-документов для Puzzle RPA Studio
"""

import os
import re

# Пытаемся импортировать win32com с обработкой ошибок
try:
    import win32com.client
    from win32com.client import constants
    WIN32COM_AVAILABLE = True
except ImportError:
    WIN32COM_AVAILABLE = False
    print("Предупреждение: модуль win32com не установлен. Используйте: pip install pywin32")

def run(input_path, output_path=None, font_name="Calibri", font_size=12, replacements=None):
    """
    Основная функция блока
    """
    if not WIN32COM_AVAILABLE:
        raise ImportError(
            "Модуль pywin32 не установлен.\\n"
            "Откройте командную строку и выполните: pip install pywin32\\n"
            "Затем перезапустите Puzzle RPA Studio"
        )
    
    if replacements is None:
        replacements = {}
    
    # Проверка входного файла
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Файл не найден: {input_path}")
    
    if not input_path.lower().endswith('.docx'):
        raise ValueError("Поддерживаются только файлы формата .docx")
    
    word = None
    doc = None
    
    try:
        # Запускаем Word
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False
        
        # Открываем документ
        abs_path = os.path.abspath(input_path)
        doc = word.Documents.Open(abs_path)
        
        # Применяем форматирование
        _apply_formatting(doc, font_name, font_size, replacements)
        
        # Сохраняем результат
        if output_path:
            doc.SaveAs(os.path.abspath(output_path))
        else:
            doc.Save()
        
        return {
            "success": True, 
            "message": f"Документ успешно отформатирован. Сохранен: {output_path or input_path}"
        }
    
    except Exception as e:
        raise RuntimeError(f"Ошибка: {str(e)}")
    
    finally:
        if doc:
            try:
                doc.Close(False)
            except:
                pass
        if word:
            try:
                word.Quit()
            except:
                pass


def _apply_formatting(doc, font_name, font_size, replacements):
    """Применяет все форматирования"""
    
    # Очищаем прямое форматирование
    doc.Content.Font.Reset()
    
    # Применяем единый шрифт
    content = doc.Content
    content.Font.Name = font_name
    content.Font.Size = font_size
    
    # Удаляем пустые абзацы (ищем с конца)
    paragraphs = doc.Paragraphs
    for i in range(paragraphs.Count, 0, -1):
        para = paragraphs(i)
        if len(para.Range.Text.strip()) == 0:
            para.Range.Delete()
    
    # Определяем заголовки
    for i in range(1, paragraphs.Count + 1):
        para = paragraphs(i)
        text = para.Range.Text.strip()
        
        if re.match(r'^\\d+\\.\\s+', text):
            para.Range.Style = doc.Styles("Заголовок 1")
        elif re.match(r'^\\d+\\.\\d+\\.\\s+', text):
            para.Range.Style = doc.Styles("Заголовок 2")
    
    # Заменяем плейсхолдеры
    if replacements:
        find = doc.Content.Find
        find.ClearFormatting()
        find.Replacement.ClearFormatting()
        
        for key, value in replacements.items():
            find.Text = f"{{{{{key}}}}}"
            find.Replacement.Text = str(value)
            find.Execute(Replace=2)