# VK → Home Assistant Notifications

Мгновенные push-уведомления о новых сообщениях ВКонтакте на iPhone через Home Assistant.

## Как это работает

```
ВКонтакте (Android, дома)
        ↓ уведомление
   MacroDroid
        ↓ POST webhook (локальная сеть)
   Home Assistant
        ↓
   Companion App → Push на iPhone
        ↓ нажатие
   Открывается ВКонтакте
```

## Требования

- Android телефон дома с установленным ВКонтакте
- [MacroDroid](https://play.google.com/store/apps/details?id=com.arlosoft.macrodroid) на Android (бесплатно)
- Home Assistant в локальной сети
- [HA Companion App](https://apps.apple.com/app/home-assistant/id1099568401) на iPhone

## Установка

См. [docs/setup.md](docs/setup.md)

## Структура репозитория

```
ha-config/
  automations.yaml     — автоматизация webhook → push на iPhone
  configuration.md     — что добавить в configuration.yaml
macrodroid/
  macro.md             — инструкция по настройке MacroDroid
docs/
  setup.md             — полная пошаговая инструкция
```