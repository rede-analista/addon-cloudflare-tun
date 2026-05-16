# addon-cloudflare-tun

Home Assistant addon to expose multiple local services via Cloudflare Tunnel with automatic DNS configuration.

## Requirements

- A domain managed by Cloudflare
- A Cloudflare API Token with permissions:
  - **Account > Cloudflare Tunnel: Edit**
  - **Zone > DNS: Edit** (for each zone you use)
- Your Cloudflare Account ID (visible in the dashboard sidebar)

## Configuration

| Option | Description |
|--------|-------------|
| `api_token` | Cloudflare API Token |
| `account_id` | Cloudflare Account ID |
| `tunnel_name` | Name for the tunnel (created automatically) |
| `services` | List of services to expose |

Each service entry:

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Friendly name | `Home Assistant` |
| `hostname` | Public hostname | `ha.example.com` |
| `service` | Internal URL | `http://homeassistant:8123` |

## How it works

On startup the addon:
1. Creates the Cloudflare Tunnel (or reuses it if credentials are saved in `/data`)
2. Creates/updates a CNAME DNS record for each service pointing to the tunnel
3. Generates the cloudflared config and starts the tunnel

Tunnel credentials are persisted in `/data/tunnel-credentials.json` and reused on restart.

## Troubleshooting

**"Tunnel already exists but no local credentials found"**
Delete the tunnel from the Cloudflare dashboard (Zero Trust > Networks > Tunnels) and restart the addon.

## Installation

Add this repository URL to Home Assistant Add-on Store:
`https://github.com/rede-analista/addon-cloudflare-tun`
