import { test, expect } from '@playwright/test';

test('debug login', async ({ page }) => {
  // Capturar erros de console
  const consoleErrors: string[] = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
    }
    console.log(`[BROWSER ${msg.type()}]:`, msg.text());
  });

  // Capturar erros de rede
  page.on('response', response => {
    if (response.status() >= 400) {
      console.log(`[HTTP ${response.status()}]: ${response.url()}`);
    }
  });

  // Ir para página de login
  const BASE_URL = process.env.BASE_URL || 'http://localhost:3003';
  await page.goto(`${BASE_URL}/auth/login`);
  await page.waitForLoadState('networkidle');

  console.log('Page loaded, filling form...');

  // Preencher campos
  const emailField = page.getByPlaceholder('seu@email.com');
  const passwordField = page.getByPlaceholder('••••••••');

  await emailField.fill('othonciclo21@gmail.com');
  await passwordField.fill('Theo@02052018');

  console.log('Form filled, clicking login...');

  // Clicar no botão
  const loginButton = page.getByRole('button', { name: /entrar na plataforma/i });
  await loginButton.click();

  // Aguardar para ver se redireciona ou mostra erro
  console.log('Waiting for response...');

  // Aguardar mudança de URL ou timeout
  try {
    await page.waitForURL(/\/(wizard|dashboard)/, { timeout: 10000 });
    console.log('SUCCESS! Redirected to:', page.url());
  } catch (e) {
    console.log('No redirect. Current URL:', page.url());

    // Verificar se há mensagem de erro na página
    const errorMessage = await page.locator('.text-destructive, [class*="error"]').first().textContent().catch(() => null);
    console.log('Error message on page:', errorMessage);

    // Screenshot
    await page.screenshot({ path: 'tests/e2e/screenshots/debug_login_failed.png', fullPage: true });
  }

  console.log('Console errors:', consoleErrors);
});
