# Async MTProto Proxy #

Fast and simple to setup MTProto proxy written in Python.

## Starting Up ##
    
1. `git clone -b stable https://github.com/alexbers/mtprotoproxy.git; cd mtprotoproxy`
2. Copy environment template and set **PORT**, **USERS** and (optionally) **AD_TAG**:
   `cp .env.example .env && nano .env`
3. Start in Docker: `docker compose up -d --build` (or run `python3 mtprotoproxy.py` without Docker)
4. *(optional, get a link to share the proxy)* `docker compose logs`

![Demo](https://alexbers.com/mtprotoproxy/install_demo_v2.gif)

## Channel Advertising ##

To advertise a channel get a tag from **@MTProxybot** and put it into `.env` as `AD_TAG`.

## Performance ##

The proxy performance should be enough to comfortably serve about 4 000 simultaneous users on
the VDS instance with 1 CPU core and 1024MB RAM.

## More Instructions ##

- [Инструкция на русском: установка и запуск на VPS с чистой системы](VPS_INSTALL_RU.md)
- [Running without Docker](https://github.com/alexbers/mtprotoproxy/wiki/Running-Without-Docker)
- [Optimization and fine tuning](https://github.com/alexbers/mtprotoproxy/wiki/Optimization-and-Fine-Tuning)

## Advanced Usage ##

The proxy can be launched:
- with a custom config: `python3 mtprotoproxy.py [configfile]`
- several times, clients will be automaticaly balanced between instances
- with uvloop module to get an extra speed boost
- with runtime statistics exported to [Prometheus](https://prometheus.io/)

### Webshare SOCKS5 bootstrap

If you use Webshare as an upstream proxy provider, you can let the proxy fetch SOCKS5
credentials automatically on startup (and on `SIGUSR2` reload):

```bash
WEBSHARE_API_KEY=your_api_key
WEBSHARE_PLAN_ID=your_plan_id
WEBSHARE_MODE=direct
```

When both `WEBSHARE_API_KEY` and `WEBSHARE_PLAN_ID` are set, the app requests
`GET https://proxy.webshare.io/api/v2/proxy/list/?mode=<mode>&plan_id=<plan_id>`
with `Authorization: Token <api_key>`, takes the first proxy from the response and
applies it as `SOCKS5_HOST/SOCKS5_PORT/SOCKS5_USER/SOCKS5_PASS`.

Reference: https://apidocs.webshare.io/
