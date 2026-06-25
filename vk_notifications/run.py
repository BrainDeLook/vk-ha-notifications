import asyncio
import json
import logging
import os
import sys

import aiohttp
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

OPTIONS_PATH = "/data/options.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("vk-notifications")


def load_options():
    with open(OPTIONS_PATH) as f:
        return json.load(f)


async def notify_ha(session: aiohttp.ClientSession, ha_url: str, webhook_id: str, data: dict):
    url = f"{ha_url}/api/webhook/{webhook_id}"
    try:
        async with session.post(url, json=data, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status == 200:
                log.info("Webhook отправлен: %s", data)
            else:
                log.warning("Webhook вернул статус %s", resp.status)
    except Exception as e:
        log.error("Ошибка отправки webhook: %s", e)


def get_sender_name(vk: vk_api.VkApi, user_id: int) -> str:
    try:
        if user_id < 0:
            groups = vk.method("groups.getById", {"group_id": abs(user_id)})
            if groups:
                return groups[0].get("name", "Группа")
        else:
            users = vk.method("users.get", {"user_ids": user_id})
            if users:
                u = users[0]
                return f"{u.get("first_name", "")} {u.get("last_name", "")}".strip()
    except Exception as e:
        log.warning("Не удалось получить имя отправителя: %s", e)
    return "Новое сообщение"


async def run_longpoll(options: dict):
    token = options["vk_access_token"]
    ha_url = options["ha_url"].rstrip("/")
    webhook_id = options["ha_webhook_id"]
    log_level = options.get("log_level", "info").upper()

    logging.getLogger().setLevel(getattr(logging, log_level, logging.INFO))

    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    log.info("VK Long Poll запущен, ожидаю сообщения...")

    async with aiohttp.ClientSession() as session:
        loop = asyncio.get_event_loop()

        def poll():
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    sender = get_sender_name(vk, event.user_id)
                    text_preview = event.text[:50] if event.text else "..."
                    log.info("Новое сообщение от %s: %s", sender, text_preview)
                    asyncio.run_coroutine_threadsafe(
                        notify_ha(session, ha_url, webhook_id, {
                            "sender": sender,
                            "user_id": event.user_id,
                            "text": text_preview,
                        }),
                        loop,
                    ).result()

        await loop.run_in_executor(None, poll)


def main():
    options = load_options()

    if not options.get("vk_access_token"):
        log.error("vk_access_token не задан в настройках аддона")
        sys.exit(1)

    if not options.get("ha_webhook_id"):
        log.error("ha_webhook_id не задан в настройках аддона")
        sys.exit(1)

    asyncio.run(run_longpoll(options))


if __name__ == "__main__":
    main()