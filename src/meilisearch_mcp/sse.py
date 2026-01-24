"""SSE transport support for remote MCP connections."""
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp.server.sse import SseServerTransport


def create_sse_server(mcp_server, message_path: str = "/messages/"):
    """
    Create a Starlette app that handles SSE connections for MCP.

    Args:
        mcp_server: The MeilisearchMCPServer instance
        message_path: Path for POST message endpoint

    Returns:
        Starlette application for SSE transport
    """
    transport = SseServerTransport(message_path)

    async def handle_sse(request):
        """Handle incoming SSE connection requests."""
        async with transport.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp_server.server.run(
                streams[0],
                streams[1],
                mcp_server.server.create_initialization_options(),
            )

    routes = [
        Route("/sse/", endpoint=handle_sse),
        Mount(message_path, app=transport.handle_post_message),
    ]

    return Starlette(routes=routes)
