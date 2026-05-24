from puzzle_logger import log_decorator, window_logger
import win32com.client as win32
import os
import re

WORD_EXTENSIONS = {'.doc', '.docx', '.docm', '.dot', '.dotx', '.dotm'}

HEADING_KEYWORDS = [
    'введение', 'заключение', 'выводы', 'вывод',
    'содержание', 'оглавление',
    'список литературы', 'литература', 'источники',
    'приложение', 'приложения', 'практическая часть', 'теоретическая часть', 'технологическая часть',
    'abstract', 'introduction', 'conclusion', 'references'
]

HEADING1_PATTERN = re.compile(r'^\d+\.\s')
HEADING2_PATTERN = re.compile(r'^\d+\.\d+\.\s')


def is_correct_format(file_path):
    """Проверяет, является ли файл документом Word по расширению."""
    return os.path.splitext(file_path)[1].lower() in WORD_EXTENSIONS


def is_heading1(text):
    """Определяет заголовок первого уровня по паттерну или ключевому слову."""
    text = text.strip()
    if HEADING1_PATTERN.match(text) and not HEADING2_PATTERN.match(text):
        return True
    return text.lower() in HEADING_KEYWORDS


def is_heading2(text):
    """Определяет заголовок второго уровня по паттерну."""
    return bool(HEADING2_PATTERN.match(text.strip()))


def clean_document(doc):
    """
    Очищает документ от лишнего форматирования:
    - сбрасывает прямое форматирование абзацев
    - удаляет пустые абзацы
    - удаляет множественные пробелы
    """
    for para in doc.Paragraphs:
        try:
            para.Range.Font.Reset()
            para.Range.ParagraphFormat.Reset()
        except Exception:
            continue

    for para in doc.Paragraphs:
        try:
            text = para.Range.Text
            stripped = text.strip()
            if stripped != text.rstrip('\r'):
                para.Range.Text = stripped + '\r'
        except Exception:
            continue

    try:
        word = doc.Application
        word.Selection.Find.ClearFormatting()
        word.Selection.Find.Replacement.ClearFormatting()
        word.Selection.Find.Execute("\t", False, False, False, False, False, True, 1, False, " ", 2)
    except Exception:
        pass

    indices_to_delete = []
    for i in range(1, doc.Paragraphs.Count + 1):
        try:
            text = doc.Paragraphs(i).Range.Text.strip()
            if not text or text == '\r':
                indices_to_delete.append(i)
        except Exception:
            continue

    for i in reversed(indices_to_delete):
        try:
            doc.Paragraphs(i).Range.Delete()
        except Exception:
            continue


def apply_font(doc, font_name, font_size):
    """Применяет единый шрифт ко всему документу."""
    doc.Range().Font.Name = font_name
    doc.Range().Font.Size = font_size


def apply_headings(doc, font_name):
    """Определяет заголовки и применяет соответствующие стили."""
    for i in range(1, doc.Paragraphs.Count + 1):
        try:
            para = doc.Paragraphs(i)
            text = para.Range.Text.strip()

            if not text:
                continue

            if is_heading2(text):
                _apply_heading_style(para, 2, font_name, doc)
            elif is_heading1(text):
                _apply_heading_style(para, 1, font_name, doc)

        except Exception:
            continue


def _apply_heading_style(para, level, font_name, doc):
    """Вспомогательная: применяет стиль и форматирование к заголовку."""
    try:
        try:
            para.Style = doc.Styles(f"Заголовок {level}")
        except Exception:
            para.Style = doc.Styles(f"Heading {level}")

        para.Range.Font.Name = font_name
        para.Range.Font.Bold = True
        para.Range.Font.Size = 14 if level == 1 else 12
    except Exception:
        para.Range.Font.Bold = True


