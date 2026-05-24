# 📄 PDFYandexVisionBlock

![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Puzzle RPA](https://img.shields.io/badge/Puzzle%20RPA-3.0.2%2B-F9A825)
![Yandex Vision](https://img.shields.io/badge/Yandex%20Vision-OCR-EA4335)
![Input](https://img.shields.io/badge/Input-PDF-1F6FEB)
![Architecture](https://img.shields.io/badge/CPU-x64%20%7C%20x86%20%7C%20ARM64-555555)
![Status](https://img.shields.io/badge/Extension-tested-success)

<img src="../Демо/YANDEX%20OCR%20LOGO.png" align="right"
     alt="Yandex logo" width="120" height="120">

PDFYandexVisionBlock — расширение для Puzzle RPA, которое отправляет PDF-документы
в Yandex Vision OCR, получает распознанный текст и таблицы, а затем извлекает
основные реквизиты документа.

- 📄 Поддержка OCR для PDF через **Yandex Vision API**.
- 🔍 Извлечение **номера**, **даты**, **суммы** и **контрагентов**.
- 📊 Поддержка табличных данных и структурированного результата.
- 🧩 Интеграция с **Puzzle RPA Studio** как value-блок.
- 🐍 Возврат результата в формате **Python dict** или **JSON**.
- 🔐 Автоматический обмен OAuth-токена на IAM-токен.
- ♻️ Кэширование IAM-токена на время работы блока для стабильной работы async OCR.

<p align="center">
  <img src="../Демо/OCR%20EXAMPLE.png"
       alt="PDF OCR Example" width="900">
</p>

## ⚙️ Что делает блок

1. Принимает PDF-файл и параметры подключения.
2. Отправляет документ в Yandex Vision OCR.
3. Получает распознанный текст и таблицы.
4. Анализирует результат.
5. Извлекает ключевые реквизиты.
6. Возвращает структурированный объект.

## 🚀 Возможности

- Распознавание PDF-документов.
- Поддержка русского и английского языка.
- Обработка OCR-таблиц.
- Автоматическое определение типа документа.
- Готовый JSON для дальнейшей автоматизации.
- Подходит для интеграции в RPA-процессы.

## 📁 Структура проекта

```text
PDFYandexVisionBlock/
├── block.json
├── meta.json
├── values.xml
├── code.value.py
├── libs.py.json
├── typeToName.json
├── README.md
├── showcase_expected_output.json
├── showcase_input.pdf
└── src/
    └── __init__.py
```

### 🧩 Содержимое файлов

- `block.json` — описание блока.
- `meta.json` — режим value-блока и внутреннее логирование.
- `values.xml` — шаблон блока для тулбокса.
- `code.value.py` — вызов функции блока.
- `libs.py.json` — импорт модуля расширения.
- `typeToName.json` — читаемое имя блока.
- `src/__init__.py` — основная логика OCR и обработки.
- `expected_output.json` — пример ожидаемого результата.

## 📋 Требования

- Windows 10/11.
- Puzzle RPA Studio 3.0.2 или совместимая версия.
- Python 3.11.
- Интернет-доступ.
- Аккаунт Yandex Cloud.
- OAuth-токен и `folder_id`.

## 🛠️ Что нужно установить

### 🤖 Puzzle RPA Studio

Официальный сайт:

```text
https://puzzle-rpa.ru/
```

Инструкция по установке:

```text
https://wiki.puzzle-rpa.ru/ru/3.0.3/start/installation/
```

### 🐍 Python 3.11

Страница загрузки:

```text
https://www.python.org/downloads/windows/
```

Подойдет любая версия Python 3.11.x.

### ☁️ Yandex Cloud

Консоль:

```text
https://console.cloud.yandex.ru/
```

OAuth-токен:

```text
https://oauth.yandex.ru/authorize?response_type=token&client_id=1a6990aa636648e9b2ef855fa7bec2fb
```

## 📦 Установка расширения

1. Откройте Puzzle RPA Studio.
2. Перейдите в `Настройки -> Расширения -> Добавление`.
3. Нажмите `Выбрать`.
4. Укажите папку `PDFYandexVisionBlock`.
5. Выберите категорию `Обработка документов -> OCR`.
6. Подтвердите установку.
7. Перезапустите Puzzle RPA Studio.
8. После перезапуска блок появится в тулбоксе.

## 🧾 Параметры блока

| Параметр | Тип | Обязательный | Описание |
|---|---|---|---|
| TOKEN | string | Да | OAuth-токен `y0_...`, `OAuth y0_...`, `Bearer y0_...`, IAM token или API key |
| FOLDER_ID | string | Да | ID каталога Yandex Cloud |
| FILE_PATH | string | Да | Путь к PDF-файлу |
| LANGUAGE | dropdown | Нет | `ru`, `en`, `ru-en` |
| OUTPUT_FORMAT | dropdown | Нет | `dict` или `json` |

> Если передан OAuth-токен `y0_...`, `OAuth y0_...` или `Bearer y0_...`, блок автоматически обменивает его на IAM-токен перед вызовом OCR API и использует кэшированный IAM-токен для последующих запросов в рамках выполнения.

## ▶️ Использование

### 🔄 Пример процесса

1. Добавьте блок на схему.
2. Передайте токен, `folder_id` и путь к PDF.
3. Выберите язык OCR.
4. Выберите формат результата.
5. Запустите процесс.

### 📤 Пример результата

```json
{
  "document_type": "invoice",
  "number": "12345",
  "date": "2026-05-24",
  "amount": "15000.00",
  "contractor": "ООО Ромашка",
  "items": [
    {
      "name": "Услуга",
      "price": "15000.00"
    }
  ]
}
```

## 🧪 Как тестировать

1. Подготовьте реальный PDF-файл.
2. Передайте его в блок.
3. Используйте режим `ru-en` для смешанных документов.
4. Для первого запуска выберите формат `json`.
5. Запустите процесс.
6. Сохраните фактический результат в `expected_output.json`.

## 🚧 Ограничения

- Качество OCR зависит от качества PDF.
- Текущая версия поддерживает только одностраничные PDF.
- Многостраничные документы рекомендуется разделять.
- PNG/JPG необходимо предварительно конвертировать в PDF.


## 👥 Авторы

Команда: `Оптимус Прайм`

Участники: `Капитан Шарипов Данис Эдуардович, Горохов Дима Максимович, Волков Роман Александрович`

## 🎬 Демонстрация работы

[Смотреть демонстрацию работы](../Демо/Demo.mp4)
