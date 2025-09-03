#!/usr/bin/env python3
import requests
import time
import argparse

def load_payloads(files):
	payload_set = []
	for f in files:
		with open(f, "r") as infile:
			payloads = [line.strip() for line in infile if line.strip()]
			payload_sets.append(payloads)
	return payload_sets

def substitute_placehoders(text, payloads, i):
    if not text:
        return text
    for j, payload_list in enumerate(payloads, start=1):
        placeholders = f"§{j}§"
    if i < len(payload_list):
        text = text.replace(placeholder, payload_list[i])
    return text

def pitchfork_attack(url, body, payload_set, headers_list=None, method="POST"):
	nb_requests = min(len(p) for p in payload_sets)

    for i in range(nb_requests):
        body = substitute_placeholders(body, payload_set, i)

        headers = {}
	    if headers_list:
		    for h in headers_list:
		    k, v = h.split(":", 1)
		    k = substitute_placeholders(k.strip(), payload_set,i)
		    v = substitute_placeholders(v.strip(), payload_set,i)
            headers[k] = v

        start = time.time()
        r = requests.request(method, url, headers=headers, data=body)
        end = time.time()
        duration = end - start

        current_payload = [pl[i] for pl in payload_set]
        payload_str = " | ".join(current_payload)

        print(f"{payload_str} || {r.status_code} | {len(r.text)} | {duration:.4f}s")

    


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Mini Pitchfork Intruder to measure response times")
	parser.add_argument("url", required=True, help="Target URL")
	parser.add_argument("-p", "--payloads", nargs="+", required=True, help="Payload files (one per §n§ placeholder accordingly)")
	parser.add_argument("-b", "--body", help="Request body (use §n§ as placeholders)"
	parser.add_argument("-X", "--method", default="POST", help="HTTP method (default POST)")
	parser.add_argument("-H", "--header", action:"append", help="Custom headers (use $n$ as placeholders)")

	args = parser.parse_args()

	payload_set = load_payloads(args.payloads)
	pitchfork_attack(args.url, args.body, payload_set, headers_list=args.header, method=args.method)
