# telegram-bridge

> ⚠️ **ALPHA — EXPERIMENTAL SOFTWARE**
>
> This project is in early development and is shared for personal use and learning purposes only.
> It is not production-ready. Use it at your own risk. No support or guarantees are provided.

A lightweight Telegram userbot that listens for incoming messages on a personal account and triggers n8n webhooks when specific patterns are matched.

Designed to run as a Docker container on the same host as a self-hosted n8n instance (e.g. a Proxmox LXC), calling n8n webhooks over the local network.

## How it works

- Runs as a Docker container
- Uses [Telethon](https://github.com/LonamiWebs/Telethon) (MTProto) to listen to your **personal** Telegram account — not a bot token
- When an incoming message matches all configured `TARGET_PHRASES`, POSTs to `N8N_WEBHOOK_URL`
- Optionally filters by sender ID (`FACILITY_BOT_ID`) to avoid false positives

## Requirements

- Docker + Docker Compose
- A Telegram account
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/mtnezdilarduya/telegram-bridge.git
cd telegram-bridge
```

### 2. Telegram API credentials

Go to [my.telegram.org](https://my.telegram.org) → API development tools → create an app.
Copy your `App api_id` and `App api_hash`.

### 3. Configure environment

```bash
cp .env.example .env
# fill in TG_API_ID, TG_API_HASH and N8N_WEBHOOK_URL
```

### 4. Build

```bash
docker compose build
```

### 5. First-time authentication (interactive, only once)

```bash
docker compose run --rm telegram-bridge
# enter your phone number (with country code, e.g. +34612345678)
# then the verification code Telegram sends you
# press Ctrl+C once you see "Escuchando mensajes..."
```

The session is saved to `./data/session.session` and reused automatically on every subsequent start.

### 6. Run

```bash
docker compose up -d
```

## Configuration

| Variable | Required | Description |
|---|---|---|
| `TG_API_ID` | yes | Telegram API ID from my.telegram.org |
| `TG_API_HASH` | yes | Telegram API Hash from my.telegram.org |
| `N8N_WEBHOOK_URL` | yes | Full URL of the n8n webhook to trigger |
| `FACILITY_BOT_ID` | no | Numeric Telegram ID of the expected sender. Forward a message from them to @userinfobot to get it. Leave empty to match any sender. |

## Customising the trigger

Edit `TARGET_PHRASES` in `monitor.py` to match whatever message text should trigger your webhook:

```python
TARGET_PHRASES = [
    "phrase one",
    "phrase two",
]
```

All phrases must be present in the message for it to trigger.

## Project structure

```
telegram-bridge/
├── monitor.py          # Telethon listener
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── data/               # gitignored — session file lives here
```
