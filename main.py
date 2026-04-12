import sys
import json
import argparse
from core.engine import Engine

def print_results(results):
    print("\n" + "="*50)
    print("ReSULTS")
    print("="*50)
    for r in results:
        status = "✓" if r.success else "✗"
        print(f"\n[{status}] {r.module} — {r.target}")
        if r.success:
            print(json.dumps(r.data, indent=2, ensure_ascii=False))
        else:
            print(f"Error: {r.error}")
    print("\n" + "="*50)


def main():
    parser = argparse.ArgumentParser(
        description="Sakai moi penis poka cto"
    )
    parser.add_argument("target", nargs="?", help="Target")
    parser.add_argument(
        "--type", default="ip",
        choices=["ip", "domain", "url", "email"],
        help="Target type"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="Show all modules"
    )
    args = parser.parse_args()
    print("[*] Modules loading...")
    engine = Engine()

    if args.list or not args.target:
        engine.list_modules()
        return

    results = engine.run(args.target, args.type)
    print_results(results)


if __name__ == "__main__":
    main()