from __future__ import annotations

import argparse
import asyncio

from mcp.server.stdio import stdio_server

from jira_mcp.factory import build_fail_closed_executor
from jira_mcp.server import build_server, health, readiness


async def run_stdio() -> None:
    executor = build_fail_closed_executor()
    server = build_server(executor)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    parser = argparse.ArgumentParser(description="Jira MCP on-premises server")
    parser.add_argument("--transport", choices=("stdio",), default="stdio")
    parser.add_argument("--health", action="store_true")
    parser.add_argument("--ready", action="store_true")
    args = parser.parse_args()
    executor = build_fail_closed_executor()
    if args.health:
        print(health())
        return
    if args.ready:
        print(readiness(executor))
        return
    asyncio.run(run_stdio())


if __name__ == "__main__":
    main()
