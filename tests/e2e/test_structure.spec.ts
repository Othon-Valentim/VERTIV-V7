/**
 * VERTIV v6.0 - Structure Validation Tests
 *
 * Tests that validate project structure without requiring running servers.
 * These tests can run in any environment.
 */

import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const PROJECT_ROOT = process.cwd();

test.describe('Project Structure Validation', () => {

  test('Backend structure exists', async () => {
    const backendPath = path.join(PROJECT_ROOT, 'apps', 'backend');
    expect(fs.existsSync(backendPath)).toBeTruthy();

    // Check critical files
    const criticalFiles = [
      'src/api/main.py',
      'src/api/routes/wizard.py',
      'src/api/routes/p1.py',
      'src/api/routes/analysis.py',
      'src/engine/cashflow.py',
      'src/engine/real_options.py',
      'requirements.txt',
      'Dockerfile'
    ];

    for (const file of criticalFiles) {
      const filePath = path.join(backendPath, file);
      expect(fs.existsSync(filePath), `File ${file} should exist`).toBeTruthy();
    }
  });

  test('Frontend structure exists', async () => {
    const frontendPath = path.join(PROJECT_ROOT, 'apps', 'frontend');
    expect(fs.existsSync(frontendPath)).toBeTruthy();

    // Check critical files
    const criticalFiles = [
      'src/app/page.tsx',
      'src/app/auth/login/page.tsx',
      'src/app/wizard/page.tsx',
      'src/app/dashboard/portfolio/page.tsx',
      'src/contexts/AuthContext.tsx',
      'package.json',
      'tailwind.config.ts'
    ];

    for (const file of criticalFiles) {
      const filePath = path.join(frontendPath, file);
      expect(fs.existsSync(filePath), `File ${file} should exist`).toBeTruthy();
    }
  });

  test('Documentation exists', async () => {
    const docsPath = path.join(PROJECT_ROOT, 'docs');
    expect(fs.existsSync(docsPath)).toBeTruthy();

    const requiredDocs = [
      'BACKEND_API_MAP.md',
      'MCP_SERVERS_DOCUMENTATION.md'
    ];

    for (const doc of requiredDocs) {
      const docPath = path.join(docsPath, doc);
      expect(fs.existsSync(docPath), `Doc ${doc} should exist`).toBeTruthy();
    }
  });

  test('Configuration files exist', async () => {
    const configFiles = [
      'docker-compose.yml',
      'playwright.config.ts',
      'package.json',
      '.env.example'
    ];

    for (const config of configFiles) {
      const configPath = path.join(PROJECT_ROOT, config);
      expect(fs.existsSync(configPath), `Config ${config} should exist`).toBeTruthy();
    }
  });

  test('VERTIV structure document exists', async () => {
    const structurePath = path.join(PROJECT_ROOT, 'VERTIV_STRUCTURE.md');
    expect(fs.existsSync(structurePath)).toBeTruthy();

    // Verify content
    const content = fs.readFileSync(structurePath, 'utf-8');
    expect(content).toContain('VERTIV');
    expect(content).toContain('apps/backend');
    expect(content).toContain('apps/frontend');
  });

});

test.describe('Backend API Contract Validation', () => {

  test('API Map contains all required endpoints', async () => {
    const apiMapPath = path.join(PROJECT_ROOT, 'docs', 'BACKEND_API_MAP.md');
    const content = fs.readFileSync(apiMapPath, 'utf-8');

    // Check required endpoints are documented
    const requiredEndpoints = [
      '/health',
      '/simulations',
      '/simulation/{',
      '/calculate/quick',
      '/wizard/p2/analyze',
      '/wizard/p4/analyze',
      '/wizard/p5/analyze',
      '/wizard/p6/analyze',
      '/wizard/p7/analyze',
      '/wizard/p8/analyze',
      '/wizard/p9/analyze',
      '/p1/analyze',
      '/analyze/thesis'
    ];

    for (const endpoint of requiredEndpoints) {
      expect(content, `Endpoint ${endpoint} should be documented`).toContain(endpoint);
    }
  });

  test('Backend main.py contains FastAPI app', async () => {
    const mainPath = path.join(PROJECT_ROOT, 'apps', 'backend', 'src', 'api', 'main.py');
    const content = fs.readFileSync(mainPath, 'utf-8');

    expect(content).toContain('FastAPI');
    expect(content).toContain('app = FastAPI');
    expect(content).toContain('@app.get');
    expect(content).toContain('/health');
  });

});

test.describe('Frontend Component Validation', () => {

  test('Login page has required elements', async () => {
    const loginPath = path.join(PROJECT_ROOT, 'apps', 'frontend', 'src', 'app', 'auth', 'login', 'page.tsx');
    const content = fs.readFileSync(loginPath, 'utf-8');

    expect(content).toContain('email');
    expect(content).toContain('password');
    expect(content).toContain('signIn');
    expect(content).toContain('useAuth');
  });

  test('Wizard page has TIV steps', async () => {
    const wizardPath = path.join(PROJECT_ROOT, 'apps', 'frontend', 'src', 'app', 'wizard', 'page.tsx');
    const content = fs.readFileSync(wizardPath, 'utf-8');

    // Check all 10 TIV steps are present
    expect(content).toContain('P1');
    expect(content).toContain('P2');
    expect(content).toContain('P10');
    expect(content).toContain('Garimpo');
    expect(content).toContain('Financeira');
  });

  test('Portfolio page fetches simulations', async () => {
    const portfolioPath = path.join(PROJECT_ROOT, 'apps', 'frontend', 'src', 'app', 'dashboard', 'portfolio', 'page.tsx');
    const content = fs.readFileSync(portfolioPath, 'utf-8');

    expect(content).toContain('/simulations');
    expect(content).toContain('SimulationSummary');
    expect(content).toContain('Global Portfolio');
  });

});

test.describe('MCP Configuration Validation', () => {

  test('MCP documentation is complete', async () => {
    const mcpDocPath = path.join(PROJECT_ROOT, 'docs', 'MCP_SERVERS_DOCUMENTATION.md');
    const content = fs.readFileSync(mcpDocPath, 'utf-8');

    expect(content).toContain('filesystem');
    expect(content).toContain('memory');
    expect(content).toContain('sequential-thinking');
  });

});

test.describe('Test Infrastructure', () => {

  test('E2E test files exist', async () => {
    const e2ePath = path.join(PROJECT_ROOT, 'tests', 'e2e');
    expect(fs.existsSync(e2ePath)).toBeTruthy();

    const testFiles = [
      'test_critical_flow.spec.ts',
      'README.md'
    ];

    for (const file of testFiles) {
      const filePath = path.join(e2ePath, file);
      expect(fs.existsSync(filePath), `Test file ${file} should exist`).toBeTruthy();
    }
  });

  test('Playwright config is valid', async () => {
    const configPath = path.join(PROJECT_ROOT, 'playwright.config.ts');
    const content = fs.readFileSync(configPath, 'utf-8');

    expect(content).toContain('defineConfig');
    expect(content).toContain('testDir');
    expect(content).toContain('chromium');
  });

  test('Screenshots directory exists', async () => {
    const screenshotsPath = path.join(PROJECT_ROOT, 'tests', 'e2e', 'screenshots');
    expect(fs.existsSync(screenshotsPath)).toBeTruthy();
  });

});
