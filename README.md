# bmat-watcher

GitHub Actions раз в 2 часа (08:00-20:00 Минск) опрашивает
https://queue.bmat.by/api/transport/svh и ищет заданные строки (переменная `NEEDLES`).
Результат шлёт в Telegram. При находке - сообщение и автоотключение workflow.

## Настройка
1. Создать бота у @BotFather -> `TG_BOT_TOKEN`; написать боту любое сообщение,
   chat_id взять из https://api.telegram.org/bot<TOKEN>/getUpdates -> `TG_CHAT_ID`.
2. Создать репозиторий на GitHub, запушить проект.
3. Settings -> Secrets and variables -> Actions: добавить `TG_BOT_TOKEN`, `TG_CHAT_ID`.
4. Settings -> Secrets and variables -> Actions -> Variables: добавить `NEEDLES`
   со значением JSON-массива, например `["строка1", "строка2"]`.
5. Actions -> watch -> Run workflow - проверить вручную.

Перезапуск после находки: Actions -> watch -> Enable workflow.
