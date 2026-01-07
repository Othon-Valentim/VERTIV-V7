# VERTIV v6.1.0-SINGULARITY API Contract

## Overview

This document defines the API contract for the VERTIV Real Estate Viability Analysis Platform.

**Base URL:** `https://api.vertiv.tech`
**Version:** 6.1.0-SINGULARITY
**Authentication:** JWT Bearer Token (Supabase)

---

## Authentication

All protected endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

Tokens are obtained via Supabase Auth (login/register flow).

---

## Rate Limits

| Scope | Limit |
|-------|-------|
| Global | 60 requests/minute, 10 requests/second |
| Simulations | 30 requests/minute |

Rate limit headers are included in responses:
- `X-RateLimit-Remaining-Minute`
- `X-RateLimit-Remaining-Second`
- `X-RateLimit-Limit-Minute`
- `X-RateLimit-Limit-Second`

---

## Endpoints

### Health Check

```
GET /health
```

**Authentication:** None required

**Response:**
```json
{
  "status": "ok",
  "version": "6.1.0-SINGULARITY",
  "mode": "GLOBAL_EDITION",
  "security": "enabled"
}
```

---

### User Info

```
GET /me
```

**Authentication:** Required

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "role": "authenticated",
  "authenticated": true
}
```

---

### Create Simulation

```
POST /calculate/quick
```

**Authentication:** Required
**Rate Limit:** 30/minute

**Request Body:**
```json
{
  "id": "project-id",
  "name": "Project Name",
  "is_mixed_use": false,
  "separate_access_cores": true,
  "fire_load_category": "Residencial",
  "efficiency": 0.85,
  "financial_input": {
    "total_units": 100,
    "sales_price_avg": 12000,
    "construction_cost_total": 50000000,
    "land_cost": 10000000,
    "development_months": 36
  },
  "real_options": {
    "land_value_current": 10000000,
    "development_cost_forcing": 60000000,
    "time_to_permit_years": 2.0,
    "volatility": 0.20,
    "risk_free_rate": 0.1375
  },
  "esg": {
    "certification": "NONE",
    "green_premium": 0,
    "brown_discount": 0
  }
}
```

**Response (202 Accepted):**
```json
{
  "simulation_id": "uuid",
  "status": "PENDING",
  "result": null
}
```

---

### Get Simulation Status

```
GET /simulation/{simulation_id}
```

**Authentication:** Required

**Response (Completed):**
```json
{
  "simulation_id": "uuid",
  "status": "COMPLETED",
  "result": {
    "npv": 15000000.00,
    "irr": 18.5,
    "roe": 0.45,
    "payback_months": 28,
    "exposure_max": 35000000.00,
    "esg_adjusted_npv": 15500000.00,
    "real_option_land_value": 2500000.00
  },
  "error": null
}
```

**Status Values:**
- `PENDING` - Queued for processing
- `PROCESSING` - Currently being calculated
- `COMPLETED` - Results available
- `FAILED` - Error occurred

---

### List Simulations

```
GET /simulations?limit=10&offset=0
```

**Authentication:** Required

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Project Alpha",
    "status": "COMPLETED",
    "created_at": "2025-12-17T10:00:00Z"
  }
]
```

---

### Recent Simulations

```
GET /simulations/recent?limit=5
```

**Authentication:** Required

**Response:** Same as List Simulations

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication required. Please provide a valid Bearer token."
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied. Required role: admin"
}
```

### 404 Not Found
```json
{
  "detail": "Simulation not found"
}
```

### 429 Too Many Requests
```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Please wait 30 seconds.",
  "retry_after": 30,
  "limit_type": "minute",
  "requests_made": 60,
  "requests_allowed": 60
}
```

### 500 Internal Server Error
```json
{
  "detail": "Database Persistence Failed: connection error"
}
```

---

## Data Models

### ProjectTIV

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique project identifier |
| name | string | Yes | Project name |
| is_mixed_use | boolean | No | IT-11 mixed-use flag |
| separate_access_cores | boolean | No | IT-11 compliance |
| fire_load_category | string | No | Fire safety category |
| efficiency | float | No | Sellable/Total area ratio |
| financial_input | P10FinancialInput | No | Financial parameters |
| real_options | RealOptionsInput | No | Black-Scholes parameters |
| esg | ESGAttributes | No | ESG certifications |

### P10FinancialInput

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total_units | integer | Yes | Number of units |
| sales_price_avg | decimal | Yes | Average price per sqm |
| construction_cost_total | decimal | Yes | Total construction cost |
| land_cost | decimal | Yes | Land acquisition cost |
| development_months | integer | Yes | Development timeline |

### P10FinancialOutput

| Field | Type | Description |
|-------|------|-------------|
| npv | decimal | Net Present Value |
| irr | float | Internal Rate of Return (%) |
| roe | float | Return on Equity (dynamic) |
| payback_months | integer | Payback period (dynamic) |
| exposure_max | decimal | Maximum cash exposure (dynamic) |
| esg_adjusted_npv | decimal | NPV with ESG adjustments |
| real_option_land_value | float | Black-Scholes land value |

---

## Changelog

### v6.1.0-SINGULARITY
- Added JWT authentication to all protected endpoints
- Implemented rate limiting (60/min global, 30/min simulations)
- Dynamic ROE, Payback, and Max Exposure calculations
- Security headers and CORS configuration

### v6.0.0
- Initial release
- Basic simulation endpoints
- Real Options calculation
- ESG adjustments

---

**Copyright 2025 VERTIV CAPITAL. All Rights Reserved.**
