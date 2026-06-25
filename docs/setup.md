# Полная инструкция по установке

## Что нам нужно

- Android телефон дома с установленным ВКонтакте
- MacroDroid на Android
- Home Assistant в локальной сети (`192.168.1.145`)
- HA Companion App на iPhone (уже установлен)

---

## Шаг 1 — Добавь автоматизацию в Home Assistant

Скопируй файл `ha-config/automations.yaml` в свой конфиг.

**Важно:** замени `notify.mobile_app_iphone` на имя своего устройства.

Найти имя: **Настройки → Мобильное приложение → твоё устройство**.
Имя сервиса обычно выглядит как `notify.mobile_app_имя_телефона`.

После добавления перезапусти HA: **Настройки → Система → Перезапуск**.

---

## Шаг 2 — Установи MacroDroid на Android

[Скачать MacroDroid](https://play.google.com/store/apps/details?id=com.arlosoft.macrodroid)

---

## Шаг 3 — Настрой макрос в MacroDroid

Подробная инструкция: [macrodroid/macro.md](../macrodroid/macro.md)

Коротко:
- Триггер: уведомление от приложения **ВКонтакте**
- Действие: HTTP POST на `http://192.168.1.145:8123/api/webhook/vk_new_message`
- Тело: `{"title": "{notification_title}", "text": "{notification_text}"}`

---

## Шаг 4 — Выдай разрешение на чтение уведомлений

**Настройки Android → Уведомления → Доступ к уведомлениям → MacroDroid → Включить**

---

## Шаг 5 — Тест

1. Напиши себе в ВК с другого аккаунта
2. MacroDroid перехватит уведомление на Android
3. Отправит webhook в HA
4. HA пришлёт push на iPhone мгновенно
5. Нажатие на push → открывается ВКонтакте

---

## Если что-то не работает

**Push не приходит:**
- Проверь что макрос MacroDroid активен (зелёный переключатель)
- Проверь разрешение на доступ к уведомлениям
- Открой MacroDroid → Журнал макросов — посмотри был ли запуск

**Webhook не доходит до HA:**
- Проверь IP: откройся в браузере `http://192.168.1.145:8123` — должен открыться HA
- Проверь что Android в той же WiFi сети

**Имя сервиса уведомлений:**
- В HA: Настройки → Интеграции → Мобильное приложение → твоё устройство
- Там будет точное имя сервиса

---

## Использование несколькими людьми

Каждый человек:
1. Устанавливает HA Companion App на свой iPhone
2. В `automations.yaml` добавляется ещё один `service` вызов с его именем устройства
3. На его Android устанавливается MacroDroid с тем же макросом

Пример для двух людей в `automations.yaml`:
```yaml
action:
  - service: notify.mobile_app_iphone_человек1
    data:
      title: "{{ trigger.json.title | default(\"ВКонтакте\") }}"
      message: "{{ trigger.json.text | default(\"Новое сообщение\") }}"
      data:
        url: "vkontakte://vk.com/im"
  - service: notify.mobile_app_iphone_человек2
    data:
      title: "{{ trigger.json.title | default(\"ВКонтакте\") }}"
      message: "{{ trigger.json.text | default(\"Новое сообщение\") }}"
      data:
        url: "vkontakte://vk.com/im"
```