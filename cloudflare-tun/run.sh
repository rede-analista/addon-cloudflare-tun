#!/usr/bin/env bash
set -e

echo "INFO: Cloudflare Tunnel Manager starting..."

python3 -u /cloudflare_api.py || { echo "ERROR: Cloudflare API configuration failed. Check api_token and account_id."; exit 1; }
python3 -u /generate_config.py || { echo "ERROR: Config generation failed."; exit 1; }

echo "INFO: Starting cloudflared..."
exec cloudflared tunnel --no-autoupdate --config /tmp/cloudflared.yml run
