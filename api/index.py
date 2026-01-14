import os
import sys

# Add the project root to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.common.server import mcp

# Check if mcp is a valid object we can serve
# If using FastMCP, it might be an object that we can interact with.
# For Vercel, we need an ASGI app.
# If mcp is a FastMCP instance, we might need to access its internal app.
# Since we can't inspect it easily without running, we will assume standard FastMCP 
# doesn't expose ASGI publicly without 'run'.
# However, we can use mcp._fastapi_app if it exists (private API).

# Fallback: create a dummy app that informs the user
from fastapi import FastAPI, Request
from mcp.server.sse import SseServerTransport
from starlette.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    # Try to check Redis connection status
    redis_status = "Not configured"
    redis_url = os.environ.get("REDIS_URL") or os.environ.get("KV_URL")
    
    if redis_url:
        try:
            from redis import Redis
            r = Redis.from_url(redis_url, socket_timeout=2)
            if r.ping():
                redis_status = "Connected ✅"
            else:
                redis_status = "Failed to Ping ❌"
        except Exception as e:
            redis_status = f"Error: {str(e)} ❌"
    
    return {
        "status": "Redis MCP Server is running 🚀",
        "redis_connection": redis_status,
        "instructions": "Use an MCP client to connect via SSE if supported, or uses stdio locally."
    }

@app.get("/sse")
async def handle_sse(request: Request):
    # This is a placeholder. 
    # Real implementation would require mounting the mcp server as an SSE endpoint.
    return JSONResponse(status_code=501, content={"error": "SSE Not implemented yet for Vercel deployment of this specific codebase. FastMCP requires explicit SSE mounting."})

# Attempt to mount if possible (optimistic)
if hasattr(mcp, '_fastapi_app'):
    # If using native FastMCP, we wrapp it but keep our root for diagnostics if needed, 
    # or let FastMCP take over. 
    # For now, let's keep our diagnostic root on a subpath if needed, or just use the app.
    # Note: FastMCP usually mounts on /sse by default or root.
    app = mcp._fastapi_app
