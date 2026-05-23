import importlib


def _load_main_with_flag(monkeypatch, enabled: bool):
    monkeypatch.setenv("WEBMCP_ENABLED", "true" if enabled else "false")
    import src.api.main as main_module

    return importlib.reload(main_module)


def test_webmcp_routes_are_not_registered_by_default(monkeypatch):
    main_module = _load_main_with_flag(monkeypatch, enabled=False)

    route_paths = {route.path for route in main_module.app.routes}

    assert main_module.WEBMCP_ENABLED is False
    assert "/api/v7/webmcp/schemas" not in route_paths
    assert "/api/v7/webmcp/schemas/{tool_name}" not in route_paths
    assert "/api/v7/openapi/schemas" not in route_paths


def test_webmcp_routes_are_registered_only_when_flag_is_enabled(monkeypatch):
    main_module = _load_main_with_flag(monkeypatch, enabled=True)

    route_paths = {route.path for route in main_module.app.routes}

    assert main_module.WEBMCP_ENABLED is True
    assert "/api/v7/webmcp/schemas" in route_paths
    assert "/api/v7/webmcp/schemas/{tool_name}" in route_paths
    assert "/api/v7/openapi/schemas" in route_paths


def test_webmcp_named_catalog_exposes_only_supported_tools():
    from src.api.export_webmcp_schemas import (
        get_webmcp_tool_by_name,
        get_webmcp_tool_catalog,
    )

    tool_names = {tool["name"] for tool in get_webmcp_tool_catalog()}

    assert tool_names == {"simulate_what_if", "highlight_pdf_evidence"}
    assert get_webmcp_tool_by_name("simulate_what_if") is not None
    assert get_webmcp_tool_by_name("approve_capital_sentence") is None