def format_tables(doc, font_name, font_size):
    """Форматирует все таблицы: границы, выравнивание, заголовочная строка."""
    for table in doc.Tables:
        try:
            # Рамка
            try:
                table.Borders.Enable = True
            except Exception:
                pass


            # Выравнивание и шрифт
            table.Range.ParagraphFormat.Alignment = 1
            table.Range.Cells.VerticalAlignment = 1
            table.Range.Font.Name = font_name
            table.Range.Font.Size = font_size

            # Заголовочная строка
            if table.Rows.Count > 0:
                header = table.Rows(1)
                header.Range.Font.Bold = True
                header.Range.Shading.BackgroundPatternColor = 12632256

        except Exception:
            continue


def replace_placeholders(doc, replacements):
    """Заменяет плейсхолдеры {{ключ}} на значения из словаря."""
    if not replacements or not isinstance(replacements, dict):
        return
    for key, value in replacements.items():
        try:
            word = doc.Application
            word.Selection.Find.ClearFormatting()
            word.Selection.Find.Replacement.ClearFormatting()
            word.Selection.Find.Execute(
                f"{{{{{key}}}}}",
                False,
                False,
                False,
                False,
                False,
                True,
                1,
                False,
                str(value),
                2
            )
        except Exception:
            continue


@window_logger
@log_decorator
def format_word_document(input_path, output_path=None, font_name="Calibri", font_size=12,
                         replacements=None, puzzle_logger_path=None, **kwargs):
    """
    Основная функция форматирования Word-документа.
    Вызывает вспомогательные функции последовательно.
    """
    if not input_path:
        raise ValueError("Не указан путь к файлу (input_path)")

    abs_input = os.path.abspath(str(input_path))

    if not os.path.exists(abs_input):
        raise FileNotFoundError(f"Файл не найден: {abs_input}")

    if not is_correct_format(abs_input):
        raise ValueError(f"Файл не является документом Word: {abs_input}")

    try:
        font_size = int(font_size)
    except (TypeError, ValueError):
        font_size = 12

    word = None
    doc = None

    try:
        try:
            word = win32.Dispatch("Word.Application")
            word.Visible = False
            word.DisplayAlerts = 0
        except Exception:
            try:
                import subprocess
                subprocess.run(["taskkill", "/f", "/im", "WINWORD.EXE"],
                               capture_output=True)
                word = win32.Dispatch("Word.Application")
                word.Visible = False
                word.DisplayAlerts = 0
            except Exception as e:
                raise EnvironmentError(
                    f"Microsoft Word не найден или не удалось запустить: {str(e)}"
                )

        doc = word.Documents.Open(abs_input)

        clean_document(doc)  # 1. Очистка
        apply_font(doc, font_name, font_size)  # 2. Шрифт
        apply_headings(doc, font_name)  # 3. Заголовки
        format_tables(doc, font_name, font_size)  # 4. Таблицы
        replace_placeholders(doc, replacements)  # 5. Плейсхолдеры

        if output_path and str(output_path).strip():
            abs_output = os.path.abspath(str(output_path))
            output_dir = os.path.dirname(abs_output)
            if output_dir and not os.path.exists(output_dir):
                raise FileNotFoundError(f"Папка для сохранения не существует: {output_dir}")
        else:
            abs_output = abs_input

        if abs_output == abs_input:
            doc.Save()
        else:
            for open_doc in word.Documents:
                try:
                    if os.path.abspath(open_doc.FullName) == abs_output:
                        open_doc.Close(SaveChanges=0)
                        break
                except Exception:
                    continue

            doc.SaveAs(abs_output)

        return f"Успешно отформатировано: {abs_output}"


    except (FileNotFoundError, ValueError, EnvironmentError):
        raise
    except Exception as e:
        raise Exception(f"Ошибка при работе с Word: {str(e)}")
    finally:
        try:
            if doc:
                doc.Close(SaveChanges=0)
        except Exception:
            pass
        try:
            if word:
                word.Quit()
        except Exception:
            pass
