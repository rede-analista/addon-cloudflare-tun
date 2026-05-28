# Cloudflare Tunnel Manager — Add-on para Home Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Add-on para Home Assistant que expõe múltiplos serviços locais via **Cloudflare Tunnel** com configuração automática de DNS.

---

## Funcionalidades

- Expõe quantos serviços locais quiser (Home Assistant, Node-RED, Grafana, etc.) com um único túnel
- Criação e reutilização automática do túnel Cloudflare
- Criação/atualização automática dos registros CNAME no DNS para cada serviço
- Suporte a redes privadas via Cloudflare WARP
- Credenciais do túnel persistidas em `/data` — sobrevivem a reinicializações

---

## Requisitos

- Home Assistant OS ou Supervised
- Um domínio gerenciado pelo DNS da Cloudflare
- Um API Token da Cloudflare com permissões de Tunnel e DNS (veja abaixo)
- O ID da sua conta Cloudflare

---

## Instalação

1. No Home Assistant, acesse **Configurações → Add-ons → Loja de Add-ons**
2. Clique no menu **⋮** (canto superior direito) → **Repositórios**
3. Adicione a URL do repositório:
   ```
   https://github.com/rede-analista/addon-cloudflare-tun
   ```
4. Localize **Cloudflare Tunnel Manager** na loja e clique em **Instalar**
5. Configure as opções e clique em **Iniciar**

---

## Configuração

| Opção | Descrição |
|-------|-----------|
| `api_token` | API Token da Cloudflare (com permissões de Tunnel e DNS) |
| `account_id` | ID da conta Cloudflare |
| `tunnel_name` | Nome do túnel (criado automaticamente se não existir) |
| `services` | Lista de serviços a expor publicamente |
| `private_networks` | (Opcional) Redes privadas acessíveis via WARP |

### Serviços

Cada entrada em `services`:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `name` | Nome amigável | `Home Assistant` |
| `hostname` | Hostname público | `ha.exemplo.com.br` |
| `service` | URL interna do serviço | `http://homeassistant:8123` |

### Exemplo de configuração

```yaml
api_token: "SEU_TOKEN_AQUI"
account_id: "SEU_ACCOUNT_ID_AQUI"
tunnel_name: "ha-tunnel"
services:
  - name: "Home Assistant"
    hostname: "ha.exemplo.com.br"
    service: "http://homeassistant:8123"
  - name: "Node-RED"
    hostname: "nodered.exemplo.com.br"
    service: "http://homeassistant:1880"
private_networks: []
```

---

## Criando o API Token

1. Acesse [dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens)
2. Clique em **Criar Token** → **Criar Token Personalizado**
3. Dê um nome (ex: `ha-tunnel-manager`)
4. Em **Permissões**, adicione:
   - `Conta` > `Cloudflare Tunnel` > **Editar**
   - `Zona` > `DNS` > **Editar**
5. Em **Recursos da Conta**, selecione sua conta
6. Em **Recursos de Zona**, selecione **Todas as zonas** (ou zonas específicas)
7. Clique em **Continuar para o resumo** → **Criar Token**
8. Copie o token — ele é exibido apenas uma vez

## Encontrando o Account ID

1. Acesse [dash.cloudflare.com](https://dash.cloudflare.com)
2. Selecione qualquer domínio
3. Na barra lateral direita, role até **API** e copie o **ID da Conta**

---

## Como funciona

Na inicialização o add-on:

1. Cria o túnel Cloudflare (ou reutiliza se as credenciais já estiverem salvas em `/data`)
2. Cria ou atualiza o registro CNAME no DNS para cada serviço, apontando para o túnel
3. Gera a configuração do `cloudflared` e inicia o processo do túnel

As credenciais do túnel são salvas em `/data/tunnel-credentials.json` e reutilizadas nos reinícios, evitando a criação de túneis duplicados.

---

## Solução de problemas

**"Tunnel already exists but no local credentials found"**

O túnel existe na Cloudflare mas as credenciais locais foram perdidas. Solução:
1. Acesse o painel Cloudflare em **Zero Trust → Redes → Túneis**
2. Delete o túnel com o nome configurado
3. Reinicie o add-on — ele criará um novo túnel

---

## Licença

[MIT](LICENSE) © Rede Analista
