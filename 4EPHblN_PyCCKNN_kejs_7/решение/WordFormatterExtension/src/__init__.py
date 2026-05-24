import os
import re
import json

from puzzle_logger import log_decorator, window_logger


def _parse_replacements(replacements):
    """Принимает dict или строку JSON, возвращает dict."""
    if not replacements:
        return {}
    if isinstance(replacements, dict):
        return replacements
    if isinstance(replacements, str):
        raw = replacements.strip()
        if not raw or raw in ("{}", "null", "none", ""):
            return {}
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Некорректный формат replacements. "
                f"Ожидается JSON-словарь, например: {{\"Дата\": \"01.01.2025\"}}. "
                f"Ошибка: {e}"
            )
    # Неожиданный тип — не бросаем ошибку, просто игнорируем замены
    return {}


def _is_heading_1(text):
    """Заголовок первого уровня: «1. Текст» или ключевое слово."""
    s = text.strip()
    if re.match(r"^\d+\.\s", s) and not re.match(r"^\d+\.\d+\.\s", s):
        return True
    keywords = {
        "введение", "заключение", "содержание", "оглавление",
        "список литературы", "приложение", "аннотация", "abstract",
    }
    return s.lower() in keywords


def _is_heading_2(text):
    """Заголовок второго уровня: «1.1. Текст»."""
    return bool(re.match(r"^\d+\.\d+\.\s", text.strip()))


def _replace_placeholders(doc, repl_dict):
    """
    Заменяет {{ключ}} на значение через Word Find/Replace.

    Проблема с пробелами в ключе: Word при поиске строки с пробелами
    может разбивать её на отдельные run-ы с разным форматированием,
    из-за чего Find не находит плейсхолдер целиком.
    Решение: используем MatchWildcards=False и явно передаём все
    параметры позиционно, чтобы исключить влияние предыдущих вызовов.
    Дополнительно обходим параграфы вручную через Python как fallback.
    """
    for key, value in repl_dict.items():
        placeholder = "{{" + str(key) + "}}"
        replace_str = str(value)

        # Попытка 1: стандартный Find/Replace по всему документу
        find = doc.Content.Find
        find.ClearFormatting()
        find.Replacement.ClearFormatting()
        find.Text = ""
        find.Replacement.Text = ""

        found = find.Execute(
            FindText=placeholder,      # 1 - что ищем
            MatchCase=True,            # 2 - учитывать регистр
            MatchWholeWord=False,      # 3 - НЕ целое слово (иначе "Номер договора" не найдётся)
            MatchWildcards=False,      # 4 - без wildcards (иначе {{ и }} интерпретируются)
            MatchSoundsLike=False,     # 5
            MatchAllWordForms=False,   # 6
            Forward=True,              # 7
            Wrap=1,                    # 8 - wdFindContinue
            Format=False,              # 9
            ReplaceWith=replace_str,   # 10
            Replace=2,                 # 11 - wdReplaceAll
        )

        # Попытка 2 (fallback): если Find не нашёл — обходим параграфы вручную через Python.
        # Это решает случай, когда плейсхолдер разбит на несколько run-ов с разным форматом.
        _replace_in_paragraphs(doc, placeholder, replace_str)


def _replace_in_paragraphs(doc, placeholder, value):
    """
    Fallback-замена: проходит по параграфам и заменяет текст напрямую.
    Работает даже когда плейсхолдер разбит на run-ы с разным форматированием,
    потому что para.Range.Text возвращает весь текст параграфа целиком.
    """
    for i in range(1, doc.Paragraphs.Count + 1):
        para = doc.Paragraphs(i)
        if placeholder in para.Range.Text:
            # Ищем и заменяем внутри этого параграфа через Find
            rng = para.Range
            find = rng.Find
            find.ClearFormatting()
            find.Replacement.ClearFormatting()
            find.Execute(
                FindText=placeholder,
                MatchCase=True,
                MatchWholeWord=False,
                MatchWildcards=False,
                MatchSoundsLike=False,
                MatchAllWordForms=False,
                Forward=True,
                Wrap=1,
                Format=False,
                ReplaceWith=value,
                Replace=2,
            )

    # Также проверяем ячейки таблиц
    for t_idx in range(1, doc.Tables.Count + 1):
        table = doc.Tables(t_idx)
        for r_idx in range(1, table.Rows.Count + 1):
            for c_idx in range(1, table.Columns.Count + 1):
                try:
                    cell = table.Cell(r_idx, c_idx)
                    if placeholder in cell.Range.Text:
                        find = cell.Range.Find
                        find.ClearFormatting()
                        find.Replacement.ClearFormatting()
                        find.Execute(
                            FindText=placeholder,
                            MatchCase=True,
                            MatchWholeWord=False,
                            MatchWildcards=False,
                            MatchSoundsLike=False,
                            MatchAllWordForms=False,
                            Forward=True,
                            Wrap=1,
                            Format=False,
                            ReplaceWith=value,
                            Replace=2,
                        )
                except Exception:
                    pass


