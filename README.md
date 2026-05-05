# BetSala Chile — production deploy

Многостраничный партнёрский сайт BetSala 11 Chile (испанский, рынок Чили).

## Деплой за 3 шага

### 1. Запусти setup-скрипт

```bash
python3 setup-production.py
```

Скрипт спросит:
- **Домен сайта** (например `betsala-chile.com`)
- **Реферальная ссылка партнёрки** (твоя рефка из дашборда BetSala/affiliate-сети)

И автоматически подставит их в:
- `sitemap.xml` — абсолютные URL для индексации
- `robots.txt` — Sitemap directive
- `play-online-now/index.html` — JS-редирект на рефку

### 2. Залей файлы на хостинг

Всё содержимое папки `betsala/` → в корень домена (`public_html`, `htdocs`, `www`).

**Важно:** `.htaccess` начинается с точки и часто скрыт в FTP-клиентах. Включи показ скрытых файлов перед заливкой.

### 3. Проверь PageSpeed

```
https://pagespeed.web.dev/analysis?url=https://your-domain.com/
```

Должно быть **100/100/100/100** на mobile и desktop.

---

## Структура

```
betsala/
├── index.html                       Главная
├── /casino/, /tragamonedas/, /casino-en-vivo/, /apuestas-deportivas/
├── /aviator/, /lucky-jet/, /mines/                    Crash games
├── /bono-de-bienvenida/, /codigo-promocional/, /promociones/
├── /registro/, /iniciar-sesion/, /app/, /vip/, /soporte/, /confiable/
├── /play-online-now/                JS-redirect (noindex)
├── /css/style.css                   Стили
├── /assets/                         Логотип, фавикон
├── /images/                         15 WebP картинок
├── .htaccess                        Кеширование, gzip, security headers
├── robots.txt
├── sitemap.xml
└── setup-production.py              Скрипт настройки
```

17 SEO-страниц + 1 redirect + 1 .htaccess.

## Партнёрский редирект

Все CTA на сайте (124 кнопки) ведут на `/play-online-now/` с атрибутами:

```
rel="nofollow noopener noreferrer sponsored"
data-nosnippet
target="_blank"
```

Страница `/play-online-now/` имеет:
- `<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">`
- Заблокирована в `robots.txt`
- JS делает `window.location.replace()` через 1500ms
- Пробрасывает UTM/clickid/gclid в рефку

## PageSpeed оптимизации

- ✅ WebP картинки (≈10x легче JPG/PNG)
- ✅ `loading="lazy"` для всех картинок ниже фолда
- ✅ `.htaccess` — gzip/brotli + кеш 1 год для статики
- ✅ HTTPS-редирект и security headers в `.htaccess`
- ✅ Минимум HTTP-запросов

## Локальный preview

Если нужно проверить перед заливкой:

```bash
cd betsala
python3 -m http.server 8000
# открой http://localhost:8000
```

**Не открывай через двойной клик (file://)** — пути в HTML абсолютные (`/images/...`), браузер не найдёт файлы.

## Где менять контент

- **Тексты страниц** — напрямую в `*/index.html` (HTML минифицирован, но читаемый)
- **CSS** — `css/style.css`, единый файл
- **Логотип/фавикон** — `assets/logo.webp`, `assets/favicon.webp`
- **Картинки** — `images/*.webp` (15 шт., имена менять не надо — просто перезаписывай)
- **Промокод** — в `codigo-promocional/index.html` найди `BETSALA2026`
- **Меню** — нижняя/верхняя навигация во всех HTML, проще править поиском по `/casino/` или другому slug

## Важно для прода

1. **HTTPS обязателен** — `.htaccess` редиректит HTTP → HTTPS автоматически
2. **HTTP/2 или HTTP/3** — на современных хостингах включено по умолчанию
3. **Brotli/Gzip** — `.htaccess` включает gzip (если есть `mod_deflate`) и brotli (если есть `mod_brotli`)
4. **CDN** — для лучшего PageSpeed подключи Cloudflare (free план достаточен)

## CDN (опционально, +5-10 баллов на мобильном PageSpeed)

Если домен на Cloudflare:
- **Speed → Optimization** → включи Auto Minify (HTML, CSS, JS)
- **Caching → Configuration** → Browser TTL: 1 month
- **Speed → Optimization → Image** → Polish (Lossy) — дополнительная оптимизация картинок
