import base64
import decimal
import datetime
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    import puzzle_logger
except ImportError:
    def log_decorator(func):
        return func

    def window_logger(func):
        return func
else:
    log_decorator = puzzle_logger.log_decorator
    window_logger = puzzle_logger.window_logger


VISION_BATCH_ANALYZE_URL = "https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze"
OCR_RECOGNIZE_URL = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"
OCR_ASYNC_URL = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeTextAsync"
OCR_GET_RECOGNITION_URL = "https://ocr.api.cloud.yandex.net/ocr/v1/getRecognition"
OPERATION_STATUS_URL_TEMPLATE = "https://operation.api.cloud.yandex.net/operations/{operation_id}"
IAM_TOKEN_URL = "https://iam.api.cloud.yandex.net/iam/v1/tokens"

REQUEST_TIMEOUT = 120
ASYNC_TIMEOUT = 300
POLL_INTERVAL_SECONDS = 2
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
MAX_PDF_PAGES = 200

SUPPORTED_EXTENSIONS = {".pdf"}
ORG_KEYWORDS = (
    "ооо",
    "ао",
    "пао",
    "оао",
    "зао",
    "ип",
    "llc",
    "jsc",
    "inc",
    "ltd",
)
DOCUMENT_NUMBER_STOPWORDS = {
    "от",
    "from",
    "dated",
    "date",
    "invoice",
    "счет",
    "счёт",
    "акт",
    "накладная",
    "договор",
    "упд",
}
COUNTERPARTY_ROLE_KEYWORDS = {
    "seller": ("продав", "поставщик", "исполнитель", "seller", "vendor", "supplier"),
    "buyer": ("покупат", "заказчик", "buyer", "customer"),
}
ORG_MARKER_PATTERN = re.compile(r"\b(?:ооо|ао|пао|оао|зао|ип|ooo|ao|pao|oao|zao|ip|llc|jsc|inc|ltd)\b", re.IGNORECASE)
TABLE_NAME_MARKERS = ("наименование", "description", "item")
TABLE_QTY_MARKERS = ("кол", "qty", "quantity")
TABLE_PRICE_MARKERS = ("цена", "price")
TABLE_AMOUNT_MARKERS = ("сумма", "amount", "total", "стоимость")
TABLE_FOOTER_MARKERS = (
    "итого",
    "всего",
    "к оплате",
    "total payable",
    "subtotal",
    "vat",
    "итоги",
    "payment terms",
    "delivery window",
    "продолжение таблицы",
    "continued table",
    "responsible manager",
    "contact email",
    "demo note",
)
NON_ORG_LINE_MARKERS = (
    "page ",
    "date:",
    "no:",
    "основание",
    "contract",
    "project",
    "примечание",
    "note",
    "@",
    "наименование",
    "description",
    "qty",
    "price",
    "amount",
    "delivery window",
    "продолжение таблицы",
    "continued table",
    "subtotal",
    "vat",
    "payment terms",
)
IAM_TOKEN_CACHE = {}


class YandexVisionError(RuntimeError):
    pass


class YandexVisionAuthError(YandexVisionError):
    pass


class YandexVisionPermissionError(YandexVisionError):
    pass


class YandexVisionQuotaError(YandexVisionError):
    pass


class YandexVisionUnavailableError(YandexVisionError):
    pass


class YandexVisionRequestError(YandexVisionError):
    def __init__(self, status_code, message):
        super().__init__(message)
        self.status_code = status_code


class YandexVisionUnsupportedError(YandexVisionRequestError):
    pass


@window_logger
@log_decorator
def process_pdf(
    token,
    folder_id,
    file_path,
    language="ru-en",
    output_format="dict",
    puzzle_logger_path=None,
    block_text=None,
    block_id=None,
    window_log=False,
    **kwargs
):
    _validate_inputs(token, folder_id, file_path)

    normalized_output = _normalize_output_format(output_format)
    language_codes = _normalize_language(language)
    document = _load_document(file_path)
    recognition = _recognize_document(
        token=token,
        folder_id=folder_id,
        content=document["content"],
        mime_type=document["mime_type"],
        language_codes=language_codes,
        page_count=document["page_count"],
    )

    pages = recognition["pages"]
    full_text = "\n\n".join(page["full_text"] for page in pages if page["full_text"]).strip()
    tables = _extract_tables(pages)
    line_items = _extract_line_items(tables)
    if not line_items:
        line_items = _extract_line_items_from_text(full_text)
    if not tables and line_items:
        tables = _build_tables_from_line_items(line_items)
    requisites = _parse_requisites(full_text)

    warnings = []
    if not line_items:
        warnings.append("Табличные позиции не найдены или не распознаны как таблица.")
    if not requisites["counterparties"]:
        warnings.append("Контрагенты не определены автоматически.")

    result = {
        "source_file": os.path.abspath(file_path),
        "page_count": len(pages) or document["page_count"],
        "document_type": requisites["document_type"],
        "document_number": requisites["document_number"],
        "document_date": requisites["document_date"],
        "total_amount": requisites["total_amount"],
        "currency": requisites["currency"],
        "counterparties": requisites["counterparties"],
        "line_items": line_items,
        "tables": tables,
        "warnings": warnings,
        "raw_text": full_text,
        "engine": recognition["engine"],
    }

    if normalized_output == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)
    return result


@window_logger
@log_decorator
def _validate_inputs(token, folder_id, file_path, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if not isinstance(token, str) or not token.strip():
        raise ValueError("Параметр TOKEN пустой.")

    if not isinstance(folder_id, str) or not folder_id.strip():
        raise ValueError("Параметр FOLDER_ID пустой.")

    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError("Параметр FILE_PATH пустой.")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Блок принимает только PDF-файлы.")

    size = os.path.getsize(file_path)
    if size <= 0:
        raise ValueError("PDF-файл пустой.")
    if size > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"Размер PDF превышает {MAX_FILE_SIZE_BYTES // (1024 * 1024)} МБ. "
            "Это ограничение публичного OCR API Yandex."
        )