def _clean_document_whitespace(doc):
    """
    Убирает табуляции и множественные пробелы во всём документе сразу
    через doc.Content.Find — надёжнее, чем работа с диапазоном параграфа,
    который может схлопываться после замены.
    """
    find = doc.Content.Find
    find.ClearFormatting()
    find.Replacement.ClearFormatting()

    # Шаг 1: заменяем табуляцию на пробел (^t — спецсимвол Word для табуляции)
    find.Execute(
        FindText="^t",
        MatchCase=False,
        MatchWholeWord=False,
        MatchWildcards=False,
        MatchSoundsLike=False,
        MatchAllWordForms=False,
        Forward=True,
        Wrap=1,
        Format=False,
        ReplaceWith=" ",
        Replace=2,
    )

    # Шаг 2: сжимаем множественные пробелы до одного.
    # Повторяем до 10 раз: каждый проход заменяет «два пробела» на «один»,
    # поэтому N последовательных пробелов требуют log2(N) проходов.
    for _ in range(10):
        replaced = find.Execute(
            FindText="  ",             # два пробела
            MatchCase=False,
            MatchWholeWord=False,
            MatchWildcards=False,
            MatchSoundsLike=False,
            MatchAllWordForms=False,
            Forward=True,
            Wrap=1,
            Format=False,
            ReplaceWith=" ",           # один пробел
            Replace=2,
        )
        # Execute возвращает True если хоть одна замена была сделана
        if not replaced:
            break


def _apply_style(doc, para, style_name):
    """Применяет встроенный стиль Word к параграфу."""
    try:
        para.Style = doc.Styles(style_name)
    except Exception:
        pass


def _apply_font(para, font_name, font_size, bold=False):
    """Применяет шрифт ко всем символам параграфа."""
    rng = para.Range
    rng.Font.Name = font_name
    rng.Font.Size = font_size
    rng.Font.Bold = bold
    if not bold:
        rng.Font.Italic = False
        rng.Font.Underline = 0


def _format_paragraphs(doc, font_name, font_size):
    """
    Проходит по всем параграфам документа:
    - убирает дублирующиеся пустые строки;
    - чистит пробелы и табуляции (один проход по всему документу до цикла);
    - назначает стили Heading 1 / Heading 2 / Normal;
    - применяет единый шрифт.
    """
    # Чистим пробелы и табуляции сразу по всему документу —
    # это надёжнее, чем делать это внутри цикла по параграфам.
    _clean_document_whitespace(doc)

    paragraphs = doc.Paragraphs
    prev_empty = False
    to_delete = []

    for i in range(1, paragraphs.Count + 1):
        para = paragraphs(i)
        raw = para.Range.Text.strip()
        is_empty = (raw == "" or raw == "\x07")

        if is_empty:
            if prev_empty:
                to_delete.append(i)
            prev_empty = True
            continue

        prev_empty = False

        if _is_heading_2(raw):
            _apply_style(doc, para, "Heading 2")
            _apply_font(para, font_name, font_size + 2, bold=True)
        elif _is_heading_1(raw):
            _apply_style(doc, para, "Heading 1")
            _apply_font(para, font_name, font_size + 4, bold=True)
        else:
            _apply_style(doc, para, "Normal")
            _apply_font(para, font_name, font_size, bold=False)

    for idx in reversed(to_delete):
        try:
            doc.Paragraphs(idx).Range.Delete()
        except Exception:
            pass


