# VERTIV E2E Tests

## Overview

End-to-end tests for VERTIV v6.0 critical flows using Playwright.

## Prerequisites

- Node.js 18+
- npm 9+
- Frontend running on `http://localhost:3000`
- Backend running on `http://localhost:8000`

## Installation

```bash
# Install root dependencies
npm install

# Install Playwright browsers
npm run playwright:install
```

## Running Tests

### All Tests
```bash
npm run test:e2e
```

### With UI Mode (Interactive)
```bash
npm run test:e2e:ui
```

### Headed Mode (See Browser)
```bash
npm run test:e2e:headed
```

### Debug Mode
```bash
npm run test:e2e:debug
```

### Specific Browser
```bash
# Chrome only
npm run test:e2e:chrome

# Firefox only
npm run test:e2e:firefox

# Safari only
npm run test:e2e:webkit

# Mobile browsers
npm run test:e2e:mobile
```

### Generate Test Code
```bash
npm run test:e2e:codegen
```

### View Report
```bash
npm run test:e2e:report
```

## Test Structure

```
tests/e2e/
  +-- test_critical_flow.spec.ts  # Main test file
  +-- screenshots/                 # Test screenshots
  +-- reports/                     # HTML reports
  +-- test-results/               # Artifacts
```

## Critical Flow Tests

1. **Login Page Access** - Verify login form renders
2. **User Login** - Test authentication flow
3. **Simulations List** - View portfolio dashboard
4. **Simulation Details** - Open specific simulation
5. **Quick Calculation** - Execute via wizard
6. **API Validation** - Backend health checks
7. **Full E2E Flow** - Complete user journey

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | http://localhost:3000 | Frontend URL |
| `API_URL` | http://localhost:8000 | Backend API URL |
| `TEST_EMAIL` | test@example.com | Test user email |
| `TEST_PASSWORD` | password123 | Test user password |
| `CI` | false | CI mode flag |

## Screenshots

Screenshots are saved to `tests/e2e/screenshots/` with timestamps:
- `01_login_page_*.png`
- `02_after_login_*.png`
- `03_simulations_list_*.png`
- `04_simulation_details_*.png`
- `05_wizard_calculation_*.png`
- `07_final_wizard_state_*.png`

## CI/CD Integration

For GitHub Actions, add to workflow:

```yaml
- name: Install Playwright
  run: npx playwright install --with-deps

- name: Run E2E Tests
  run: npm run test:e2e
  env:
    CI: true
    BASE_URL: http://localhost:3000
    API_URL: http://localhost:8000
```

## Troubleshooting

### Tests fail with timeout
1. Ensure frontend is running: `npm run dev:frontend`
2. Ensure backend is running: `npm run dev:backend`
3. Increase timeout in `playwright.config.ts`

### Login fails
1. Check if test user exists in Supabase
2. Verify credentials in environment variables

### Screenshots not taken
1. Check `tests/e2e/screenshots/` directory exists
2. Verify write permissions
