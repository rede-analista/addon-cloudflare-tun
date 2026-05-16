# addon-cloudflare-tun

Add-on para Home Assistant que expõe múltiplos serviços locais via Cloudflare Tunnel com configuração automática de DNS.

## Pré-requisitos

- Um domínio gerenciado pelo DNS da Cloudflare
- Um API Token da Cloudflare (veja abaixo)
- O ID da sua conta Cloudflare

## Criando o API Token

1. Acesse [https://dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens)
2. Clique em **Criar Token**
3. Clique em **Criar Token Personalizado**
4. Dê um nome (ex: `ha-tunnel-manager`)
5. Em **Permissões**, adicione:
   - `Conta` > `Cloudflare Tunnel` > **Editar**
   - `Zona` > `DNS` > **Editar**
6. Em **Recursos da Conta**, selecione sua conta
7. Em **Recursos de Zona**, selecione **Todas as zonas** (ou zonas específicas)
8. Clique em **Continuar para o resumo** > **Criar Token**
9. Copie o token — ele é exibido apenas uma vez

## Encontrando o Account ID

1. Acesse [https://dash.cloudflare.com](https://dash.cloudflare.com)
2. Selecione qualquer domínio
3. Na barra lateral direita, role até **API** e copie o **ID da Conta**

## Configuração

| Opção | Descrição |
|-------|-----------|
| `api_token` | API Token da Cloudflare |
| `account_id` | ID da conta Cloudflare |
| `tunnel_name` | Nome do túnel (criado automaticamente) |
| `services` | Lista de serviços a expor |

Cada entrada em `services`:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `name` | Nome amigável | `Home Assistant` |
| `hostname` | Hostname público | `ha.exemplo.com.br` |
| `service` | URL interna | `http://homeassistant:8123` |

## Como funciona

Na inicialização o add-on:
1. Cria o túnel Cloudflare (ou reutiliza se as credenciais já estiverem salvas em `/data`)
2. Cria ou atualiza o registro CNAME no DNS para cada serviço apontando para o túnel
3. Gera o config do cloudflared e inicia o túnel

As credenciais do túnel são salvas em `/data/tunnel-credentials.json` e reutilizadas nos reinícios.

## Instalação

Adicione a URL deste repositório na loja de add-ons do Home Assistant:
`https://github.com/rede-analista/addon-cloudflare-tun`

## Solução de problemas

**"Tunnel already exists but no local credentials found"**
Delete o túnel pelo painel da Cloudflare em **Zero Trust > Redes > Túneis** e reinicie o add-on.
