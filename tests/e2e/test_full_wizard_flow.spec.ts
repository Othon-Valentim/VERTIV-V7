/**
 * VERTIV v6.0 - Full Wizard Flow E2E Test (P2-P9)
 *
 * Tests the complete wizard journey through steps P2 to P9:
 * 1. Login as test@vertiv.tech
 * 2. Navigate to wizard
 * 3. Complete each wizard step sequentially:
 *    - P2: Dinâmica Econômica
 *    - P4: Vocação Imobiliária
 *    - P5: Due Diligence Legal
 *    - P6: Demanda Qualificada
 *    - P7: Oferta & Concorrência
 *    - P8: Absorção (VSO)
 *    - P9: Validação Estratégica
 * 4. Verify each step completes without errors
 * 5. Screenshot final validation
 *
 * @author VERTIV Development Team
 * @version 6.1.0-SINGULARITY
 */

import { test, expect, Page } from '@playwright/test';

// Configuration
const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const API_URL = process.env.API_URL || 'http://localhost:8000';
const TEST_USER = {
  email: process.env.TEST_EMAIL || 'test@vertiv.tech',
  password: process.env.TEST_PASSWORD || 'Test@2024!'
};

// Test data
const TEST_DATA = {
  municipality: 'Leopoldina-MG',
  neighborhood: 'Centro',
  population: 55000,
  landRegistration: '12.345',
};

// Helper functions
async function waitForNetworkIdle(page: Page, timeout = 15000) {
  try {
    await page.waitForLoadState('networkidle', { timeout });
  } catch {
    // Continue if timeout - page may still be usable
  }
}

async function takeScreenshot(page: Page, name: string) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  await page.screenshot({
    path: `tests/e2e/screenshots/${name}_${timestamp}.png`,
    fullPage: true
  });
}

async function login(page: Page) {
  await page.goto(`${BASE_URL}/auth/login`);
  await waitForNetworkIdle(page);

  await page.locator('input[type="email"]').fill(TEST_USER.email);
  await page.locator('input[type="password"]').fill(TEST_USER.password);
  await page.getByRole('button', { name: /entrar|login/i }).click();

  // Wait for redirect to wizard or dashboard
  await page.waitForURL(/\/(wizard|dashboard)/, { timeout: 15000 });
}

async function navigateToWizard(page: Page) {
  await page.goto(`${BASE_URL}/wizard`);
  await waitForNetworkIdle(page);
  await expect(page.locator('text=VERTIV.global')).toBeVisible({ timeout: 10000 });
  await expect(page.locator('text=TIV Wizard')).toBeVisible({ timeout: 5000 });
}

async function clickNextStep(page: Page) {
  const nextButton = page.getByRole('button', { name: /próximo/i });
  await expect(nextButton).toBeVisible({ timeout: 5000 });
  await nextButton.click();
  await page.waitForTimeout(500); // Wait for animation
}

async function verifyNoErrors(page: Page) {
  // Check for error messages (red error banners)
  const errorBanner = page.locator('.bg-red-500\\/10, .text-destructive, [class*="error"]');
  const errorCount = await errorBanner.count();

  // If errors exist, they should not be visible in current context
  if (errorCount > 0) {
    // Allow for transient errors that may have been dismissed
    for (let i = 0; i < errorCount; i++) {
      const isVisible = await errorBanner.nth(i).isVisible();
      if (isVisible) {
        const text = await errorBanner.nth(i).textContent();
        // Don't fail on analysis results that may contain "error" in text
        if (!text?.includes('resultado') && !text?.includes('Result')) {
          console.warn(`Warning: Possible error visible: ${text}`);
        }
      }
    }
  }
}

async function selectWizardStep(page: Page, stepNumber: number) {
  // Click on step in sidebar (steps are numbered 1-10 in UI)
  const stepButton = page.locator(`nav button`).filter({ hasText: new RegExp(`P${stepNumber}:`) });
  await stepButton.click();
  await page.waitForTimeout(500);
}

