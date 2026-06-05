# telegram-bridge

> ⚠️ **ALPHA — EXPERIMENTAL SOFTWARE**
>
> This project is in early development and is shared for personal use and learning purposes only.
> It is not production-ready. Use it at your own risk. No support or guarantees are provided.

A lightweight Telegram userbot that listens for incoming messages on a personal account and triggers n8n webhooks when specific patterns are matched.

## How it works

- Runs as a Docker container
- Uses [Telethon](https://github.com/LonamiWebs/Telethon) (MTProto) to listen to your personal Telegram account
- When a message matches the configured patterns, POSTs to an n8n webhook URL
- Designed to be a generic, reusable bridge between Telegram notifications and n8n workflows

## Setup

### 1. Telegram API credentials

Go to [my.telegram.org](https://my.telegram.org) → API development tools → create an app.
Copy your `api_id` and `api_hash`.

### 2. Configure environment

```bash
cp .env.example .env
# fill in TG_API_ID, TG_API_HASH and N8N_WEBHOOK_URL
```

### 3. First-time authentication (interactive)

```bash
docker compose run --rm telegram-bridge
# enter your phone number and the verification code Telegram sends you
# press Ctrl+C once you see "Escuchando mensajes..."
```

The session is saved to `./data/session.session` and reused on every subsequent start.

### 4. Run

```bash
docker compose up -d
```

## Configuration

| Variable | Required | Description |
|---|---|---|
| `TG_API_ID` | yes | Telegram API ID from my.telegram.org |
| `TG_API_HASH` | yes | Telegram API Hash from my.telegram.org |
| `N8N_WEBHOOK_URL` | yes | Full URL of the n8n webhook to trigger |
| `FACILITY_BOT_ID` | no | Telegram user ID of the sender to filter by |
