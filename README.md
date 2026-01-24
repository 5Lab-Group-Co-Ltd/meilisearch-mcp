<div align="center">
  <img src="https://github.com/meilisearch/meilisearch/blob/main/assets/logo.svg" alt="Meilisearch" width="200" height="200" />
</div>

<h1 align="center">Meilisearch MCP Server</h1>

<p align="center">
  <a href="https://pypi.org/project/meilisearch-mcp/"><img src="https://img.shields.io/pypi/v/meilisearch-mcp.svg" alt="PyPI version"></a>
  <a href="https://github.com/meilisearch/meilisearch-mcp/actions"><img src="https://github.com/meilisearch/meilisearch-mcp/workflows/Test%20and%20Lint/badge.svg" alt="Tests"></a>
  <a href="https://github.com/meilisearch/meilisearch-mcp/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-informational" alt="License"></a>
</p>

<p align="center">MCP server for Meilisearch with SSE transport for n8n integration</p>

## Quick Start with Docker Compose

**For n8n MCP Client integration**, use Docker Compose to run Meilisearch and the MCP server:

```bash
# Create data directory with correct permissions
sudo mkdir -p /var/lib/meilisearch
sudo chown -R 1000:1000 /var/lib/meilisearch

# Start services
docker-compose up -d

# Verify health
curl http://localhost:8000/health
# {"status":"healthy","service":"meilisearch-mcp"}
```

### Configure n8n MCP Client

In n8n, add an **MCP Client** node:

| Setting | Value |
|---------|-------|
| Connection Type | `Server-Sent Events (SSE)` |
| URL | `http://localhost:8000/sse/` |

### Upgrade Meilisearch

```bash
# Edit docker-compose.yml, change version, then:
docker-compose down
docker-compose up -d
```

Data persists at `/var/lib/meilisearch` on the host (Ubuntu 24 LTS).

### nginx Reverse Proxy (HTTPS Only)

If only port 443 is open, use nginx as a reverse proxy for SSE:

```nginx
# /etc/nginx/sites-available/meilisearch-mcp
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # SSE endpoint (requires special handling)
    location /sse/ {
        proxy_pass http://localhost:8000/sse/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_cache off;
        proxy_buffering off;
        chunked_transfer_encoding off;
        proxy_read_timeout 3600s;
    }

    # POST messages endpoint
    location /messages/ {
        proxy_pass http://localhost:8000/messages/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }

    # Health check
    location /health {
        proxy_pass http://localhost:8000/health;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
```

Then update n8n MCP Client URL to: `https://your-domain.com/sse/`

## Installation

### From PyPI

```bash
pip install meilisearch-mcp
```

### From Source

```bash
git clone https://github.com/meilisearch/meilisearch-mcp.git
cd meilisearch-mcp
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

### STDIO Mode (Claude Desktop)

```bash
meilisearch-mcp
```

Configuration for `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "meilisearch": {
      "command": "uvx",
      "args": ["-n", "meilisearch-mcp"]
    }
  }
}
```

### HTTP/SSE Mode (n8n, Remote Clients)

```bash
meilisearch-mcp-http
```

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `MEILI_HTTP_ADDR` | `http://localhost:7700` | Meilisearch URL |
| `MEILI_MASTER_KEY` | - | Meilisearch API key (optional) |
| `MCP_HOST` | `0.0.0.0` | Server host |
| `MCP_PORT` | `8000` | Server port |

## Available Tools

### Connection Management
- `get-connection-settings` - View current connection settings
- `update-connection-settings` - Update URL and/or API key

### Index Operations
- `create-index` - Create a new index
- `list-indexes` - List all indexes
- `delete-index` - Delete an index
- `get-index-metrics` - Get detailed index metrics

### Document Operations
- `get-documents` - Retrieve documents with pagination
- `add-documents` - Add or update documents

### Search
- `search` - Search across single or multiple indices with filtering

### Settings Management
- `get-settings` - View index settings
- `update-settings` - Update index settings

### Task Management
- `get-task` / `get-tasks` - Query tasks
- `cancel-tasks` - Cancel pending tasks

### API Key Management
- `get-keys` - List API keys
- `create-key` - Create new API key
- `delete-key` - Delete API key

### System Monitoring
- `health-check` / `get-health-status` - Health checks
- `get-version` / `get-stats` / `get-system-info` - System info

## Development

```bash
# Run tests
python -m pytest tests/ -v

# Format code
black src/ tests/

# Test with MCP Inspector
npx @modelcontextprotocol/inspector python -m src.meilisearch_mcp
```

## License

MIT - see [LICENSE](LICENSE) for details.
