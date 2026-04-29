import { test, expect } from "@playwright/test";

test.describe("V7 Upload -> Audit (mocked)", () => {
  test("uploads a zip and navigates to terminal audit view", async ({ page }) => {
    const ingestionId = "ing-mock-123";

    await page.route("**/api/v7/ingest", async (route) => {
      await route.fulfill({
        status: 202,
        contentType: "application/json",
        body: JSON.stringify({ ingestion_id: ingestionId }),
      });
    });

    await page.route(`**/api/v7/ingestion/${ingestionId}`, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          ingestion_id: ingestionId,
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
        }),
      });
    });

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
});