@window_logger
@log_decorator
def _normalize_output_format(output_format, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    value = str(output_format or "dict").strip().lower()
    if value not in {"dict", "json"}:
        raise ValueError("OUTPUT_FORMAT должен быть dict или json.")
    return value


@window_logger
@log_decorator
def _normalize_language(language, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    value = str(language or "ru-en").strip().lower()
    if value == "ru":
        return ["ru"]
    if value == "en":
        return ["en"]
    if value in {"ru-en", "ru_en", "both", "mixed"}:
        return ["ru", "en"]
    raise ValueError("LANGUAGE должен быть ru, en или ru-en.")


@window_logger
@log_decorator
def _load_document(file_path, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    with open(file_path, "rb") as source_file:
        content = source_file.read()

    page_count = _count_pdf_pages(content)
    if page_count > MAX_PDF_PAGES:
        raise ValueError(
            f"PDF содержит {page_count} страниц. Публичный OCR API Yandex поддерживает до {MAX_PDF_PAGES} страниц на один PDF."
        )

    return {
        "content": content,
        "mime_type": "application/pdf",
        "page_count": page_count,
    }


@window_logger
@log_decorator
def _count_pdf_pages(content, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    matches = re.findall(rb"/Type\s*/Page\b", content)
    return max(1, len(matches))


@window_logger
@log_decorator
def _recognize_document(token, folder_id, content, mime_type, language_codes, page_count, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    try:
        batch_payload = _recognize_with_batch_analyze(token, folder_id, content, mime_type)
        batch_pages = _extract_batch_pages(batch_payload)
        if batch_pages:
            return {
                "pages": batch_pages,
                "engine": "Yandex Vision batchAnalyze",
            }
    except (YandexVisionUnsupportedError, YandexVisionRequestError, YandexVisionUnavailableError):
        pass

    ocr_payload = _recognize_with_ocr(token, folder_id, content, mime_type, language_codes, page_count)
    ocr_pages = _extract_ocr_pages(ocr_payload)
    if not ocr_pages:
        raise RuntimeError("Yandex Vision вернул ответ без распознанных страниц.")
    return {
        "pages": ocr_pages,
        "engine": "Yandex Vision OCR API",
    }


@window_logger
@log_decorator
def _recognize_with_batch_analyze(token, folder_id, content, mime_type, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    headers = _build_common_headers(token)
    payload = {
        "folderId": folder_id.strip(),
        "analyzeSpecs": [
            {
                "content": _to_base64(content),
                "mimeType": mime_type,
                "features": [
                    {
                        "type": "DOCUMENT_RECOGNITION",
                    }
                ],
            }
        ],
    }
    return _request_json(
        method="POST",
        url=VISION_BATCH_ANALYZE_URL,
        headers=headers,
        payload=payload,
        service_name="Yandex Vision batchAnalyze",
    )


@window_logger
@log_decorator
def _recognize_with_ocr(token, folder_id, content, mime_type, language_codes, page_count, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if page_count > 1:
        return _recognize_with_ocr_async(token, folder_id, content, mime_type, language_codes)
    return _recognize_with_ocr_sync(token, folder_id, content, mime_type, language_codes)


@window_logger
@log_decorator
def _recognize_with_ocr_sync(token, folder_id, content, mime_type, language_codes, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    headers = _build_ocr_headers(token, folder_id)
    payload = {
        "content": _to_base64(content),
        "mimeType": mime_type,
        "languageCodes": language_codes,
        "model": "page",
    }
    return _request_json(
        method="POST",
        url=OCR_RECOGNIZE_URL,
        headers=headers,
        payload=payload,
        service_name="Yandex OCR",
    )


@window_logger
@log_decorator
def _recognize_with_ocr_async(token, folder_id, content, mime_type, language_codes, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    headers = _build_ocr_headers(token, folder_id)
    payload = {
        "content": _to_base64(content),
        "mimeType": mime_type,
        "languageCodes": language_codes,
        "model": "page",
    }
    operation = _request_json(
        method="POST",
        url=OCR_ASYNC_URL,
        headers=headers,
        payload=payload,
        service_name="Yandex OCR async",
    )

    operation_id = str(operation.get("id") or "").strip()
    if not operation_id:
        raise RuntimeError("Yandex OCR async не вернул operation id.")

    _wait_for_operation(token, operation_id)
    return _get_recognition_result(token, folder_id, operation_id)


@window_logger
@log_decorator
def _wait_for_operation(token, operation_id, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    headers = _build_common_headers(token)
    deadline = time.time() + ASYNC_TIMEOUT

    while time.time() < deadline:
        payload = _request_json(
            method="GET",
            url=OPERATION_STATUS_URL_TEMPLATE.format(operation_id=operation_id),
            headers=headers,
            service_name="Yandex Operation",
        )
        if payload.get("done") is True:
            error_payload = payload.get("error") or {}
            if error_payload:
                message = _extract_error_message(error_payload) or "Асинхронная операция OCR завершилась с ошибкой."
                raise RuntimeError(message)
            return payload
        time.sleep(POLL_INTERVAL_SECONDS)

    raise RuntimeError("Yandex OCR выполняется слишком долго. Попробуйте уменьшить размер файла или повторить позже.")


@window_logger
@log_decorator
def _get_recognition_result(token, folder_id, operation_id, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    headers = _build_ocr_headers(token, folder_id)
    return _request_json(
        method="GET",
        url=OCR_GET_RECOGNITION_URL,
        headers=headers,
        params={"operationId": operation_id},
        service_name="Yandex OCR result",
    )


@window_logger
@log_decorator
def _build_common_headers(token, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    auth_scheme, auth_token = _resolve_authorization(token)
    return {
        "Authorization": f"{auth_scheme} {auth_token}",
        "Content-Type": "application/json",
    }


@window_logger
@log_decorator
def _build_ocr_headers(token, folder_id, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    headers = _build_common_headers(token)
    headers["x-folder-id"] = folder_id.strip()
    return headers


@window_logger
@log_decorator
def _resolve_authorization(token, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    token_value = str(token or "").strip()
    if not token_value:
        raise ValueError("Пустой токен авторизации.")

    lower_value = token_value.lower()
    if lower_value.startswith("bearer "):
        token_value = token_value[7:].strip()
        lower_value = token_value.lower()
    elif lower_value.startswith("oauth "):
        token_value = token_value[6:].strip()
        lower_value = token_value.lower()
    elif lower_value.startswith("api-key "):
        return "Api-Key", token_value[8:].strip()

    if _looks_like_oauth_token(token_value):
        return "Bearer", _exchange_oauth_to_iam(token_value)

    if _looks_like_api_key(token_value):
        return "Api-Key", token_value

    return "Bearer", token_value


@window_logger
@log_decorator
def _looks_like_oauth_token(token, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    return str(token).startswith("y0_")


@window_logger
@log_decorator
def _looks_like_api_key(token, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    return str(token or "").strip().startswith("AQVN")


@window_logger
@log_decorator
def _exchange_oauth_to_iam(oauth_token, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    cached_token = _get_cached_iam_token(oauth_token)
    if cached_token:
        return cached_token

    payload = {"yandexPassportOauthToken": oauth_token}
    response = _request_json(
        method="POST",
        url=IAM_TOKEN_URL,
        headers={"Content-Type": "application/json"},
        payload=payload,
        service_name="Yandex IAM",
    )

    iam_token = response.get("iamToken") or response.get("iam_token")
    if not iam_token:
        raise RuntimeError("Yandex IAM не вернул IAM-токен.")

    _store_cached_iam_token(oauth_token, iam_token, response.get("expiresAt") or response.get("expires_at"))
    return iam_token


@window_logger
@log_decorator
def _get_cached_iam_token(oauth_token, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    cache_entry = IAM_TOKEN_CACHE.get(oauth_token)
    if not cache_entry:
        return None

    expires_at = cache_entry.get("expires_at")
    if expires_at and expires_at <= datetime.datetime.utcnow() + datetime.timedelta(minutes=5):
        IAM_TOKEN_CACHE.pop(oauth_token, None)
        return None

    return cache_entry.get("iam_token")


@window_logger
@log_decorator
def _store_cached_iam_token(oauth_token, iam_token, expires_at_raw, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    IAM_TOKEN_CACHE[oauth_token] = {
        "iam_token": iam_token,
        "expires_at": _parse_iam_expiration(expires_at_raw),
    }


@window_logger
@log_decorator
def _parse_iam_expiration(expires_at_raw, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if not expires_at_raw:
        return None

    value = str(expires_at_raw).strip()
    if not value:
        return None

    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        parsed = datetime.datetime.fromisoformat(value)
        if parsed.tzinfo is not None:
            parsed = parsed.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        return parsed
    except ValueError:
        return None


@window_logger
@log_decorator
def _request_json(method, url, headers, payload=None, params=None, service_name="Yandex service", puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    final_url = _append_query_params(url, params)
    request_body = None
    if payload is not None:
        request_body = json.dumps(payload).encode("utf-8")

    http_request = urllib.request.Request(
        final_url,
        data=request_body,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(http_request, timeout=REQUEST_TIMEOUT) as response:
            status_code = response.getcode()
            response_text = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        status_code = exc.code
        response_text = exc.read().decode("utf-8", errors="replace")
    except TimeoutError as exc:
        raise RuntimeError(f"Превышено время ожидания ответа от {service_name}.") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ошибка сети при обращении к {service_name}: {exc}") from exc

    if status_code >= 400:
        _raise_service_error(service_name, status_code, response_text)

    raw_text = response_text.strip()
    if not raw_text:
        return {}
    return _decode_json_response(raw_text)


@window_logger
@log_decorator
def _append_query_params(url, params, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if not params:
        return url

    prepared = {}
    for key, value in params.items():
        if value is None:
            continue
        prepared[key] = str(value)

    if not prepared:
        return url

    delimiter = "&" if "?" in url else "?"
    return url + delimiter + urllib.parse.urlencode(prepared)


@window_logger
@log_decorator
def _raise_service_error(service_name, status_code, response_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    payload = _decode_error_payload(response_text)
    message = _extract_error_message(payload) or response_text.strip() or f"HTTP {status_code}"
    normalized = message.lower()

    if status_code == 401:
        raise YandexVisionAuthError(
            "Ошибка авторизации в Yandex Vision. Проверьте TOKEN: OAuth должен быть действительным, IAM token не должен быть просрочен."
        )
    if status_code == 403:
        raise YandexVisionPermissionError("Yandex Vision вернул 403. Проверьте права токена и корректность folder_id.")
    if status_code == 429 or "quota" in normalized or "limit" in normalized:
        raise YandexVisionQuotaError("Превышена квота или лимит запросов Yandex Vision.")
    if status_code >= 500:
        raise YandexVisionUnavailableError(f"Сервис {service_name} временно недоступен: HTTP {status_code}. {message}")

    if service_name == "Yandex Vision batchAnalyze" and _is_batch_unsupported_error(status_code, normalized):
        raise YandexVisionUnsupportedError(status_code, message)

    raise YandexVisionRequestError(status_code, f"{service_name}: HTTP {status_code}. {message}")


@window_logger
@log_decorator
def _decode_error_payload(response_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    try:
        return json.loads(response_text)
    except ValueError:
        return {"message": response_text.strip()}


@window_logger
@log_decorator
def _extract_error_message(payload, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if isinstance(payload, str):
        return payload.strip()

    if isinstance(payload, dict):
        for key in ("message", "description", "error"):
            value = payload.get(key)
            message = _extract_error_message(value)
            if message:
                return message
        details = payload.get("details")
        if isinstance(details, list):
            for detail in details:
                message = _extract_error_message(detail)
                if message:
                    return message
    return ""


@window_logger
@log_decorator
def _is_batch_unsupported_error(status_code, normalized_message, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if status_code in {404, 405, 501}:
        return True

    unsupported_markers = (
        "document_recognition",
        "unsupported",
        "not support",
        "application/pdf",
        "mime",
        "unknown field",
        "unknown feature",
        "bad request",
    )
    return status_code in {400, 415, 422} and any(marker in normalized_message for marker in unsupported_markers)


@window_logger
@log_decorator
def _decode_json_response(response_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    raw_text = response_text.strip()
    if not raw_text:
        return {}

    try:
        return json.loads(raw_text)
    except ValueError:
        pass

    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    parsed_lines = []
    for line in lines:
        try:
            parsed_lines.append(json.loads(line))
        except ValueError:
            parsed_lines = []
            break
    if parsed_lines:
        return parsed_lines

    decoder = json.JSONDecoder()
    objects = []
    position = 0
    while position < len(raw_text):
        while position < len(raw_text) and raw_text[position].isspace():
            position += 1
        if position >= len(raw_text):
            break
        parsed_object, position = decoder.raw_decode(raw_text, position)
        objects.append(parsed_object)

    if objects:
        return objects

    raise RuntimeError("Не удалось разобрать ответ Yandex Vision как JSON.")


@window_logger
@log_decorator
def _extract_batch_pages(payload, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    pages = []
    analyze_results = _ensure_list(payload.get("results")) or [payload]

    for analyze_result in analyze_results:
        feature_results = _ensure_list(analyze_result.get("results")) or [analyze_result]
        for feature_result in feature_results:
            candidates = []
            for key in ("documentRecognition", "document_recognition", "textDetection", "text_detection"):
                value = feature_result.get(key)
                if isinstance(value, dict):
                    candidates.append(value)
            if not candidates:
                candidates.append(feature_result)

            for candidate in candidates:
                if candidate.get("textAnnotation") or candidate.get("text_annotation"):
                    pages.append(_page_from_text_annotation(candidate, len(pages) + 1))
                    continue

                page_payloads = _ensure_list(candidate.get("pages"))
                for page_payload in page_payloads:
                    pages.append(_page_from_batch_payload(page_payload, candidate, len(pages) + 1))

    return [page for page in pages if page["full_text"] or page["tables"] or page["entities"]]


@window_logger
@log_decorator
def _extract_ocr_pages(payload, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    pages = []
    for item in _ensure_list(payload):
        if not isinstance(item, dict):
            continue

        if item.get("textAnnotation") or item.get("text_annotation"):
            pages.append(_page_from_text_annotation(item, len(pages) + 1))
            continue

        nested_result = item.get("result")
        if isinstance(nested_result, dict) and (nested_result.get("textAnnotation") or nested_result.get("text_annotation")):
            pages.append(_page_from_text_annotation(nested_result, len(pages) + 1))
            continue

        nested_results = _ensure_list(item.get("results"))
        if nested_results:
            pages.extend(_extract_ocr_pages(nested_results))

    return [page for page in pages if page["full_text"] or page["tables"] or page["entities"]]


@window_logger
@log_decorator
def _ensure_list(value, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


@window_logger
@log_decorator
def _page_from_text_annotation(payload, fallback_page_number, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    annotation = payload.get("textAnnotation") or payload.get("text_annotation") or {}
    blocks = annotation.get("blocks") or []
    full_text = (annotation.get("fullText") or annotation.get("full_text") or "").strip()
    if not full_text:
        full_text = _build_text_from_blocks(blocks, full_text)

    return {
        "page_number": _safe_int(payload.get("page"), fallback_page_number),
        "full_text": full_text.strip(),
        "blocks": blocks,
        "tables": annotation.get("tables") or [],
        "entities": annotation.get("entities") or [],
    }


@window_logger
@log_decorator
def _page_from_batch_payload(page_payload, parent_payload, fallback_page_number, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    blocks = page_payload.get("blocks") or parent_payload.get("blocks") or []
    full_text = (
        page_payload.get("text")
        or page_payload.get("fullText")
        or page_payload.get("full_text")
        or ""
    )
    if not full_text:
        full_text = _build_text_from_blocks(blocks, "")

    return {
        "page_number": _safe_int(page_payload.get("page") or page_payload.get("pageNumber"), fallback_page_number),
        "full_text": full_text.strip(),
        "blocks": blocks,
        "tables": page_payload.get("tables") or parent_payload.get("tables") or [],
        "entities": page_payload.get("entities") or parent_payload.get("entities") or [],
    }


@window_logger
@log_decorator
def _safe_int(value, default_value, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default_value


@window_logger
@log_decorator
def _extract_tables(pages, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    extracted = []
    table_index = 1
    for page in pages:
        for table in page.get("tables") or []:
            rows = _table_to_matrix(table, page.get("full_text") or "")
            if not rows:
                continue
            extracted.append(
                {
                    "table_index": table_index,
                    "page_number": page["page_number"],
                    "rows": rows,
                }
            )
            table_index += 1
    return extracted


@window_logger
@log_decorator
def _table_to_matrix(table, full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    cells = table.get("cells") or []
    if not cells:
        return []

    row_count = _safe_int(table.get("rowCount") or table.get("row_count"), 0)
    column_count = _safe_int(table.get("columnCount") or table.get("column_count"), 0)

    if row_count <= 0:
        row_count = max((_safe_int(cell.get("rowIndex") or cell.get("row_index"), 0) + 1 for cell in cells), default=0)
    if column_count <= 0:
        column_count = max((_safe_int(cell.get("columnIndex") or cell.get("column_index"), 0) + 1 for cell in cells), default=0)

    if row_count <= 0 or column_count <= 0:
        return []

    matrix = [["" for _ in range(column_count)] for _ in range(row_count)]
    for cell in cells:
        row_index = _safe_int(cell.get("rowIndex") or cell.get("row_index"), 0)
        column_index = _safe_int(cell.get("columnIndex") or cell.get("column_index"), 0)
        if row_index >= row_count or column_index >= column_count:
            continue
        text = _extract_text_from_node(cell, full_text)
        matrix[row_index][column_index] = text
    return matrix


@window_logger
@log_decorator
def _extract_text_from_node(node, full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if isinstance(node, str):
        return node.strip()
    if not isinstance(node, dict):
        return ""

    for key in ("text", "value", "content", "fullText", "full_text"):
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    segments = node.get("textSegments") or node.get("text_segments") or []
    segment_text = _extract_text_from_segments(segments, full_text)
    if segment_text:
        return segment_text

    words = node.get("words") or []
    if words:
        parts = [_extract_text_from_node(word, full_text) for word in words]
        return " ".join(part for part in parts if part).strip()

    lines = node.get("lines") or []
    if lines:
        parts = [_extract_text_from_node(line, full_text) for line in lines]
        return "\n".join(part for part in parts if part).strip()

    return ""


@window_logger
@log_decorator
def _extract_text_from_segments(segments, full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    fragments = []
    for segment in segments or []:
        start_index = _safe_int(segment.get("startIndex") or segment.get("start_index"), 0)
        end_index = _safe_int(segment.get("endIndex") or segment.get("end_index"), start_index)
        if 0 <= start_index <= end_index <= len(full_text):
            fragments.append(full_text[start_index:end_index])
    return "".join(fragments).strip()


@window_logger
@log_decorator
def _build_text_from_blocks(blocks, full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    lines = []
    for block in blocks or []:
        block_lines = block.get("lines") or []
        if not block_lines:
            line_text = _extract_text_from_node(block, full_text)
            if line_text:
                lines.append(line_text)
            continue
        for line in block_lines:
            line_text = _extract_text_from_node(line, full_text)
            if line_text:
                lines.append(line_text.strip())
    return "\n".join(line for line in lines if line).strip()


@window_logger
@log_decorator
def _extract_line_items(tables, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    items = []
    for table in tables:
        rows = table.get("rows") or []
        header_info = _detect_table_header(rows)
        if not header_info:
            continue

        header_row_index, mapping = header_info
        for row in rows[header_row_index + 1 :]:
            if not any(cell.strip() for cell in row):
                continue

            row_text = " ".join(cell.strip() for cell in row if cell.strip()).lower()
            if any(keyword in row_text for keyword in ("итого", "всего", "к оплате", "total")):
                continue

            name_index = mapping.get("name")
            name = row[name_index].strip() if name_index is not None and name_index < len(row) else ""
            if not name:
                continue

            quantity = _value_from_row(row, mapping.get("quantity"))
            price = _value_from_row(row, mapping.get("price"))
            amount = _value_from_row(row, mapping.get("amount"))
            if amount is None and quantity is not None and price is not None:
                amount = round(quantity * price, 2)

            items.append(
                {
                    "name": name,
                    "quantity": quantity,
                    "price": price,
                    "amount": amount,
                }
            )
    return items


@window_logger
@log_decorator
def _value_from_row(row, column_index, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if column_index is None or column_index >= len(row):
        return None
    return _to_float(_parse_decimal(row[column_index]))


@window_logger
@log_decorator
def _detect_table_header(rows, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    best_match = None
    best_score = 0
    for row_index, row in enumerate(rows[:5]):
        mapping = {"name": None, "quantity": None, "price": None, "amount": None}
        score = 0
        for column_index, cell in enumerate(row):
            normalized = _normalize_cell(cell)
            if mapping["name"] is None and any(keyword in normalized for keyword in ("наименование", "товар", "услуг", "работ", "item", "description")):
                mapping["name"] = column_index
                score += 1
            if mapping["quantity"] is None and any(keyword in normalized for keyword in ("кол", "qty", "quantity")):
                mapping["quantity"] = column_index
                score += 1
            if mapping["price"] is None and any(keyword in normalized for keyword in ("цена", "price")):
                mapping["price"] = column_index
                score += 1
            if mapping["amount"] is None and any(keyword in normalized for keyword in ("сумма", "итого", "amount", "total", "стоимость")):
                mapping["amount"] = column_index
                score += 1

        if score > best_score and mapping["name"] is not None:
            best_score = score
            best_match = (row_index, mapping)

    if best_score >= 2:
        return best_match
    return None


@window_logger
@log_decorator
def _normalize_cell(value, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    return str(value or "").strip().lower().replace("ё", "е")


@window_logger
@log_decorator
def _extract_line_items_from_text(full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    lines = [line.strip() for line in full_text.splitlines() if line.strip()]
    if not lines:
        return []

    items = []
    row_pattern = re.compile(
        r"^(?P<name>.+?)\s+(?P<quantity>\d+(?:[\.,]\d+)?)\s+(?P<price>\d[\d\s]*(?:[\.,]\d{1,2})?)\s+(?P<amount>\d[\d\s]*(?:[\.,]\d{1,2})?)$"
    )
    for line in lines:
        normalized = _normalize_cell(line)
        if any(keyword in normalized for keyword in ("итого", "всего", "к оплате", "total")):
            continue
        match = row_pattern.match(line)
        if not match:
            continue
        items.append(
            {
                "name": match.group("name").strip(),
                "quantity": _to_float(_parse_decimal(match.group("quantity"))),
                "price": _to_float(_parse_decimal(match.group("price"))),
                "amount": _to_float(_parse_decimal(match.group("amount"))),
            }
        )

    if items:
        return items

    items = _extract_structured_line_items_from_lines(lines)
    if items:
        return items

    return _extract_vertical_line_items(lines)


@window_logger
@log_decorator
def _extract_structured_line_items_from_lines(lines, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    items = []
    for block in _extract_table_blocks(lines):
        items.extend(_parse_table_block(block))
    return items


@window_logger
@log_decorator
def _extract_table_blocks(lines, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    blocks = []
    index = 0
    while index < len(lines):
        header_end = _get_table_header_end(lines, index)
        if header_end is None:
            index += 1
            continue

        block = []
        index = header_end
        while index < len(lines):
            line = lines[index].strip()
            normalized = _normalize_cell(line)
            if _get_table_header_end(lines, index) is not None and block:
                break
            if _is_table_footer_line(normalized):
                break
            if _is_table_noise_line(normalized):
                index += 1
                continue
            block.append(line)
            index += 1

        if block:
            blocks.append(block)
    return blocks


@window_logger
@log_decorator
def _get_table_header_end(lines, start_index, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if start_index >= len(lines):
        return None

    normalized = _normalize_cell(lines[start_index])
    if not any(marker in normalized for marker in TABLE_NAME_MARKERS):
        return None

    found_qty = any(marker in normalized for marker in TABLE_QTY_MARKERS)
    found_price = any(marker in normalized for marker in TABLE_PRICE_MARKERS)
    found_amount = any(marker in normalized for marker in TABLE_AMOUNT_MARKERS)

    end_index = start_index + 1
    while end_index < len(lines) and end_index - start_index <= 5:
        normalized = _normalize_cell(lines[end_index])
        found_qty = found_qty or any(marker in normalized for marker in TABLE_QTY_MARKERS)
        found_price = found_price or any(marker in normalized for marker in TABLE_PRICE_MARKERS)
        found_amount = found_amount or any(marker in normalized for marker in TABLE_AMOUNT_MARKERS)
        if found_qty and found_price and found_amount:
            return end_index + 1
        end_index += 1
    return None


@window_logger
@log_decorator
def _is_table_footer_line(normalized, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    return any(marker in normalized for marker in TABLE_FOOTER_MARKERS)


@window_logger
@log_decorator
def _is_table_noise_line(normalized, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if normalized in {"#", "_", "# _", "_ #"}:
        return True
    if normalized.startswith("page "):
        return True
    if normalized.startswith("date:") or normalized.startswith("no:"):
        return True
    if "universal transfer document" in normalized:
        return True
    if "продолжение спецификации" in normalized:
        return True
    return False


@window_logger
@log_decorator
def _parse_table_block(block_lines, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    items = []
    index = 0
    while index < len(block_lines):
        line = block_lines[index].strip()
        normalized = _normalize_cell(line)
        if not line or _is_table_noise_line(normalized):
            index += 1
            continue

        row_number = None
        if _looks_like_row_number_line(line):
            row_tokens = _extract_number_tokens(line)
            if row_tokens:
                row_number = row_tokens[0]
            index += 1

        name_lines = []
        while index < len(block_lines):
            line = block_lines[index].strip()
            normalized = _normalize_cell(line)
            if not line or _is_table_noise_line(normalized):
                index += 1
                continue
            if _is_numericish_line(line):
                break
            name_lines.append(line)
            index += 1

        numeric_lines = []
        while index < len(block_lines):
            line = block_lines[index].strip()
            normalized = _normalize_cell(line)
            if not line or _is_table_noise_line(normalized):
                index += 1
                continue
            if not _is_numericish_line(line):
                break
            if numeric_lines and len(numeric_lines) >= 2 and _looks_like_row_number_line(line) and _next_significant_line_is_text(block_lines, index):
                break
            numeric_lines.append(line)
            index += 1

        item = _build_line_item_from_fragments(row_number, name_lines, numeric_lines)
        if item:
            items.append(item)
            continue

        if not name_lines and not numeric_lines:
            index += 1
    return items


@window_logger
@log_decorator
def _looks_like_row_number_line(line, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    stripped = str(line or "").strip()
    if not stripped or "." in stripped or "," in stripped:
        return False
    if not re.fullmatch(r"\d+(?:\s+\d+){0,2}", stripped):
        return False
    tokens = _extract_number_tokens(stripped)
    if not tokens:
        return False
    return all(float(token) < 1000 for token in tokens)


@window_logger
@log_decorator
def _is_numericish_line(line, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    stripped = str(line or "").strip()
    if not stripped:
        return False
    return bool(re.fullmatch(r"[\d\s\.,]+", stripped))


@window_logger
@log_decorator
def _extract_number_tokens(line, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    return re.findall(r"\d+(?:[\.,]\d+)?", str(line or ""))


@window_logger
@log_decorator
def _build_line_item_from_fragments(row_number, name_lines, numeric_lines, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    cleaned_name_lines = [line.strip(" /") for line in name_lines if line.strip(" /")]
    if not cleaned_name_lines:
        return None

    name = " ".join(cleaned_name_lines).strip()
    if not name:
        return None

    numeric_tokens = []
    for line in numeric_lines:
        numeric_tokens.extend(_extract_number_tokens(line))
    if len(numeric_tokens) >= 4 and row_number is not None:
        numeric_tokens = numeric_tokens[-3:]

    quantity = None
    price = None
    amount = None
    if len(numeric_tokens) >= 3:
        quantity = _to_float(_parse_decimal(numeric_tokens[-3]))
        price = _to_float(_parse_decimal(numeric_tokens[-2]))
        amount = _to_float(_parse_decimal(numeric_tokens[-1]))
    elif len(numeric_tokens) == 2:
        price = _to_float(_parse_decimal(numeric_tokens[0]))
        amount = _to_float(_parse_decimal(numeric_tokens[1]))
        quantity = _infer_quantity_from_amount(price, amount)
    else:
        return None

    if amount is None and quantity is not None and price is not None:
        amount = round(quantity * price, 2)
    if amount is None or price is None:
        return None
    if quantity is None:
        quantity = _infer_quantity_from_amount(price, amount)

    return {
        "name": name,
        "quantity": quantity,
        "price": price,
        "amount": amount,
    }


@window_logger
@log_decorator
def _next_significant_line_is_text(lines, current_index, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    next_index = current_index + 1
    while next_index < len(lines):
        normalized = _normalize_cell(lines[next_index])
        if not lines[next_index].strip() or _is_table_noise_line(normalized):
            next_index += 1
            continue
        return not _is_numericish_line(lines[next_index])
    return False


@window_logger
@log_decorator
def _infer_quantity_from_amount(price, amount, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if price is None or amount is None or price == 0:
        return None

    ratio = amount / price
    rounded_integer = round(ratio)
    if abs(ratio - rounded_integer) <= 0.02 and rounded_integer > 0:
        return float(rounded_integer)

    rounded_value = round(ratio, 3)
    if rounded_value > 0 and abs((price * rounded_value) - amount) <= 0.02:
        return float(rounded_value)
    return None


@window_logger
@log_decorator
def _build_tables_from_line_items(line_items, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    rows = [["Наименование", "Количество", "Цена", "Сумма"]]
    for item in line_items:
        rows.append(
            [
                item.get("name") or "",
                _format_numeric_value(item.get("quantity"), trim_trailing_zeros=True),
                _format_numeric_value(item.get("price"), decimals=2),
                _format_numeric_value(item.get("amount"), decimals=2),
            ]
        )
    return [{"table_index": 1, "page_number": 1, "rows": rows}]


@window_logger
@log_decorator
def _format_numeric_value(value, decimals=2, trim_trailing_zeros=False, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if value is None:
        return ""

    if trim_trailing_zeros:
        text = f"{float(value):.{decimals}f}" if decimals is not None else str(value)
        return text.rstrip("0").rstrip(".")
    if decimals is None:
        return str(value)
    return f"{float(value):.{decimals}f}"


@window_logger
@log_decorator
def _extract_vertical_line_items(lines, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    header_index = None
    for index in range(max(0, len(lines) - 3)):
        normalized_chunk = [_normalize_cell(line) for line in lines[index : index + 4]]
        if normalized_chunk == ["item", "quantity", "price", "total"]:
            header_index = index
            break

    if header_index is None:
        return []

    data_lines = []
    for line in lines[header_index + 4 :]:
        normalized = _normalize_cell(line)
        if normalized.startswith("total:") or normalized.startswith("итого") or normalized.startswith("всего"):
            break
        data_lines.append(line)

    items = []
    for index in range(0, len(data_lines), 4):
        chunk = data_lines[index : index + 4]
        if len(chunk) < 4:
            continue

        name = chunk[0].strip()
        if not name:
            continue
        items.append(
            {
                "name": name,
                "quantity": _to_float(_parse_decimal(chunk[1])),
                "price": _to_float(_parse_decimal(chunk[2])),
                "amount": _to_float(_parse_decimal(chunk[3])),
            }
        )
    return items


@window_logger
@log_decorator
def _parse_requisites(full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    return {
        "document_type": _detect_document_type(full_text),
        "document_number": _detect_document_number(full_text),
        "document_date": _detect_document_date(full_text),
        "total_amount": _detect_total_amount(full_text),
        "currency": _detect_currency(full_text),
        "counterparties": _extract_counterparties(full_text),
    }


@window_logger
@log_decorator
def _detect_document_type(full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    text = full_text.lower().replace("ё", "е")
    patterns = [
        ("УПД", ("упд", "универсальный передаточный документ")),
        ("Счет-фактура", ("счет-фактура", "счет фактура")),
        ("Счет", ("счет", "invoice")),
        ("Акт", ("акт",)),
        ("Товарная накладная", ("товарная накладная",)),
        ("Накладная", ("накладная",)),
        ("Договор", ("договор", "contract")),
    ]
    for document_type, keywords in patterns:
        if any(keyword in text for keyword in keywords):
            return document_type
    return None


@window_logger
@log_decorator
def _detect_document_number(full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    lines = [line.strip() for line in full_text.splitlines() if line.strip()]
    candidate_lines = []
    for line in lines[:12]:
        normalized = _normalize_cell(line)
        if any(keyword in normalized for keyword in ("№", "номер", "number", "no", "invoice", "счет", "счёт", "акт", "накладная", "договор", "упд")):
            candidate_lines.append(line)
    candidate_lines.extend(lines[:12])

    patterns = [
        r"(?:№|номер|number|no\.?)\s*[:\-]?\s*([A-Za-zА-Яа-я0-9][A-Za-zА-Яа-я0-9\-\/]{0,63})",
        r"(?:invoice|счет\-фактура|счет фактура|счет|сч[её]т|акт|накладная|договор|упд)\s+(?:№|номер|number|no\.?)?\s*[:\-]?\s*([A-Za-zА-Яа-я0-9][A-Za-zА-Яа-я0-9\-\/]{0,63})",
    ]
    for line in candidate_lines:
        for pattern in patterns:
            for match in re.finditer(pattern, line, flags=re.IGNORECASE):
                candidate = match.group(1).strip()
                if _is_valid_document_number(candidate):
                    return candidate
    return None


@window_logger
@log_decorator
def _is_valid_document_number(candidate, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    value = str(candidate or "").strip()
    if not value:
        return False

    normalized = value.lower()
    if normalized in DOCUMENT_NUMBER_STOPWORDS:
        return False
    if re.fullmatch(r"\d{2}[\.\-/]\d{2}[\.\-/]\d{4}", value):
        return False
    if normalized in {"инн", "кпп"}:
        return False
    return bool(re.search(r"\d", value) or len(value) >= 3)


@window_logger
@log_decorator
def _detect_document_date(full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    patterns = [
        r"\b(\d{2}\.\d{2}\.\d{4})\b",
        r"\b(\d{2}/\d{2}/\d{4})\b",
        r"\b(\d{4}-\d{2}-\d{2})\b",
    ]

    lines = [line.strip() for line in full_text.splitlines() if line.strip()]
    for line in lines[:12]:
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(1)

    for pattern in patterns:
        match = re.search(pattern, full_text)
        if match:
            return match.group(1)
    return None


@window_logger
@log_decorator
def _detect_total_amount(full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    lines = [line.strip() for line in full_text.splitlines() if line.strip()]
    amount_pattern = re.compile(r"(?:\d{1,3}(?:[ \u00A0]\d{3})+|\d+)(?:[\.,]\d{2})?")

    for line in reversed(lines):
        normalized = line.lower().replace("ё", "е")
        if any(keyword in normalized for keyword in ("итого", "всего", "к оплате", "сумма", "total")):
            matches = amount_pattern.findall(line)
            if matches:
                return _to_float(_parse_decimal(matches[-1]))
    return None


@window_logger
@log_decorator
def _detect_currency(full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    normalized = full_text.lower()
    if any(token in normalized for token in ("руб", "rur", "rub")):
        return "RUB"
    if any(token in normalized for token in ("usd", "$")):
        return "USD"
    if any(token in normalized for token in ("eur", "€")):
        return "EUR"
    return None


@window_logger
@log_decorator
def _extract_counterparties(full_text, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    lines = [line.strip() for line in full_text.splitlines() if line.strip()]
    entries = _extract_counterparty_entries(lines)
    if not entries:
        return []

    role_hints = _extract_role_hints(lines)
    name_candidates = _extract_name_candidates(lines, role_hints)
    ordered_name_candidates = _build_ordered_name_candidates(entries, name_candidates, role_hints)
    results = []
    seen = set()
    used_name_indexes = set()

    for position, entry in enumerate(entries):
        inline_name = _extract_inline_counterparty_name(lines[entry["line_index"]])
        candidate = None if inline_name else _select_name_candidate_for_entry(entry, position, entries, name_candidates, used_name_indexes, ordered_name_candidates)
        name = inline_name or (candidate["name"] if candidate else _extract_counterparty_name(lines, entry["line_index"]))
        role = candidate["role"] if candidate else "unknown"
        if candidate:
            used_name_indexes.add(candidate["line_index"])

        if role == "unknown":
            role = _guess_role_near_index(lines, entry["line_index"], role_hints)
        if role == "unknown" and position < len(role_hints):
            role = role_hints[position]["role"]
        if role == "unknown":
            role = _guess_role_from_hints(entry["line_index"], role_hints)

        key = (entry["inn"], entry["kpp"], name, role)
        if key in seen:
            continue
        seen.add(key)
        results.append(
            {
                "role": role,
                "name": name,
                "inn": entry["inn"],
                "kpp": entry["kpp"],
            }
        )

    return results


@window_logger
@log_decorator
def _extract_counterparty_entries(lines, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    entries = []
    for index, line in enumerate(lines):
        inn_match = re.search(r"(?:инн|inn)\s*[:№]?\s*(\d{10}|\d{12})", line, flags=re.IGNORECASE)
        if not inn_match:
            continue
        entries.append(
            {
                "line_index": index,
                "inn": inn_match.group(1),
                "kpp": _extract_kpp(lines, index),
            }
        )
    return entries


@window_logger
@log_decorator
def _extract_role_hints(lines, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    hints = []
    for index, line in enumerate(lines):
        role = _guess_counterparty_role(line)
        if role != "unknown":
            hints.append({"line_index": index, "role": role})
    return hints


@window_logger
@log_decorator
def _extract_name_candidates(lines, role_hints, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    candidates = []
    for index, line in enumerate(lines):
        if not _is_org_name_line(line):
            continue
        cleaned_name = _cleanup_counterparty_text(line)
        if not cleaned_name:
            continue
        candidates.append(
            {
                "line_index": index,
                "name": cleaned_name,
                "role": _guess_counterparty_role(line),
            }
        )
    return candidates


@window_logger
@log_decorator
def _is_org_name_line(line, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    candidate = str(line or "").strip()
    normalized = _normalize_cell(candidate)
    if not candidate:
        return False
    if any(marker in normalized for marker in NON_ORG_LINE_MARKERS):
        return False
    if re.search(r"(?:инн|кпп|inn|kpp)\s*[:№]?\s*\d", normalized):
        return False
    if not re.search(r"[A-Za-zА-Яа-я]", candidate):
        return False
    if ORG_MARKER_PATTERN.search(candidate):
        return True
    return any(mark in candidate for mark in ('"', "«", "»")) and len(candidate.split()) >= 2


@window_logger
@log_decorator
def _normalize_org_name_text(line, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    cleaned = str(line or "").strip()
    replacements = {
        r"^OOO\b": "ООО",
        r"^AO\b": "АО",
        r"^PAO\b": "ПАО",
        r"^OAO\b": "ОАО",
        r"^ZAO\b": "ЗАО",
        r"^IP\b": "ИП",
    }
    for pattern, replacement in replacements.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
    return cleaned


@window_logger
@log_decorator
def _cleanup_counterparty_text(line, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    cleaned = re.sub(
        r"(?:продавец|покупатель|заказчик|поставщик|исполнитель|seller|buyer|customer|vendor|supplier)\s*[:\-]?\s*",
        "",
        str(line or ""),
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"(?:инн|inn)\s*[:№]?\s*\d{10,12}", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(?:кпп|kpp)\s*[:№]?\s*\d{9}", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip(" ,;:-")
    return _normalize_org_name_text(cleaned)


@window_logger
@log_decorator
def _guess_role_from_hints(index, role_hints, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if not role_hints:
        return "unknown"

    nearest_hint = min(
        role_hints,
        key=lambda hint: (abs(hint["line_index"] - index), 0 if hint["line_index"] <= index else 1),
    )
    return nearest_hint["role"]


@window_logger
@log_decorator
def _build_ordered_name_candidates(entries, name_candidates, role_hints, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if len(name_candidates) < len(entries):
        return []

    first_entry_index = entries[0]["line_index"] if entries else 0
    ordered_candidates = [dict(candidate) for candidate in name_candidates if candidate["line_index"] < first_entry_index]
    if len(ordered_candidates) < len(entries):
        return []

    ordered_candidates = ordered_candidates[: len(entries)]
    for index, candidate in enumerate(ordered_candidates):
        if index < len(role_hints):
            candidate["role"] = role_hints[index]["role"]
    return ordered_candidates


@window_logger
@log_decorator
def _select_name_candidate_for_entry(entry, position, entries, name_candidates, used_name_indexes, ordered_name_candidates=None, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if ordered_name_candidates and position < len(ordered_name_candidates):
        candidate = ordered_name_candidates[position]
        if candidate["line_index"] not in used_name_indexes:
            return candidate

    local_candidates = [
        candidate
        for candidate in name_candidates
        if candidate["line_index"] not in used_name_indexes and abs(candidate["line_index"] - entry["line_index"]) <= 2
    ]
    if local_candidates:
        return min(local_candidates, key=lambda candidate: abs(candidate["line_index"] - entry["line_index"]))

    if len(name_candidates) >= len(entries) and position < len(name_candidates):
        candidate = name_candidates[position]
        if candidate["line_index"] not in used_name_indexes:
            return candidate

    unused_candidates = [candidate for candidate in name_candidates if candidate["line_index"] not in used_name_indexes]
    if not unused_candidates:
        return None

    return min(unused_candidates, key=lambda candidate: abs(candidate["line_index"] - entry["line_index"]))


@window_logger
@log_decorator
def _guess_role_near_index(lines, index, role_hints, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    candidate_indexes = [index]
    if index > 0:
        candidate_indexes.append(index - 1)
    if index + 1 < len(lines):
        candidate_indexes.append(index + 1)
    for line_index in candidate_indexes:
        role = _guess_counterparty_role(lines[line_index])
        if role != "unknown":
            return role
    return "unknown"


@window_logger
@log_decorator
def _extract_inline_counterparty_name(line, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if not re.search(r"(?:инн|inn)\s*[:№]?\s*\d{10,12}", str(line or ""), flags=re.IGNORECASE):
        return None

    cleaned = _cleanup_counterparty_text(line)
    if not cleaned:
        return None

    normalized = _normalize_cell(cleaned)
    if ORG_MARKER_PATTERN.search(cleaned) or any(mark in cleaned for mark in ('"', "«", "»")):
        return cleaned
    if len(normalized.split()) >= 2 and re.search(r"[A-Za-zА-Яа-я]", cleaned):
        return cleaned
    return None


@window_logger
@log_decorator
def _extract_kpp(lines, index, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    window = []
    if 0 <= index < len(lines):
        window.append(lines[index])
    if index > 0:
        window.append(lines[index - 1])
    if index + 1 < len(lines):
        window.append(lines[index + 1])

    for line in window:
        match = re.search(r"(?:кпп|kpp)\s*[:№]?\s*(\d{9})", line, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


@window_logger
@log_decorator
def _extract_counterparty_name(lines, index, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    for candidate_index in (index, index - 1, index + 1, index - 2, index + 2):
        if candidate_index < 0 or candidate_index >= len(lines):
            continue
        candidate = lines[candidate_index]
        if not _is_org_name_line(candidate):
            continue
        cleaned = _cleanup_counterparty_text(candidate)
        normalized = cleaned.lower().replace("ё", "е")
        if not cleaned:
            continue
        if ORG_MARKER_PATTERN.search(cleaned) or any(mark in cleaned for mark in ('"', "«", "»")):
            return cleaned
    return None


@window_logger
@log_decorator
def _guess_counterparty_role(context, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    normalized = str(context or "").lower().replace("ё", "е")
    for role, keywords in COUNTERPARTY_ROLE_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return role
    return "unknown"


@window_logger
@log_decorator
def _parse_decimal(value, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if value is None:
        return None

    cleaned = str(value).strip()
    if not cleaned:
        return None

    cleaned = cleaned.replace("\u00A0", " ").replace(" ", "")
    cleaned = re.sub(r"[^0-9,.-]", "", cleaned)
    if cleaned.count(",") > 1 and "." not in cleaned:
        cleaned = cleaned.replace(",", "")
    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    else:
        cleaned = cleaned.replace(",", ".")

    try:
        return decimal.Decimal(cleaned)
    except decimal.InvalidOperation:
        return None


@window_logger
@log_decorator
def _to_float(value, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    if value is None:
        return None
    return float(value)


@window_logger
@log_decorator
def _to_base64(content, puzzle_logger_path=None, block_text=None, block_id=None, window_log=False, **kwargs):
    return base64.b64encode(content).decode("ascii")
