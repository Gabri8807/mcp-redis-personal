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
    return {"message": "Redis MCP Server is running. Use an MCP client to connect via SSE if supported."}

@app.get("/sse")
async def handle_sse(request: Request):
    # This is a placeholder. 
    # Real implementation would require mounting the mcp server as an SSE endpoint.
    return JSONResponse(status_code=501, content={"error": "SSE Not implemented yet for Vercel deployment of this specific codebase. FastMCP requires explicit SSE mounting."})

# Attempt to mount if possible (optimistic)
if hasattr(mcp, '_fastapi_app'):
    app = mcp._fastapi_app