def _format_tables(doc, font_name, font_size):
    """
    Форматирует все таблицы:
    - видимые границы;
    - шрифт во всех ячейках;
    - первая строка — жирный + светло-серая заливка;
    - выравнивание по левому краю.
    """
    WD_LINE_SINGLE = 1
    WD_COLOR_GRAY  = 15921906  # #F2F2F2

    for t_idx in range(1, doc.Tables.Count + 1):
        table = doc.Tables(t_idx)
        try:
            table.Borders.InsideLineStyle  = WD_LINE_SINGLE
            table.Borders.OutsideLineStyle = WD_LINE_SINGLE
        except Exception:
            pass

        for r_idx in range(1, table.Rows.Count + 1):
            is_header = (r_idx == 1)
            for c_idx in range(1, table.Columns.Count + 1):
                try:
                    cell = table.Cell(r_idx, c_idx)
                    cell.Range.Font.Name = font_name
                    cell.Range.Font.Size = font_size
                    cell.Range.Font.Bold = is_header
                    if is_header:
                        cell.Shading.BackgroundPatternColor = WD_COLOR_GRAY
                    for p_idx in range(1, cell.Range.Paragraphs.Count + 1):
                        cell.Range.Paragraphs(p_idx).Alignment = 0
                except Exception:
                    pass


@window_logger
@log_decorator
def format_document(
    input_path,
    output_path=None,
    font_name="Calibri",
    font_size=12,
    replacements=None,
    puzzle_logger_path=None,
    block_text=None,
    block_id=None,
    window_log=False,
    **kwargs,
):
    """
    Форматирует Word-документ (.docx):
      - Заменяет плейсхолдеры {{ключ}} значениями из словаря replacements.
      - Убирает лишние пустые абзацы, пробелы, табуляции.
      - Применяет единый шрифт font_name / font_size ко всему тексту.
      - Назначает стили Heading 1 / Heading 2 по нумерации или ключевым словам.
      - Форматирует таблицы: границы, заливка заголовка, выравнивание.
      - Сохраняет результат в output_path (или перезаписывает input_path).

    :param input_path:   Абсолютный путь к исходному .docx файлу (обязательный).
    :param output_path:  Путь для сохранения результата (необязательный).
    :param font_name:    Название шрифта (по умолчанию Calibri).
    :param font_size:    Размер шрифта в пунктах (по умолчанию 12).
    :param replacements: Словарь или JSON-строка для замены {{ключ}}.
    """

    if not input_path:
        raise ValueError("Параметр input_path обязателен и не может быть пустым.")

    input_path = str(input_path).strip()

    if not os.path.isabs(input_path):
        raise ValueError(
            f"input_path должен быть абсолютным путём. Получено: '{input_path}'"
        )
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Файл не найден: '{input_path}'")
    if not input_path.lower().endswith(".docx"):
        raise ValueError(
            f"Поддерживается только .docx. Получен: '{os.path.basename(input_path)}'"
        )

    # Путь сохранения
    if output_path and str(output_path).strip():
        save_path = str(output_path).strip()
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
    else:
        save_path = input_path

    # Замены
    repl_dict = _parse_replacements(replacements)

    # Размер шрифта
    try:
        font_size = int(font_size)
    except (TypeError, ValueError):
        raise ValueError(f"font_size должен быть числом, получено: '{font_size}'")
    if not (6 <= font_size <= 72):
        raise ValueError(f"font_size должен быть от 6 до 72, получено: {font_size}")

    font_name = str(font_name).strip() if font_name and str(font_name).strip() not in ("None", "") else "Calibri"

    try:
        import win32com.client as win32
    except ImportError:
        raise ImportError(
            "win32com не найден. Проверьте корректность установки Puzzle RPA Studio."
        )

    word = None
    doc  = None
    try:
        word = win32.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0

        doc = word.Documents.Open(input_path)

        if repl_dict:
            _replace_placeholders(doc, repl_dict)

        _format_paragraphs(doc, font_name, font_size)
        _format_tables(doc, font_name, font_size)

        if save_path == input_path:
            doc.Save()
        else:
            # Если файл по пути сохранения уже существует — удаляем его заранее.
            # Это предотвращает диалог подтверждения перезаписи в Word,
            # который блокирует выполнение даже при DisplayAlerts = 0.
            if os.path.exists(save_path):
                os.remove(save_path)
            doc.SaveAs2(save_path)

    except Exception as exc:
        raise RuntimeError(
            f"Ошибка при обработке '{os.path.basename(input_path)}': {exc}"
        ) from exc
    finally:
        if doc is not None:
            try:
                doc.Close(False)
            except Exception:
                pass
        if word is not None:
            try:
                word.Quit()
            except Exception:
                pass

    return save_path
