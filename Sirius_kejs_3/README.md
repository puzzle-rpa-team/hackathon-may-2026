# Кейс 3 — Поиск документа и формирование печатной формы

**Хакатон Puzzle RPA | Команда 7**

## Описание

RPA-робот для автоматического поиска документов в 1С Бухгалтерия предприятия КОРП 3.0 и формирования печатных форм. Робот взаимодействует с 1С через веб-клиент — нажимает кнопки и вводит данные как пользователь.

## Архитектура

Проект построен на модульном принципе: каждая функция вынесена в отдельный `.robot` процесс, которые вызываются последовательно из главного `main.robot`.

```
main.robot
├── LoadConfig          — чтение конфигурации
├── ValidateConfig      — валидация полей конфига
├── PrepareEnvironment  — подготовка папок и путей
├── SearchDocuments     — поиск документов в 1С веб-клиенте
├── CheckSearchResults  — проверка результатов поиска
├── PrepareDocumentsList — фильтрация по режиму (first_only / all)
├── ProcessDocument     — получение и сохранение печатной формы
├── GenerateFinalReport — формирование report.csv
├── GenerateSummary     — формирование summary.txt
└── FinishProcess       — итоговый статус и завершение
```

## Структура проекта

```
Кейс3_ПоискПечатнойФормы1С/
├── process/
│   ├── main.robot
│   ├── LoadConfig.robot
│   ├── ValidateConfig.robot
│   ├── PrepareEnvironment.robot
│   ├── SearchDocuments.robot
│   ├── CheckSearchResults.robot
│   ├── PrepareDocumentsList.robot
│   ├── ProcessDocument.robot
│   ├── GetPrintForm.robot
│   ├── SavePrintForm.robot
│   ├── GenerateFinalReport.robot
│   ├── GenerateSummary.robot
│   └── FinishProcess.robot
└── resource/
    ├── config.json
    ├── print_forms/     — сохранённые печатные формы
    ├── report.csv       — отчёт по обработанным документам
    └── summary.txt      — итоги запуска
```

## Конфигурация

Все параметры запуска задаются в файле `resource/config.json`:

```json
{
  "document_type": "Документ.СчетНаОплатуПокупателю",
  "base_url": "https://demo1c.mkskom.ru/puzzle_buh_corp_8.3/ru/",
  "search_criteria": {
    "number": "",
    "date_from": "01.08.2025",
    "date_to": "31.08.2025",
    "counterparty": "",
    "organization": "",
    "sum_from": 0,
    "sum_to": 0
  },
  "mode": "first_only",
  "output_path": "print_forms",
  "output_format": "pdf",
  "file_name_template": "документ_{number}_{date}.pdf"
}
```

### Параметры

| Параметр | Описание |
|---|---|
| `document_type` | Тип документа в 1С |
| `base_url` | URL 1С веб-клиента |
| `search_criteria` | Критерии поиска (дата, номер, контрагент, организация) |
| `mode` | Режим обработки: `first_only`, `all`, `ask` |
| `output_path` | Папка для сохранения печатных форм |
| `output_format` | Формат файла: `pdf` |
| `file_name_template` | Шаблон имени файла |

## Режимы работы

| Режим | Описание |
|---|---|
| `first_only` | Обработать только первый найденный документ |
| `all` | Обработать все найденные документы |
| `ask` | Обработать все документы (расширенный режим) |

## Результаты работы

После запуска в папке `resource/` появятся:

- `print_forms/` — PDF файлы печатных форм
- `report.csv` — таблица с результатами обработки каждого документа
- `summary.txt` — итоговая сводка запуска

### Статусы завершения

| Статус | Описание |
|---|---|
| `SUCCESS` | Все документы обработаны без ошибок |
| `PARTIAL_SUCCESS` | Часть документов обработана с ошибками |
| `NO_DOCUMENTS` | Документы не найдены по заданным критериям |
| `FAILED` | Критическая ошибка процесса |

## Технологии

- **Puzzle RPA Studio** — среда разработки
- **1С Бухгалтерия предприятия КОРП 3.0** — целевая система
- **Блоки 1С веб-клиент** — взаимодействие с интерфейсом 1С
- **Яндекс Браузер** — браузер для веб-автоматизации
