#!/usr/bin/env python3
import json
import sys

OPTIONS_FILE = "/data/options.json"
CREDENTIALS_FILE = "/data/tunnel-credentials.json"
TUNNEL_ID_FILE = "/tmp/tunnel_id"
CONFIG_FILE = "/tmp/cloudflared.yml"


def main():
    with open(OPTIONS_FILE) as f:
        opts = json.load(f)

    with open(TUNNEL_ID_FILE) as f:
        tunnel_id = f.read().strip()

    services = opts["services"]
    if not services:
        print("ERROR: No services configured.", file=sys.stderr)
        sys.exit(1)

    lines = [
        f"tunnel: {tunnel_id}",
        f"credentials-file: {CREDENTIALS_FILE}",
        "",
        "ingress:",
    ]
    for svc in services:
        lines.append(f"  - hostname: {svc['hostname']}")
        lines.append(f"    service: {svc['service']}")
    lines.append("  - service: http_status:404")

    with open(CONFIG_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Config written with {len(services)} service(s).")


if __name__ == "__main__":
    main()
