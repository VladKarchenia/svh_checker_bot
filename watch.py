"""Проверяет ответ API на наличие искомых строк и уведомляет в Telegram.

Если строка найдена - шлёт сообщение и отключает workflow (см. watch.yml).
Только стандартная библиотека.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

URL = "https://queue.bmat.by/api/transport/svh"
# JSON-массив строк в переменной окружения NEEDLES, например ["Шукалович", "Shukalovich"]
# Сравнение без учёта регистра
NEEDLES = [n.lower() for n in json.loads(os.environ["NEEDLES"])]
FOUND_FLAG = "found.flag"  # файл-маркер для workflow


def telegram(text: str) -> None:
    token = os.environ["TG_BOT_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    with urllib.request.urlopen(
        f"https://api.telegram.org/bot{token}/sendMessage", data=data, timeout=30
    ) as resp:
        resp.read()


def fetch() -> str:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
    json.loads(body)  # убеждаемся, что это валидный JSON
    return body


def main() -> int:
    try:
        body = fetch()
    except Exception as e:  # сеть/5xx/не JSON - это не "не найдено"
        telegram(f"⚠️ Ошибка запроса к API: {e}")
        return 1

    haystack = body.lower()
    # json.loads/dumps с ensure_ascii=False не нужен: ищем и в сыром тексте,
    # и в варианте с \uXXXX-экранированием
    haystack += json.dumps(json.loads(body), ensure_ascii=False).lower()
    hits = [n for n in NEEDLES if n in haystack]

    if hits:
        telegram(f"✅ Найдено: {', '.join(hits)}\n{URL}\nПроверки остановлены.")
        open(FOUND_FLAG, "w").close()
    else:
        telegram(f"🔎 Пока не найдено: {' / '.join(NEEDLES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
