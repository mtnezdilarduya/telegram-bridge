"""
Monitor de mensajes de Telegram.
Detecta cuando el bot de fuencarraltm.es avisa de plaza libre
y dispara el webhook de n8n para lanzar la reserva automática.

Primera ejecución: pide número de teléfono y código de verificación.
El token de sesión queda guardado en session.session para siempre.
"""

import asyncio
import logging
import os

import aiohttp
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

API_ID           = int(os.environ["TG_API_ID"])
API_HASH         = os.environ["TG_API_HASH"]
N8N_WEBHOOK_URL  = os.environ["N8N_WEBHOOK_URL"]
FACILITY_BOT_ID  = int(os.environ.get("FACILITY_BOT_ID", "0"))  # 0 = sin filtro de remitente

TARGET_PHRASES = [
    "Alguien se ha desapuntado",
    "Sábado Escuela 09:00 a 11:00",
    "Quedan plazas libres",
]

client = TelegramClient("/data/session", API_ID, API_HASH)


def matches_target(text: str) -> bool:
    return all(phrase in text for phrase in TARGET_PHRASES)


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    text = event.message.message or ""
    if not matches_target(text):
        return

    if FACILITY_BOT_ID and event.sender_id != FACILITY_BOT_ID:
        log.info("Mensaje coincide pero remitente %s != %s esperado", event.sender_id, FACILITY_BOT_ID)
        return

    log.info("¡Plaza libre detectada! Disparando webhook de n8n...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(N8N_WEBHOOK_URL, json={"source": "telegram_monitor"}) as resp:
                log.info("n8n respondió con status %s", resp.status)
    except Exception as exc:
        log.error("Error al llamar al webhook: %s", exc)


async def main():
    await client.start()
    me = await client.get_me()
    log.info("Sesión iniciada como @%s. Escuchando mensajes...", me.username or me.id)
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
