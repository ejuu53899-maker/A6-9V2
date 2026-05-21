# Secrets & Credentials Management

This project requires certain credentials to fully function. **Do not commit these values to the repository.**

## Environment Variables (CI/CD & Scripts)

When running deployment scripts, use environment variables in your `.env` file or export them.

### Firefox Relay
- `SCRSOR`: Firefox Relay profile API key (`https://relay.firefox.com/accounts/profile/`).
- `COPILOT`: Same as `SCRSOR`.

### Telegram Bot
- `TELEGRAM_BOT_NAME`: The t.me link to your bot (e.g., `t.me/GenX_FX_bot`).
- `TELEGRAM_BOT_API`: Your bot token from @BotFather.
- `TELEGRAM_BOT_TOKEN`: Same as `TELEGRAM_BOT_API`.
- `TELEGRAM_ALLOWED_USER_IDS`: Comma-separated list of authorized user IDs.

### Cloudflare
- `CLOUDFLARE_ZONE_ID`: Your Cloudflare Zone ID.
- `CLOUDFLARE_ACCOUNT_ID`: Your Cloudflare Account ID.
- `DOMAIN_NAME`: Your primary domain (e.g., `lengkundee01.org`).

### Docker Hub
- `DOCKER_USERNAME`: Your Docker Hub username.
- `DOCKER_PASSWORD`: Your Docker Hub access token or password.

Example:
```bash
export DOCKER_USERNAME="your_user"
export DOCKER_PASSWORD="your_token"
./scripts/update_vps.sh
```

## MQL5 Expert Advisor Inputs

When configuring the EAs in MetaTrader 5, use the Inputs tab. Do not hardcode these in `.mq5` files.

- **GeminiApiKey**: Your Google Gemini API Key.
- **WebRequestURL**: The ZOLO Bridge URL.

## Windows Credential Manager

For local automation, store sensitive tokens in Windows Credential Manager if required by custom scripts.
