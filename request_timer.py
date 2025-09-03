#!/usr/bin/env python3
import time
import argparse
import httpx

def load_payloads(files):
    payload_sets = []
    for f in files:
        with open(f, "r") as infile:
            payloads = [line.strip() for line in infile if line.strip()]
            payload_sets.append(payloads)
    return payload_sets

def substitute_placeholders(text, payloads, i):
    if not text:
        return text
    for j, payload_list in enumerate(payloads, start=1):
        placeholder = f"§{j}§"
        if i < len(payload_list):
            text = text.replace(placeholder, payload_list[i])
    return text

def make_request(client, url, method, headers_list, body, payload_sets, i):
    req_body = substitute_placeholders(body, payload_sets, i)

    headers = {}
    if headers_list:
        for h in headers_list:
            k, v = h.split(":", 1)
            k = substitute_placeholders(k.strip(), payload_sets, i)
            v = substitute_placeholders(v.strip(), payload_sets, i)
            headers[k] = v

    start = time.time()
    r = client.request(method, url, headers=headers, data=req_body)
    end = time.time()

    current_payload = [pl[i] for pl in payload_sets]
    payload_str = " | ".join(current_payload)
    return f"{payload_str} || {r.status_code} | {len(r.text)} | {end-start:.4f}s"

def pitchfork_attack(url, body, payload_sets, headers_list=None, method="POST", http_version="1.1"):
    nb_requests = min(len(p) for p in payload_sets)

    with httpx.Client(http2=(http_version == "2")) as client:
        client.get(url) # Dummy request
        for i in range(nb_requests):
            result = make_request(client, url, method, headers_list, body, payload_sets, i)
            print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini Pitchfork Intruder to measure response times")
    parser.add_argument("--http-version", choices=["1.1", "2"], default="1.1", help="HTTP version (1.1 or 2)")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-p", "--payloads", nargs="+", required=True, help="Payload files (one per §n§ placeholder accordingly)")
    parser.add_argument("-b", "--body", help="Request body (use §n§ as placeholders)")
    parser.add_argument("-X", "--method", default="POST", help="HTTP method (default POST)")
    parser.add_argument("-H", "--header", action="append", help="Custom headers (use §n§ as placeholders)")

    args = parser.parse_args()
    payload_sets = load_payloads(args.payloads)

    pitchfork_attack(
        args.url,
        args.body,
        payload_sets,
        headers_list=args.header,
        method=args.method,
        http_version=args.http_version,
    )
