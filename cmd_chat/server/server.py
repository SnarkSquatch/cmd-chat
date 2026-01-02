from typing import Optional
from .logger import logger
from .factory import create_app

app = create_app()


def run_server(
    host: str = "0.0.0.0",
    port: int = 8000,
    admin_password: Optional[str] = None,
    workers: int = 1,
) -> None:
    app.ctx.admin_password = admin_password
    logger.info(f"Starting server on {host}:{port}")

    app.run(
        host=host,
        port=port,
        workers=workers,
        debug=False,
        access_log=True,
    )
