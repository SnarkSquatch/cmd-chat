import argparse
from cmd_chat.server.server import run_server
from cmd_chat.client.client import Client


def run_http_server(ip: str, port: int, password: str | None) -> None:
    run_server(host=ip, port=int(port), admin_password=password)


def main():
    parser = argparse.ArgumentParser(description="Command-line chat application")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve_p = subparsers.add_parser("serve", help="Run server")
    serve_p.add_argument("ip_address")
    serve_p.add_argument("port")
    serve_p.add_argument("--password", "-p", required=True)

    connect_p = subparsers.add_parser("connect", help="Connect to server")
    connect_p.add_argument("ip_address")
    connect_p.add_argument("port")
    connect_p.add_argument("username")
    connect_p.add_argument("password")

    args = parser.parse_args()

    if args.command == "serve":
        run_http_server(args.ip_address, args.port, args.password)
    elif args.command == "connect":
        Client(
            server=args.ip_address,
            port=int(args.port),
            username=args.username,
            password=args.password,
        ).run()


if __name__ == "__main__":
    main()
