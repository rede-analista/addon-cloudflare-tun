ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache python3 py3-pip curl

RUN pip3 install requests --break-system-packages 2>/dev/null || pip3 install requests

ARG BUILD_ARCH
RUN case "${BUILD_ARCH}" in \
      "amd64") CF_ARCH="amd64" ;; \
      "aarch64") CF_ARCH="arm64" ;; \
      "armhf"|"armv7") CF_ARCH="arm" ;; \
      "i386") CF_ARCH="386" ;; \
      *) CF_ARCH="amd64" ;; \
    esac && \
    curl -fsSL "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${CF_ARCH}" \
      -o /usr/local/bin/cloudflared && \
    chmod +x /usr/local/bin/cloudflared

COPY run.sh /etc/services.d/cloudflare-tun/run
COPY cloudflare_api.py /
COPY generate_config.py /

RUN chmod +x /etc/services.d/cloudflare-tun/run
