# ha-config/configuration.md
# Что добавить в configuration.yaml

Если автоматизации у тебя подключены через единый файл, убедись что в
`configuration.yaml` есть:

```yaml
automation: !include automations.yaml
```

Если используешь папку:

```yaml
automation: !include_dir_merge_list automations/
```

Больше ничего в configuration.yaml добавлять не нужно —
webhook-триггер не требует отдельной настройки.