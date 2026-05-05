#!/usr/bin/env python3
"""
BetSala Chile — production setup.

Запусти один раз ПЕРЕД заливкой на хостинг:
  python3 setup-production.py

Скрипт спросит твой домен и реферальную ссылку, после чего:
- заменит example.com на твой домен в sitemap.xml и robots.txt
- заменит REFERRAL_URL в /play-online-now/index.html на твою рефку
- готово к заливке
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def ask(prompt, default=None):
    full = f'{prompt}'
    if default:
        full += f' [{default}]'
    full += ': '
    answer = input(full).strip()
    return answer or default

print('=== BetSala Chile — production setup ===\n')
domain = ask('Домен сайта (без https://, например betsala-chile.com)')
if not domain:
    print('Домен обязателен. Выход.')
    sys.exit(1)
domain = domain.replace('https://', '').replace('http://', '').strip('/')

referral = ask('Реферальная ссылка партнёрки (полный URL)', 'https://www.betsala11.com/es/')

print(f'\nИспользую:')
print(f'  Домен: https://{domain}')
print(f'  Рефка: {referral}\n')

# 1. sitemap.xml — заменить example.com на домен
sm_path = os.path.join(ROOT, 'sitemap.xml')
if os.path.exists(sm_path):
    with open(sm_path) as f:
        sm = f.read()
    sm = sm.replace('https://example.com', f'https://{domain}')
    with open(sm_path, 'w') as f:
        f.write(sm)
    print(f'✓ sitemap.xml')

# 2. robots.txt
rb_path = os.path.join(ROOT, 'robots.txt')
if os.path.exists(rb_path):
    with open(rb_path) as f:
        rb = f.read()
    rb = rb.replace('https://example.com', f'https://{domain}')
    with open(rb_path, 'w') as f:
        f.write(rb)
    print(f'✓ robots.txt')

# 3. play-online-now/index.html — заменить REFERRAL_URL
po_path = os.path.join(ROOT, 'play-online-now', 'index.html')
if os.path.exists(po_path):
    with open(po_path) as f:
        po = f.read()
    po = re.sub(
        r"var REFERRAL_URL\s*=\s*'[^']*'",
        f"var REFERRAL_URL = '{referral}'",
        po
    )
    with open(po_path, 'w') as f:
        f.write(po)
    print(f'✓ play-online-now/index.html')

print('\n✅ Готово. Теперь:')
print('   1. Залей всю папку на хостинг (FTP, rsync, cPanel — что используешь)')
print('   2. .htaccess уже в корне — Apache подхватит его автоматически')
print(f'   3. Проверь сайт: https://{domain}/')
print(f'   4. Проверь рефку: https://{domain}/play-online-now/')
print(f'   5. Запусти PageSpeed: https://pagespeed.web.dev/analysis?url=https://{domain}/')
