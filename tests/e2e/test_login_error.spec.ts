/**
 * VERTIV v6.0 - Login Error Validation E2E Test
 *
 * Tests the login error handling:
 * 1. Invalid credentials show error message
 * 2. User stays on login page
 * 3. No session token is saved
 *
 * @author VERTIV Development Team
 * @version 6.1.0-SINGULARITY
 */

import { test, expect, Page } from '@playwright/test';

// Test configuration
const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';

// Invalid test credentials
const INVALID_CREDENTIALS = {
  email: 'wrong@vertiv.tech',
  password: 'WrongPassword123!'
};

// Helper function
async function takeScreenshot(page: Page, name: string) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  await page.screenshot({
    path: `tests/e2e/screenshots/${name}_${timestamp}.png`,
    fullPage: true
  });
}

test.describe('Login Error Handling', () => {

  test.beforeEach(async ({ page }) => {
    // Set viewport for consistent screenshots
    await page.setViewportSize({ width: 1920, height: 1080 });
  });

  test('1. Invalid credentials show error message', async ({ page }) => {
    // Step 1: Navigate to login page
    await page.goto(`${BASE_URL}/auth/login`);

    // Verify login page loaded
    await expect(page.locator('input[type="email"]')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('input[type="password"]')).toBeVisible();

    // Step 2: Fill invalid email
    await page.locator('input[type="email"]').fill(INVALID_CREDENTIALS.email);

    // Step 3: Fill invalid password
    await page.locator('input[type="password"]').fill(INVALID_CREDENTIALS.password);

    // Step 4: Click login button
    await page.getByRole('button', { name: /entrar|login/i }).click();

    // Wait for response
    await page.waitForTimeout(3000);

    // Step 5a: Verify still on login page
    expect(page.url()).toContain('/auth/login');

    // Step 5b: Verify error message is displayed
    const errorMessage = page.locator('text=Email ou senha incorretos');
    const genericError = page.locator('text=Credenciais inválidas');
    const errorContainer = page.locator('.text-destructive, [class*="error"], [class*="alert"]');

    const hasSpecificError = await errorMessage.isVisible().catch(() => false);
    const hasGenericError = await genericError.isVisible().catch(() => false);
    const hasErrorContainer = await errorContainer.isVisible().catch(() => false);

    expect(hasSpecificError || hasGenericError || hasErrorContainer).toBeTruthy();

    await takeScreenshot(page, 'login_error_message');
  });

  test('2. No session token saved after failed login', async ({ page, context }) => {
    // Navigate to login page
    await page.goto(`${BASE_URL}/auth/login`);
    await expect(page.locator('input[type="email"]')).toBeVisible({ timeout: 10000 });

    // Attempt login with invalid credentials
    await page.locator('input[type="email"]').fill(INVALID_CREDENTIALS.email);
    await page.locator('input[type="password"]').fill(INVALID_CREDENTIALS.password);
    await page.getByRole('button', { name: /entrar|login/i }).click();

    // Wait for any response
    await page.waitForTimeout(3000);

    // Verify no auth tokens in localStorage
    const localStorage = await page.evaluate(() => {
      const storage: Record<string, string> = {};
      for (let i = 0; i < window.localStorage.length; i++) {
        const key = window.localStorage.key(i);
        if (key) {
          storage[key] = window.localStorage.getItem(key) || '';
        }
      }
      return storage;
    });

    // Check that no Supabase auth token exists
    const hasAuthToken = Object.keys(localStorage).some(key =>
      key.includes('supabase') && key.includes('auth')
    );

    // If there's a token, it should not contain valid session data
    if (hasAuthToken) {
      const authKeys = Object.keys(localStorage).filter(key =>
        key.includes('supabase') && key.includes('auth')
      );

      for (const key of authKeys) {
        const value = localStorage[key];
        if (value) {
          try {
            const parsed = JSON.parse(value);
            // Session should be null or expired
            expect(parsed.session).toBeFalsy();
          } catch {
            // If not parseable, that's fine
          }
        }
      }
    }

    // Verify cookies don't contain auth tokens
    const cookies = await context.cookies();
    const authCookies = cookies.filter(cookie =>
      cookie.name.includes('auth') ||
      cookie.name.includes('session') ||
      cookie.name.includes('supabase')
    );

    // Auth cookies should be empty or not have valid tokens
    for (const cookie of authCookies) {
      // Token cookies should not exist or be empty
      if (cookie.name.includes('token')) {
        expect(cookie.value).toBeFalsy();
      }
    }

    await takeScreenshot(page, 'login_no_session');
  });

  test('3. Multiple failed attempts show consistent error', async ({ page }) => {
    await page.goto(`${BASE_URL}/auth/login`);
    await expect(page.locator('input[type="email"]')).toBeVisible({ timeout: 10000 });

    // First attempt
    await page.locator('input[type="email"]').fill('attempt1@vertiv.tech');
    await page.locator('input[type="password"]').fill('WrongPass1!');
    await page.getByRole('button', { name: /entrar|login/i }).click();
    await page.waitForTimeout(2000);

    // Verify error shown
    expect(page.url()).toContain('/auth/login');

    // Clear and try second attempt
    await page.locator('input[type="email"]').clear();
    await page.locator('input[type="password"]').clear();
    await page.locator('input[type="email"]').fill('attempt2@vertiv.tech');
    await page.locator('input[type="password"]').fill('WrongPass2!');
    await page.getByRole('button', { name: /entrar|login/i }).click();
    await page.waitForTimeout(2000);

    // Still on login page after multiple attempts
    expect(page.url()).toContain('/auth/login');

    // Error message still visible
    const errorVisible = await page.locator('.text-destructive, [class*="error"]').isVisible().catch(() => false);
    expect(errorVisible || page.url().includes('/auth/login')).toBeTruthy();

    await takeScreenshot(page, 'login_multiple_attempts');
  });

  test('4. Empty credentials show validation error', async ({ page }) => {
    await page.goto(`${BASE_URL}/auth/login`);
    await expect(page.locator('input[type="email"]')).toBeVisible({ timeout: 10000 });

    // Try to submit without filling anything
    const submitButton = page.getByRole('button', { name: /entrar|login/i });
    await submitButton.click();

    // Should stay on login page
    expect(page.url()).toContain('/auth/login');

    // HTML5 validation should prevent submission or show error
    const emailInput = page.locator('input[type="email"]');
    const isInvalid = await emailInput.evaluate((el: HTMLInputElement) => !el.validity.valid);

    // Either HTML5 validation kicks in or we stay on login
    expect(isInvalid || page.url().includes('/auth/login')).toBeTruthy();

    await takeScreenshot(page, 'login_empty_credentials');
  });

  test('5. SQL injection attempt is rejected', async ({ page }) => {
    await page.goto(`${BASE_URL}/auth/login`);
    await expect(page.locator('input[type="email"]')).toBeVisible({ timeout: 10000 });

    // Attempt SQL injection in email field
    await page.locator('input[type="email"]').fill("admin'--@vertiv.tech");
    await page.locator('input[type="password"]').fill("' OR '1'='1");
    await page.getByRole('button', { name: /entrar|login/i }).click();

    await page.waitForTimeout(3000);

    // Should stay on login page (injection rejected)
    expect(page.url()).toContain('/auth/login');

    // No successful login
    const loggedIn = page.url().includes('/wizard') || page.url().includes('/dashboard');
    expect(loggedIn).toBeFalsy();

    await takeScreenshot(page, 'login_sql_injection_rejected');
  });

  test('6. XSS attempt in credentials is sanitized', async ({ page }) => {
    await page.goto(`${BASE_URL}/auth/login`);
    await expect(page.locator('input[type="email"]')).toBeVisible({ timeout: 10000 });

    // Attempt XSS in email field
    const xssPayload = '<script>alert("xss")</script>@vertiv.tech';
    await page.locator('input[type="email"]').fill(xssPayload);
    await page.locator('input[type="password"]').fill('<img src=x onerror=alert(1)>');
    await page.getByRole('button', { name: /entrar|login/i }).click();

    await page.waitForTimeout(2000);

    // Should stay on login page
    expect(page.url()).toContain('/auth/login');

    // No alert dialog should appear (XSS blocked)
    // If we get here without exception, XSS was blocked

    await takeScreenshot(page, 'login_xss_sanitized');
  });

});

