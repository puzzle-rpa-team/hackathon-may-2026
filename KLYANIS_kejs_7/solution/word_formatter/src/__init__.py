import os
import re
import pythoncom
import win32com.client as win32

from function_message.desktop_message import send_action_message
from puzzle_logger import log_decorator, window_logger

_H2_RE = re.compile(r'^\d+\.\d+\.?\s+\S')
_H1_RE = re.compile(r'^\d+\.?\s+\S')
_H1_KEYWORDS = frozenset([
    'введение', 'заключение', 'список литературы', 'библиография',
    'содержание', 'оглавление', 'приложение', 'аннотация',
    'abstract', 'references', 'conclusion', 'introduction',
])


@window_logger
@log_decorator
def word_formatter(
    path_file=None,
    path_file_end=None,
    font_name=None,
    font_size=None,
    replacements=None,
    puzzle_logger_path=None,
    block_text=None,
    block_id=None,
    window_log=False,
    **kwargs
):
    current_language = kwargs.get('current_language', 'ru')

    if not path_file:
        raise ValueError("'Путь к файлу' обязателен")

    in_path = os.path.abspath(str(path_file))
    if not os.path.isfile(in_path):
        raise FileNotFoundError(f"Файл не найден: {in_path}")

    out_path = os.path.abspath(str(path_file_end)) if path_file_end else in_path

    if _word_locked(in_path):
        raise PermissionError(f"Файл уже открыт в Word: {in_path}")

    font_name    = str(font_name) if font_name else None
    font_size    = int(font_size) if font_size else None
    replacements = dict(replacements) if replacements else {}

    send_action_message("message_open_file", current_language, window_log)
    pythoncom.CoInitialize()
    word = None
    try:
        word = win32.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False
        doc = word.Documents.Open(in_path)

        send_action_message("message_data_file", current_language, window_log)

        for key, value in replacements.items():
            _find_replace(doc, "{{" + str(key) + "}}", str(value))

        _find_replace(doc, "^t", " ")
        for _ in range(15):
            if not _find_replace(doc, "  ", " "):
                break
        for _ in range(20):
            if not _find_replace(doc, "^p^p^p", "^p^p"):
                break

        if font_name:
            doc.Content.Font.Name = font_name
        if font_size:
            doc.Content.Font.Size = font_size

        style_h1 = _get_style(doc, "Заголовок 1", "Heading 1")
        style_h2 = _get_style(doc, "Заголовок 2", "Heading 2")
        for para in doc.Paragraphs:
            text = para.Range.Text.strip()
            if not text:
                continue
            lower = text.lower()
            target_style, size_delta = None, 0
            if _H2_RE.match(text):
                target_style, size_delta = style_h2, 2
            elif _H1_RE.match(text):
                target_style, size_delta = style_h1, 4
            elif any(kw in lower for kw in _H1_KEYWORDS):
                target_style, size_delta = style_h1, 4
            if target_style is not None:
                try:
                    para.Style = target_style
                except Exception:
                    pass
                if font_name:
                    para.Range.Font.Name = font_name
                if font_size:
                    para.Range.Font.Size = font_size + size_delta
                para.Range.Font.Bold = True
                para.Range.Font.Color = 0

        for table in doc.Tables:
            try:
                table.Borders.Enable = True
                table.Borders.InsideLineStyle = 1
                table.Borders.OutsideLineStyle = 1
            except Exception:
                pass
            if font_name:
                table.Range.Font.Name = font_name
            if font_size:
                table.Range.Font.Size = font_size
            table.Range.ParagraphFormat.Alignment = 0
            if table.Rows.Count >= 1:
                header_row = table.Rows(1)
                header_row.Range.Font.Bold = True
                _color_row(header_row, 14935011)

        send_action_message("message_save_file", current_language, window_log)

        if out_path != in_path:
            doc.SaveAs2(out_path, FileFormat=12)
        else:
            doc.Save()
        doc.Close()
        word.Quit()
        word = None

    finally:
        if word is not None:
            try:
                word.Quit(SaveChanges=0)
            except Exception:
                pass
        pythoncom.CoUninitialize()


def _word_locked(path):
    lock = os.path.join(os.path.dirname(path), '~$' + os.path.basename(path))
    return os.path.exists(lock)


def _find_replace(doc, find_text, replace_text):
    return bool(doc.Content.Find.Execute(
        FindText=find_text,
        MatchCase=False, MatchWholeWord=False, MatchWildcards=False,
        MatchSoundsLike=False, MatchAllWordForms=False,
        Forward=True, Wrap=1, Format=False,
        ReplaceWith=replace_text, Replace=2,
    ))


def _get_style(doc, *names):
    for name in names:
        try:
            return doc.Styles(name)
        except Exception:
            pass
    return None


def _color_row(row, color_long):
    try:
        for i in range(1, row.Cells.Count + 1):
            row.Cells(i).Shading.BackgroundPatternColor = color_long
    except Exception:
        pass
