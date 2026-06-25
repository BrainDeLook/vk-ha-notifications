# VK → Home Assistant Notifications

Push-уведомления о новых сообщениях ВКонтакте через Home Assistant Companion App для iOS.

## Как это работает

```
VK API (polling каждые 30 сек)
        ↓
  Home Assistant (REST sensor)
        ↓
  Автоматизация (при изменении счётчика)
        ↓
  Companion App → Push на iPhone
        ↓
  Нажатие → открывает vk://im
```

## Структура

```
ha-config/
  sensors.yaml          — REST-сенсор опроса VK API
  automations.yaml      — автоматизация отправки уведомления
  secrets_example.yaml  — пример секретов (токен VK)
docs/
  setup.md              — пошаговая инструкция
  vk-token.md           — как получить токен VK
```

## Быстрый старт

1. Получи VK токен — см. [docs/vk-token.md](docs/vk-token.md)
2. Добавь токен в `secrets.yaml` Home Assistant
3. Скопируй файлы из `ha-config/` в свой конфиг HA
4. Перезапусти Home Assistant
5. Установи [Home Assistant Companion App](https://apps.apple.com/app/home-assistant/id1099568401) на iPhone

## Требования

- Home Assistant 2023.1+
- Home Assistant Companion App на iPhone
- Токен VK с правами: `messages`, `offline`