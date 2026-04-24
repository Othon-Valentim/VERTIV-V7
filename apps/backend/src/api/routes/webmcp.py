"""
Experimental WebMCP endpoints.

These routes are registered only when WEBMCP_ENABLED=true. All catalog
surfaces require authentication so experimental agent capabilities do not
become public production API by accident.
"""

from fastapi import APIRouter, Depends, HTTPException

from src.api.export_webmcp_schemas import (
    get_webmcp_tool_catalog,
    get_webmcp_tool_by_name,
)
from src.infrastructure.auth import CurrentUser, get_current_user

router = APIRouter()


def _catalog_response(protocol: str) -> dict:
    return {
        "version": "7.0.0-SINGULARITY",
        "protocol": protocol,
        "tools": get_webmcp_tool_catalog(),
        "context_policy": {
            "max_fields": 5,
            "allowed_fields": [
                "project_id",
                "current_vpl",
                "current_irr",
                "role",
                "active_step",
            ],
        },
    }


@router.get("/webmcp/schemas")
async def get_webmcp_schemas(user: CurrentUser = Depends(get_current_user)):
    """
    Return the authenticated WebMCP tool catalog for browser agents.
    """
    return _catalog_response("webmcp-draft-2026")


@router.get("/webmcp/schemas/{tool_name}")
async def get_webmcp_schema_by_name(
    tool_name: str, user: CurrentUser = Depends(get_current_user)
):
    """
    Return a single authenticated tool definition by name.
    """
    tool = get_webmcp_tool_by_name(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool


@router.get("/openapi/schemas")
async def get_openapi_schemas_b2b(user: CurrentUser = Depends(get_current_user)):
    """
    Protected schema catalog for B2B integrators and internal tooling.
    """
    response = _catalog_response("openapi-b2b-v7")
    response["description"] = (
        "VERTIV Real Estate Analysis Platform - deterministic NPV/IRR engine "
        "with legal due diligence."
    )
    response["documentation"] = "https://vertiv.tech/docs/api"
    return response