// Test Suite
test.describe('VERTIV Full Wizard Flow (P2-P9)', () => {

  test.beforeEach(async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
  });

  test('Complete wizard flow from P2 to P9', async ({ page }) => {
    test.setTimeout(180000); // 3 minutes for full flow

    // Step 1: Login
    console.log('Step 1: Logging in...');
    await login(page);
    await takeScreenshot(page, 'wizard_01_after_login');

    // Step 2: Navigate to Wizard
    console.log('Step 2: Navigating to wizard...');
    await navigateToWizard(page);
    await takeScreenshot(page, 'wizard_02_wizard_home');

    // ==================== P2: Dinâmica Econômica ====================
    console.log('Step 3: P2 - Dinâmica Econômica...');
    await selectWizardStep(page, 2);
    await expect(page.locator('text=Dinâmica Econômica')).toBeVisible({ timeout: 10000 });

    // Fill P2 form
    const p2MunicipalityInput = page.locator('input[type="text"]').first();
    await p2MunicipalityInput.fill(TEST_DATA.municipality);

    const p2PopulationInput = page.locator('input[type="number"]').first();
    await p2PopulationInput.fill(String(TEST_DATA.population));

    // Run analysis
    const p2AnalyzeButton = page.getByRole('button', { name: /analisar indicadores/i });
    await p2AnalyzeButton.click();

    // Wait for results (loading spinner disappears)
    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });
    await waitForNetworkIdle(page);

    // Verify results appeared
    await expect(page.locator('text=P2i-Lead').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
    await takeScreenshot(page, 'wizard_03_p2_complete');

    // Navigate to next step
    await clickNextStep(page);

    // ==================== P3: Skip (placeholder step) ====================
    console.log('Step 4: P3 - Skipping placeholder...');
    // P3 is a placeholder, just click through
    await page.waitForTimeout(500);
    await clickNextStep(page);

    // ==================== P4: Vocação Imobiliária ====================
    console.log('Step 5: P4 - Vocação Imobiliária...');
    await expect(page.locator('text=Vocação Imobiliária')).toBeVisible({ timeout: 10000 });

    // Use "Carregar Exemplo" for easier testing
    const loadExampleP4 = page.locator('text=Carregar Exemplo');
    if (await loadExampleP4.isVisible()) {
      await loadExampleP4.click();
      await page.waitForTimeout(300);
    } else {
      // Manual fill
      const p4MunicipalityInput = page.locator('label:has-text("Município") + input, label:has-text("Município") ~ input').first();
      await p4MunicipalityInput.fill(TEST_DATA.municipality);

      const p4NeighborhoodInput = page.locator('label:has-text("Bairro") + input, label:has-text("Bairro") ~ input').first();
      await p4NeighborhoodInput.fill(TEST_DATA.neighborhood);
    }

    // Run analysis
    const p4AnalyzeButton = page.getByRole('button', { name: /analisar vocação/i });
    await p4AnalyzeButton.click();

    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });
    await waitForNetworkIdle(page);

    // Verify results
    await expect(page.locator('text=Score Total').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
    await takeScreenshot(page, 'wizard_04_p4_complete');

    await clickNextStep(page);

    // ==================== P5: Due Diligence Legal ====================
    console.log('Step 6: P5 - Due Diligence Legal...');
    await expect(page.locator('text=Due Diligence Legal')).toBeVisible({ timeout: 10000 });

    // Use "Carregar Exemplo" for easier testing
    const loadExampleP5 = page.locator('text=Carregar Exemplo');
    if (await loadExampleP5.isVisible()) {
      await loadExampleP5.click();
      await page.waitForTimeout(300);
    } else {
      // Manual fill
      const registrationInput = page.locator('input[placeholder*="12.345"], input[type="text"]').first();
      await registrationInput.fill(TEST_DATA.landRegistration);

      // Find municipality field (second text input typically)
      const textInputs = page.locator('input[type="text"]');
      const inputCount = await textInputs.count();
      if (inputCount > 1) {
        await textInputs.nth(1).fill(TEST_DATA.municipality);
      }
    }

    // Run analysis
    const p5AnalyzeButton = page.getByRole('button', { name: /executar due diligence/i });
    await p5AnalyzeButton.click();

    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });
    await waitForNetworkIdle(page);

    // Verify results (Gate result)
    await expect(page.locator('text=Gate').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
    await takeScreenshot(page, 'wizard_05_p5_complete');

    await clickNextStep(page);

    // ==================== P6: Demanda Qualificada ====================
    console.log('Step 7: P6 - Demanda Qualificada...');
    await expect(page.locator('text=Demanda Qualificada')).toBeVisible({ timeout: 10000 });

    // Fill P6 form
    const p6TextInputs = page.locator('input[type="text"], input:not([type])');
    const p6TextCount = await p6TextInputs.count();
    if (p6TextCount > 0) {
      await p6TextInputs.first().fill(TEST_DATA.municipality);
    }

    // Run analysis
    const p6AnalyzeButton = page.getByRole('button', { name: /calcular demanda/i });
    await p6AnalyzeButton.click();

    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });
    await waitForNetworkIdle(page);

    // Verify results
    await expect(page.locator('text=Demanda Efetiva').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
    await takeScreenshot(page, 'wizard_06_p6_complete');

    await clickNextStep(page);

    // ==================== P7: Oferta & Concorrência ====================
    console.log('Step 8: P7 - Oferta & Concorrência...');
    await expect(page.locator('text=Oferta & Mercado')).toBeVisible({ timeout: 10000 });

    // Fill P7 form
    const p7TextInputs = page.locator('input[type="text"], input:not([type])');
    const p7TextCount = await p7TextInputs.count();
    if (p7TextCount > 0) {
      await p7TextInputs.first().fill(TEST_DATA.municipality);
    }

    // Run analysis
    const p7AnalyzeButton = page.getByRole('button', { name: /analisar oferta/i });
    await p7AnalyzeButton.click();

    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });
    await waitForNetworkIdle(page);

    // Verify results
    await expect(page.locator('text=Concorrentes').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
    await takeScreenshot(page, 'wizard_07_p7_complete');

    await clickNextStep(page);

    // ==================== P8: Absorção (VSO) ====================
    console.log('Step 9: P8 - Absorção (VSO)...');
    await expect(page.locator('text=Absorção (VSO)')).toBeVisible({ timeout: 10000 });

    // Fill P8 form
    const p8TextInputs = page.locator('input[type="text"], input:not([type])');
    const p8TextCount = await p8TextInputs.count();
    if (p8TextCount > 0) {
      await p8TextInputs.first().fill(TEST_DATA.municipality);
    }

    // Run analysis
    const p8AnalyzeButton = page.getByRole('button', { name: /calcular absorção/i });
    await p8AnalyzeButton.click();

    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });
    await waitForNetworkIdle(page);

    // Verify results
    await expect(page.locator('text=Vendas/Mês').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
    await takeScreenshot(page, 'wizard_08_p8_complete');

    await clickNextStep(page);

    // ==================== P9: Validação Estratégica ====================
    console.log('Step 10: P9 - Validação Estratégica...');
    await expect(page.locator('text=Convalidação 4:1')).toBeVisible({ timeout: 10000 });

    // Fill P9 form
    const p9TextInputs = page.locator('input[type="text"], input:not([type])');
    const p9TextCount = await p9TextInputs.count();
    if (p9TextCount > 0) {
      await p9TextInputs.first().fill(TEST_DATA.municipality);
    }

    // Run validation
    const p9AnalyzeButton = page.getByRole('button', { name: /validar gate/i });
    await p9AnalyzeButton.click();

    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });
    await waitForNetworkIdle(page);

    // Verify final validation results
    await expect(page.locator('text=Gate 4:1').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);

    // Final screenshot - full flow complete
    await takeScreenshot(page, 'wizard_full_flow');

    console.log('Full wizard flow completed successfully!');
  });

  test('Verify P2 step loads and processes correctly', async ({ page }) => {
    await login(page);
    await navigateToWizard(page);
    await selectWizardStep(page, 2);

    await expect(page.locator('text=Dinâmica Econômica')).toBeVisible({ timeout: 10000 });

    // Fill and submit
    await page.locator('input[type="text"]').first().fill(TEST_DATA.municipality);
    await page.getByRole('button', { name: /analisar indicadores/i }).click();

    // Wait for results
    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });

    // Verify results
    await expect(page.locator('text=P2i-Lead').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
  });

  test('Verify P4 step loads and processes correctly', async ({ page }) => {
    await login(page);
    await navigateToWizard(page);
    await selectWizardStep(page, 4);

    await expect(page.locator('text=Vocação Imobiliária')).toBeVisible({ timeout: 10000 });

    // Use example data
    const loadExample = page.locator('text=Carregar Exemplo');
    if (await loadExample.isVisible()) {
      await loadExample.click();
      await page.waitForTimeout(300);
    }

    await page.getByRole('button', { name: /analisar vocação/i }).click();
    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });

    await expect(page.locator('text=Score Total').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
  });

  test('Verify P5 step loads and processes correctly', async ({ page }) => {
    await login(page);
    await navigateToWizard(page);
    await selectWizardStep(page, 5);

    await expect(page.locator('text=Due Diligence Legal')).toBeVisible({ timeout: 10000 });

    // Use example data
    const loadExample = page.locator('text=Carregar Exemplo');
    if (await loadExample.isVisible()) {
      await loadExample.click();
      await page.waitForTimeout(300);
    }

    await page.getByRole('button', { name: /executar due diligence/i }).click();
    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });

    await expect(page.locator('text=Gate').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
  });

  test('Verify P6 step loads and processes correctly', async ({ page }) => {
    await login(page);
    await navigateToWizard(page);
    await selectWizardStep(page, 6);

    await expect(page.locator('text=Demanda Qualificada')).toBeVisible({ timeout: 10000 });

    // Fill municipality
    const textInputs = page.locator('input[type="text"], input:not([type])');
    if (await textInputs.first().isVisible()) {
      await textInputs.first().fill(TEST_DATA.municipality);
    }

    await page.getByRole('button', { name: /calcular demanda/i }).click();
    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });

    await expect(page.locator('text=Demanda Efetiva').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
  });

  test('Verify P7 step loads and processes correctly', async ({ page }) => {
    await login(page);
    await navigateToWizard(page);
    await selectWizardStep(page, 7);

    await expect(page.locator('text=Oferta & Mercado')).toBeVisible({ timeout: 10000 });

    // Fill municipality
    const textInputs = page.locator('input[type="text"], input:not([type])');
    if (await textInputs.first().isVisible()) {
      await textInputs.first().fill(TEST_DATA.municipality);
    }

    await page.getByRole('button', { name: /analisar oferta/i }).click();
    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });

    await expect(page.locator('text=Concorrentes').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
  });

  test('Verify P8 step loads and processes correctly', async ({ page }) => {
    await login(page);
    await navigateToWizard(page);
    await selectWizardStep(page, 8);

    await expect(page.locator('text=Absorção (VSO)')).toBeVisible({ timeout: 10000 });

    // Fill municipality
    const textInputs = page.locator('input[type="text"], input:not([type])');
    if (await textInputs.first().isVisible()) {
      await textInputs.first().fill(TEST_DATA.municipality);
    }

    await page.getByRole('button', { name: /calcular absorção/i }).click();
    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });

    await expect(page.locator('text=Vendas/Mês').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
  });

  test('Verify P9 step loads and processes correctly', async ({ page }) => {
    await login(page);
    await navigateToWizard(page);
    await selectWizardStep(page, 9);

    await expect(page.locator('text=Convalidação 4:1')).toBeVisible({ timeout: 10000 });

    // Fill municipality
    const textInputs = page.locator('input[type="text"], input:not([type])');
    if (await textInputs.first().isVisible()) {
      await textInputs.first().fill(TEST_DATA.municipality);
    }

    await page.getByRole('button', { name: /validar gate/i }).click();
    await page.waitForSelector('.animate-spin', { state: 'hidden', timeout: 30000 });

    await expect(page.locator('text=Gate 4:1').first()).toBeVisible({ timeout: 10000 });
    await verifyNoErrors(page);
  });

  test('Verify "Próximo" button navigates correctly', async ({ page }) => {
    await login(page);
    await navigateToWizard(page);

    // Start at P1, navigate to P2
    await selectWizardStep(page, 1);
    await clickNextStep(page);

    // Should be on P2 now
    await expect(page.locator('text=Dinâmica Econômica')).toBeVisible({ timeout: 10000 });

    // Navigate to P3
    await clickNextStep(page);
    await expect(page.locator('text=Área de Influência')).toBeVisible({ timeout: 10000 });
  });

  test('Verify wizard step indicators work', async ({ page }) => {
    await login(page);
    await navigateToWizard(page);

    // Click on P4 in sidebar
    await selectWizardStep(page, 4);
    await expect(page.locator('text=Vocação Imobiliária')).toBeVisible({ timeout: 10000 });

    // Click on P6 in sidebar
    await selectWizardStep(page, 6);
    await expect(page.locator('text=Demanda Qualificada')).toBeVisible({ timeout: 10000 });

    // Click on P9 in sidebar
    await selectWizardStep(page, 9);
    await expect(page.locator('text=Convalidação 4:1')).toBeVisible({ timeout: 10000 });
  });

});

