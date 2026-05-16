#!/usr/bin/env python3
import json
import os
import sys
import requests

OPTIONS_FILE = "/data/options.json"
CREDENTIALS_FILE = "/data/tunnel-credentials.json"
TUNNEL_ID_FILE = "/tmp/tunnel_id"
CF_API = "https://api.cloudflare.com/client/v4"


def load_options():
    with open(OPTIONS_FILE) as f:
        return json.load(f)


def headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def api_get(token, path):
    resp = requests.get(f"{CF_API}{path}", headers=headers(token))
    resp.raise_for_status()
    return resp.json()


def api_post(token, path, body):
    resp = requests.post(f"{CF_API}{path}", headers=headers(token), json=body)
    resp.raise_for_status()
    return resp.json()


def api_patch(token, path, body):
    resp = requests.patch(f"{CF_API}{path}", headers=headers(token), json=body)
    resp.raise_for_status()
    return resp.json()


def api_delete(token, path):
    resp = requests.delete(f"{CF_API}{path}", headers=headers(token))
    resp.raise_for_status()
    return resp.json()


def get_zone_id(token, hostname):
    parts = hostname.split(".")
    # Tenta 2 partes (ex: example.com) e depois 3 (ex: pensenet.com.br)
    for n in [2, 3]:
        if len(parts) < n:
            continue
        domain = ".".join(parts[-n:])
        data = api_get(token, f"/zones?name={domain}")
        if data["success"] and data["result"]:
            return data["result"][0]["id"]
    print(f"ERROR: Zone não encontrada para '{hostname}'. Verifique se o domínio está gerenciado por esta conta Cloudflare.", file=sys.stderr)
    sys.exit(1)


def verify_tunnel(token, account_id, tunnel_id):
    try:
        data = api_get(token, f"/accounts/{account_id}/cfd_tunnel/{tunnel_id}")
        return data["success"] and not data["result"].get("deleted_at")
    except Exception:
        return False


def create_tunnel(token, account_id, tunnel_name):
    data = api_post(token, f"/accounts/{account_id}/cfd_tunnel", {
        "name": tunnel_name,
        "config_src": "local"
    })
    if not data["success"]:
        print(f"ERROR: Failed to create tunnel: {data['errors']}", file=sys.stderr)
        sys.exit(1)
    tunnel = data["result"]
    creds = tunnel["credentials_file"]
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(creds, f)
    print(f"Tunnel '{tunnel_name}' created: {tunnel['id']}")
    return tunnel["id"]


def get_or_create_tunnel(token, account_id, tunnel_name):
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE) as f:
            creds = json.load(f)
        tunnel_id = creds.get("TunnelID") or creds.get("tunnel_id", "")
        if tunnel_id and verify_tunnel(token, account_id, tunnel_id):
            print(f"Reusing existing tunnel: {tunnel_id}")
            return tunnel_id
        print("Saved tunnel no longer valid, creating a new one...")

    data = api_get(token, f"/accounts/{account_id}/cfd_tunnel?name={tunnel_name}&is_deleted=false")
    if data["success"] and data["result"]:
        existing_id = data["result"][0]["id"]
        print(f"ERROR: Tunnel '{tunnel_name}' already exists (ID: {existing_id}) but no local credentials found.", file=sys.stderr)
        print("Delete the tunnel from the Cloudflare dashboard and restart the addon.", file=sys.stderr)
        sys.exit(1)

    return create_tunnel(token, account_id, tunnel_name)


def ensure_dns_record(token, zone_id, hostname, tunnel_id):
    cname_target = f"{tunnel_id}.cfargotunnel.com"
    data = api_get(token, f"/zones/{zone_id}/dns_records?type=CNAME&name={hostname}")

    if data["success"] and data["result"]:
        record = data["result"][0]
        if record["content"] == cname_target:
            print(f"  DNS {hostname}: already correct")
            return
        api_patch(token, f"/zones/{zone_id}/dns_records/{record['id']}", {"content": cname_target})
        print(f"  DNS {hostname}: updated")
    else:
        api_post(token, f"/zones/{zone_id}/dns_records", {
            "type": "CNAME",
            "name": hostname,
            "content": cname_target,
            "proxied": True
        })
        print(f"  DNS {hostname}: created")


def main():
    opts = load_options()
    token = opts["api_token"]
    account_id = opts["account_id"]
    tunnel_name = opts["tunnel_name"]
    services = opts["services"]

    if "@" in account_id or " " in account_id or len(account_id) < 20:
        print("ERROR: 'account_id' parece inválido. Deve ser o ID hexadecimal da conta (32 chars), não o email.", file=sys.stderr)
        print("Acesse dash.cloudflare.com → selecione um domínio → barra lateral direita → 'ID da Conta'.", file=sys.stderr)
        sys.exit(1)

    tunnel_id = get_or_create_tunnel(token, account_id, tunnel_name)

    with open(TUNNEL_ID_FILE, "w") as f:
        f.write(tunnel_id)

    print("Configuring DNS records...")
    zone_cache = {}
    for svc in services:
        hostname = svc["hostname"]
        domain = ".".join(hostname.split(".")[-2:])
        if domain not in zone_cache:
            zone_cache[domain] = get_zone_id(token, hostname)
        ensure_dns_record(token, zone_cache[domain], hostname, tunnel_id)

    print(f"Cloudflare configured: {len(services)} service(s) ready.")


if __name__ == "__main__":
    main()
