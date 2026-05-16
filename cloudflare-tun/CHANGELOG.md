# Changelog

## 1.0.4

- Validação do campo account_id com mensagem de erro clara quando email é fornecido no lugar do ID hexadecimal

## 1.0.3

- Correção: base image trocada de `ghcr.io/home-assistant/amd64-base` para `alpine:3.19`
  (a imagem base do HA tem s6-overlay com ENTRYPOINT /init, causando conflito de PID 1)
- Volta ao padrão CMD ["/run.sh"] igual ao SMCR_HA

## 1.0.2

- Correção: shebang do run.sh trocado de `with-contenv bashio` para `bash`
  (with-contenv no s6-overlay v3 chama s6-overlay-suexec que só roda como PID 1)

## 1.0.1

- Correção: run.sh registrado como serviço s6 em vez de CMD do Docker
  (resolvia erro "can only run as pid 1" ao iniciar o add-on)

## 1.0.0

- Initial release
- Cloudflare Tunnel creation and reuse via API
- Automatic DNS CNAME record management per service
- Multi-architecture support (amd64, aarch64, armhf, armv7, i386)
- Credentials persisted in /data to survive restarts