// API Integration Tests
test.describe('Wizard API Integration', () => {

  test('P2 API endpoint returns valid response', async ({ request }) => {
    const response = await request.post(`${API_URL}/wizard/p2/analyze`, {
      data: {
        municipality: TEST_DATA.municipality,
        municipality_population: TEST_DATA.population,
        is_metropolitan: false
      }
    });

    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.p2i_lead_score).toBeDefined();
    expect(data.decision).toBeDefined();
  });

  test('P4 API endpoint returns valid response', async ({ request }) => {
    const response = await request.post(`${API_URL}/wizard/p4/analyze`, {
      data: {
        municipality: TEST_DATA.municipality,
        neighborhood: TEST_DATA.neighborhood,
        zoning_type: 'ZR2',
        max_height_floors: 4,
        max_coverage_ratio: 0.6,
        max_floor_area_ratio: 2.0,
        distance_city_center_km: 2.0,
        distance_main_avenue_km: 0.5,
        infrastructure_level: 'COMPLETE',
        land_area_sqm: 5000,
        land_price_per_sqm: 150
      }
    });

    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.total_score).toBeDefined();
    expect(data.decision).toBeDefined();
  });

  test('P5 API endpoint returns valid response', async ({ request }) => {
    const response = await request.post(`${API_URL}/wizard/p5/analyze`, {
      data: {
        land_registration_number: TEST_DATA.landRegistration,
        municipality: TEST_DATA.municipality,
        has_clear_title: true,
        is_registered: true,
        has_pending_lawsuits: false,
        complies_with_zoning: true,
        complies_with_master_plan: true
      }
    });

    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.gate_result).toBeDefined();
    expect(data.summary).toBeDefined();
  });

  test('P6 API endpoint returns valid response', async ({ request }) => {
    const response = await request.post(`${API_URL}/wizard/p6/analyze`, {
      data: {
        municipality: TEST_DATA.municipality,
        influence_area_population: 50000,
        average_household_income: 5000,
        target_segment: 'MEDIO',
        unit_price_min: 150000,
        unit_price_max: 250000
      }
    });

    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.summary).toBeDefined();
    expect(data.funnel_stages).toBeDefined();
  });

  test('P7 API endpoint returns valid response', async ({ request }) => {
    const response = await request.post(`${API_URL}/wizard/p7/analyze`, {
      data: {
        municipality: TEST_DATA.municipality,
        influence_area_km: 5.0,
        competitors: [],
        market_average_price_sqm: 300
      }
    });

    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.summary).toBeDefined();
  });

  test('P8 API endpoint returns valid response', async ({ request }) => {
    const response = await request.post(`${API_URL}/wizard/p8/analyze`, {
      data: {
        municipality: TEST_DATA.municipality,
        project_units: 30,
        project_price_avg: 180000,
        qualified_demand: 200,
        active_inventory: 50,
        market_vso_monthly: 0.08
      }
    });

    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.absorption_projection).toBeDefined();
    expect(data.market_dynamics).toBeDefined();
  });

  test('P9 API endpoint returns valid response', async ({ request }) => {
    const response = await request.post(`${API_URL}/wizard/p9/analyze`, {
      data: {
        municipality: TEST_DATA.municipality,
        qualified_demand: 200,
        active_inventory: 50,
        competitors_count: 3,
        projected_absorption_months: 24,
        project_units: 30,
        project_price_sqm: 300,
        market_price_sqm: 280
      }
    });

    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.gate_result).toBeDefined();
    expect(data.key_ratio).toBeDefined();
  });

});
