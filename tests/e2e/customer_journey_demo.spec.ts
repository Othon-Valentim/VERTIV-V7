import { test, expect } from '@playwright/test';

test('Complete Customer Journey Simulation', async ({ page }) => {
  // Pre-verified demo user (created via Supabase Admin API)
  const email = 'demo@vertiv.tech';
  const password = 'Vertiv2026!';

  // 1. Landing Page
  await page.goto('/');
  await expect(page).toHaveTitle(/VERTIV/);
  
  // Smooth scroll
  await page.mouse.wheel(0, 500);
  await page.waitForTimeout(1000);
  await page.mouse.wheel(0, 500);
  await page.waitForTimeout(1000);

  // 2. Go to Login (pre-verified user, skip registration)
  await page.click('text=Entrar');
  await expect(page).toHaveURL(/auth\/login/);

  // 3. Login with pre-verified demo user
  await page.fill('input[type="email"]', email);
  await page.fill('input[type="password"]', password);
  await page.click('button[type="submit"]');

  // Wait for wizard
  await page.waitForURL(/wizard/, { timeout: 15000 });

  // 5. TIV Wizard - Step 1
  await expect(page.locator('body')).toContainText(/Garimpo/);
  await page.fill('placeholder="Nome do empreendimento"', 'Residencial Jardins do Sol');
  await page.fill('placeholder="Ex: 5000"', '5000');
  await page.fill('placeholder="Ex: 15.000.000"', '15000000');
  
  await page.click('text=Analisar Viabilidade');
  
  // Wait for results
  await page.waitForTimeout(5000); // Simulated processing time to show UI
  
  // 6. Next Steps
  await page.click('text=Próximo Passo');
  await page.waitForTimeout(2000);
  
  // Step 2
  await expect(page.locator('body')).toContainText(/Dinâmica Econômica/);
  await page.waitForTimeout(2000);
  
  // Step 4 (Vocação)
  await page.click('text=Próximo Passo'); // From P2 to P3 (Area de Influencia)
  await page.waitForTimeout(1000);
  await page.click('text=Próximo Passo'); // From P3 to P4 (Vocation)
  await page.waitForTimeout(2000);
  
  await expect(page.locator('body')).toContainText(/Vocação/);

  // Finalize
  await page.click('text=Sair');
});
