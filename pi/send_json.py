#!/usr/bin/env python3

import time
import argparse
import os
import sys

try:
	import requests
	from requests.auth import HTTPBasicAuth
except Exception:
	print("Missing dependency: requests. Install with: pip3 install requests")
	raise


"""
Simple uploader for JSON files.

Usage examples:
  python3 pi/send_json.py --file ../web/2019-03-28T15:53:00.json --url https://example.com/upload.php
  python3 pi/send_json.py -f web/2019-03-28T15:53:00.json -u https://example.com/upload.php --method put

By default the script will POST the file as multipart/form-data under the field name `file`.
Use `--method put` to send the JSON as the raw request body with `Content-Type: application/json`.
Supports optional basic auth (`--auth user:pass`) and retries.
"""


def parse_args():
	p = argparse.ArgumentParser(description="Upload a JSON file to a web endpoint")
	p.add_argument("--file", "-f", required=True, help="Path to the JSON file to upload")
	p.add_argument("--url", "-u", required=True, help="Target URL to upload to")
	p.add_argument("--method", "-m", choices=["post", "put"], default="post",
				   help="HTTP method: post (multipart file) or put (raw JSON body)")
	p.add_argument("--auth", help="Basic auth in the form user:pass")
	p.add_argument("--retries", type=int, default=3, help="Number of upload attempts")
	p.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds")
	return p.parse_args()


def build_auth(auth_str):
	if not auth_str:
		return None
	if ":" in auth_str:
		user, pwd = auth_str.split(":", 1)
	else:
		user, pwd = auth_str, ""
	return HTTPBasicAuth(user, pwd)


def upload_json(file_path, url, method="post", auth=None, retries=3, timeout=30):
	if not os.path.isfile(file_path):
		raise FileNotFoundError(f"File not found: {file_path}")

	# Read file content once
	with open(file_path, "rb") as fh:
		content = fh.read()

	last_exc = None
	for attempt in range(1, retries + 1):
		try:
			if method == "put":
				headers = {"Content-Type": "application/json"}
				resp = requests.put(url, data=content, headers=headers, auth=auth, timeout=timeout)
			else:
				files = {"file": (os.path.basename(file_path), content, "application/json")}
				resp = requests.post(url, files=files, auth=auth, timeout=timeout)

			resp.raise_for_status()
			print(f"Upload successful: {resp.status_code} {resp.reason}")
			return resp
		except Exception as e:
			last_exc = e
			print(f"Attempt {attempt} failed: {e}")
			if attempt < retries:
				backoff = 2 ** attempt
				print(f"Retrying in {backoff}s...")
				time.sleep(backoff)

	# after retries
	raise last_exc


def main():
	args = parse_args()
	auth = build_auth(args.auth)
	try:
		resp = upload_json(args.file, args.url, method=args.method, auth=auth, retries=args.retries, timeout=args.timeout)
		# print response body if small
		text = resp.text
		if text:
			print("Response body:")
			print(text)
	except FileNotFoundError as fnf:
		print(fnf)
		sys.exit(2)
	except Exception as e:
		print("Upload failed:", e)
		sys.exit(1)


if __name__ == "__main__":
	main()
