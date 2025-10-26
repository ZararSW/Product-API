import argparse
import json
import os
import sys
from typing import Any, Dict

import requests


DEFAULT_BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")


def _print_json(obj: Any) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def _handle_response(resp: requests.Response, expect_no_content: bool = False) -> int:
    if expect_no_content:
        if resp.status_code in (200, 201, 202, 204):
            print(f"Status: {resp.status_code}")
            return 0
        print(f"Status: {resp.status_code}\nBody: {resp.text}")
        return 1

    ct = resp.headers.get("content-type", "")
    if resp.ok:
        if "application/json" in ct:
            try:
                _print_json(resp.json())
            except Exception:
                print(resp.text)
        else:
            print(resp.text)
        return 0
    else:
        msg = None
        try:
            msg = resp.json()
        except Exception:
            msg = resp.text
        print(f"Status: {resp.status_code}")
        if msg:
            if isinstance(msg, (dict, list)):
                _print_json(msg)
            else:
                print(msg)
        return 1


def cmd_health(args: argparse.Namespace) -> int:
    resp = requests.get(f"{args.base_url}/health", timeout=10)
    return _handle_response(resp)


def cmd_create(args: argparse.Namespace) -> int:
    payload: Dict[str, Any] = {
        "name": args.name,
        "price": args.price,
        "quantity": args.quantity,
    }
    resp = requests.post(f"{args.base_url}/products", json=payload, timeout=10)
    return _handle_response(resp)


def cmd_list(args: argparse.Namespace) -> int:
    resp = requests.get(f"{args.base_url}/products", timeout=10)
    return _handle_response(resp)


def cmd_get(args: argparse.Namespace) -> int:
    resp = requests.get(f"{args.base_url}/products/{args.id}", timeout=10)
    return _handle_response(resp)


def cmd_update(args: argparse.Namespace) -> int:
    payload: Dict[str, Any] = {
        "name": args.name,
        "price": args.price,
        "quantity": args.quantity,
    }
    resp = requests.put(
        f"{args.base_url}/products/{args.id}", json=payload, timeout=10
    )
    return _handle_response(resp)


def cmd_delete(args: argparse.Namespace) -> int:
    resp = requests.delete(f"{args.base_url}/products/{args.id}", timeout=10)
    return _handle_response(resp, expect_no_content=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI client for the Product CRUD API"
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"API base URL (default: {DEFAULT_BASE_URL}) or use env BASE_URL",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("health", help="Check API health")
    p.set_defaults(func=cmd_health)

    p = sub.add_parser("create", help="Create a product")
    p.add_argument("--name", required=True)
    p.add_argument("--price", type=float, required=True)
    p.add_argument("--quantity", type=int, required=True)
    p.set_defaults(func=cmd_create)

    p = sub.add_parser("list", help="List all products")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("get", help="Get a product by id")
    p.add_argument("--id", type=int, required=True)
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("update", help="Update a product by id")
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--price", type=float, required=True)
    p.add_argument("--quantity", type=int, required=True)
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("delete", help="Delete a product by id")
    p.add_argument("--id", type=int, required=True)
    p.set_defaults(func=cmd_delete)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)  # type: ignore[attr-defined]
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