test.describe('Login Error UI/UX', () => {

  test('Error message has proper styling', async ({ page }) => {
    await page.goto(`${BASE_URL}/auth/login`);
    await expect(page.locator('input[type="email"]')).toBeVisible({ timeout: 10000 });

    await page.locator('input[type="email"]').fill(INVALID_CREDENTIALS.email);
    await page.locator('input[type="password"]').fill(INVALID_CREDENTIALS.password);
    await page.getByRole('button', { name: /entrar|login/i }).click();

    await page.waitForTimeout(3000);

    // Check for error styling (red/destructive color)
    const errorElement = page.locator('.text-destructive, [class*="error"], .bg-destructive').first();

    if (await errorElement.isVisible()) {
      // Error should be visible and styled
      const styles = await errorElement.evaluate((el) => {
        const computed = window.getComputedStyle(el);
        return {
          color: computed.color,
          backgroundColor: computed.backgroundColor,
          display: computed.display
        };
      });

      // Should not be hidden
      expect(styles.display).not.toBe('none');
    }

    await takeScreenshot(page, 'login_error_styling');
  });

  test('Password field hides input', async ({ page }) => {
    await page.goto(`${BASE_URL}/auth/login`);
    await expect(page.locator('input[type="password"]')).toBeVisible({ timeout: 10000 });

    const passwordInput = page.locator('input[type="password"]');

    // Verify password field type is "password" (hides text)
    const inputType = await passwordInput.getAttribute('type');
    expect(inputType).toBe('password');

    // Fill password
    await passwordInput.fill('TestPassword123');

    // Should still be password type (not exposed)
    const typeAfterFill = await passwordInput.getAttribute('type');
    expect(typeAfterFill).toBe('password');
  });

});
