"""HTTP/SSE server entry point for meilisearch-mcp."""
import os
import uvicorn
from fastapi import FastAPI
from .server import create_server
from .sse import create_sse_server


def main():
    """Run the MCP server with SSE transport."""
    url = os.getenv("MEILI_HTTP_ADDR", "http://localhost:7700")
    api_key = os.getenv("MEILI_MASTER_KEY")

    # Create MCP server instance
    mcp_server = create_server(url, api_key)

    # Create FastAPI app with SSE transport
    app = FastAPI(
        title="Meilisearch MCP Server",
        description="MCP server for Meilisearch with SSE transport",
        version="0.6.0",
    )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "meilisearch-mcp"}

    # Mount SSE transport at root
    app.mount("/", create_sse_server(mcp_server))

    # Configuration
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))

    # Run server
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
