import uvicorn
import argparse
import socket


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI server.")
    parser.add_argument(
        "--host",
        type=str,
        default=get_local_ip(),
        help="Host IP to bind (default: local IP)",
    )
    parser.add_argument(
        "--port", type=int, default=1919, help="Port to bind (default: 1919)"
    )
    args = parser.parse_args()

    from db_api import delete_all

    delete_all()

    uvicorn.run("fast_router:app", host=args.host, port=args.port, reload=True)
