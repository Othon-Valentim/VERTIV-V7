import { test, expect, type Page } from "@playwright/test";

test.describe("V7 Upload -> Audit (mocked)", () => {
  const terminalAuditBody = {
    status: "AUTONOMOUS_SENTENCED",
    accuracy_score: 96.2,
    polars_calculations: {
      npv: 1250000,
      irr: 18.4,
      roe: 0.21,
      payback_months: 26,
      is_viable: true,
      wacc_used: 0.145,
      total_units: 42,
    },
    validation_metrics: {
      accuracy_score: 96.2,
    },
    llm_extracted_payload: {
      project_name: "Mock Project",
      city: "Sao Paulo",
    },
    kill_reasons: [],
  };

  async function mockAuditResponse(
    page: Page,
    ingestionId: string,
    body: Record<string, unknown>,
    status = 200,
  ) {
    await page.route(`**/api/v7/ingestion/${ingestionId}`, async (route) => {
      await route.fulfill({
        status,
        contentType: "application/json",
        body: JSON.stringify({
          ingestion_id: ingestionId,
          ...body,
        }),
      });
    });
  }

  test("uploads a zip and navigates to terminal audit view", async ({ page }) => {
    const ingestionId = "ing-mock-123";

    await page.route("**/api/v7/ingest", async (route) => {
      await route.fulfill({
        status: 202,
        contentType: "application/json",
        body: JSON.stringify({ ingestion_id: ingestionId }),
      });
    });

    await mockAuditResponse(page, ingestionId, terminalAuditBody);

    await page.goto("/dashboard/upload");

    await page.locator("#file-input").setInputFiles({
      name: "mock-data-room.zip",
      mimeType: "application/zip",
      buffer: Buffer.from("mock zip content"),
    });

    await page.getByRole("button", { name: "INICIAR INGESTÃO" }).click();

    await expect(page).toHaveURL(new RegExp(`/dashboard/audit/${ingestionId}$`));
    await expect(page.getByText("AUDIT /", { exact: false })).toBeVisible();
    await expect(page.getByText("SCORE:", { exact: false })).toBeVisible();
    await expect(
      page.getByText("PROJETO VIÁVEL — TIR > WACC (GOLDEN RULE)"),
    ).toBeVisible();
  });

  test("rejects non-zip upload", async ({ page }) => {
    const ingestCalls: number[] = [];

    await page.route("**/api/v7/ingest", async (route) => {
      ingestCalls.push(Date.now());
      await route.abort();
    });

    await page.goto("/dashboard/upload");

    await page.locator("#file-input").setInputFiles({
      name: "mock-data-room.txt",
      mimeType: "text/plain",
      buffer: Buffer.from("not a zip"),
    });

    await expect(page.getByText("Apenas arquivos .zip são aceitos.")).toBeVisible();
    await expect(page.getByRole("button", { name: "INICIAR INGESTÃO" })).toBeDisabled();

    await expect(page).toHaveURL(/\/dashboard\/upload$/);
    expect(ingestCalls).toHaveLength(0);
  });

  test.describe("audit handles auth and missing-access errors", () => {
    for (const { status, message } of [
      { status: 401, message: "Sessão expirada" },
      { status: 403, message: "Sessão expirada" },
      { status: 404, message: "Ingestão não encontrada" },
    ]) {
      test(`returns a friendly message for ${status}`, async ({ page }) => {
        const ingestionId = `ing-error-${status}`;

        await page.route(`**/api/v7/ingestion/${ingestionId}`, async (route) => {
          await route.fulfill({
            status,
            contentType: "application/json",
            body: JSON.stringify({ detail: `forced-${status}` }),
          });
        });

        await page.goto(`/dashboard/audit/${ingestionId}`);

        await expect(page.getByText(message, { exact: false })).toBeVisible();
      });
    }
  });

  test("stops polling on terminal status", async ({ page }) => {
    const ingestionId = "ing-terminal-123";
    let getCalls = 0;

    await page.route(`**/api/v7/ingestion/${ingestionId}`, async (route) => {
      getCalls += 1;
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          ingestion_id: ingestionId,
          ...terminalAuditBody,
        }),
      });
    });

    await page.goto(`/dashboard/audit/${ingestionId}`);

    await expect(page.getByText("PROJETO VIÁVEL — TIR > WACC (GOLDEN RULE)")).toBeVisible();

    await page.waitForTimeout(3300);

    const callsAfterFirstWindow = getCalls;
    expect(callsAfterFirstWindow).toBeGreaterThanOrEqual(1);

    await page.waitForTimeout(1200);

    expect(getCalls).toBe(callsAfterFirstWindow);
  });
});
