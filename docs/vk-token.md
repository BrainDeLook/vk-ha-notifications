# Как получить токен VK

Для работы сенсора нужен **Standalone-токен** с правами `messages` и `offline`.

## Способ через vk.com/dev

1. Перейди на https://vk.com/dev/standalone
2. Создай новое Standalone-приложение (тип: "Standalone")
3. Запомни **ID приложения** (app_id)

## Получение токена через браузер

Открой в браузере эту ссылку, подставив свой `app_id`:

```
https://oauth.vk.com/authorize?client_id=ВАШ_APP_ID&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=messages,offline&response_type=token&v=5.199
```

После авторизации тебя перенаправит на страницу вида:

```
https://oauth.vk.com/blank.html#access_token=ВАШ_ТОКЕН&expires_in=0&user_id=...
```

Скопируй значение `access_token` — это и есть токен.

## Права токена

- `messages` — чтение сообщений
- `offline` — токен не истекает (бессрочный)

## Безопасность

- Храни токен только в `secrets.yaml`
- Никогда не публикуй токен в открытых репозиториях
- Токен даёт доступ к сообщениям — не передавай его третьим лицам