#!/usr/bin/with-contenv bashio

bashio::log.info "Cloudflare Tunnel Manager starting..."

python3 /cloudflare_api.py
if [ $? -ne 0 ]; then
    bashio::log.error "Failed to configure Cloudflare. Check your api_token and account_id."
    exit 1
fi

python3 /generate_config.py
if [ $? -ne 0 ]; then
    bashio::log.error "Failed to generate cloudflared config."
    exit 1
fi

bashio::log.info "Starting cloudflared..."
exec cloudflared tunnel --no-autoupdate --config /tmp/cloudflared.yml run
