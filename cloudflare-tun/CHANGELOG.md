# Changelog

## 1.0.1

- Correção: run.sh registrado como serviço s6 em vez de CMD do Docker
  (resolvia erro "can only run as pid 1" ao iniciar o add-on)

## 1.0.0

- Initial release
- Cloudflare Tunnel creation and reuse via API
- Automatic DNS CNAME record management per service
- Multi-architecture support (amd64, aarch64, armhf, armv7, i386)
- Credentials persisted in /data to survive restarts
