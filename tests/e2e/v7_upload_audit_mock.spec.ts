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
          id: ingestionId,
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
          id: ingestionId,
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

  test("requests manual audit from terminal audit view", async ({ page }) => {
    const ingestionId = "ing-manual-action-123";
    let body = { ...terminalAuditBody };
    let actionCalls = 0;

    await page.route(`**/api/v7/ingestion/${ingestionId}`, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          id: ingestionId,
          ingestion_id: ingestionId,
          ...body,
        }),
      });
    });

    await page.route(
      `**/api/v7/ingestion/${ingestionId}/manual-audit`,
      async (route) => {
        actionCalls += 1;
        body = { ...body, status: "PENDING_HUMAN_AUDIT" };
        await route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify({
            ingestion_id: ingestionId,
            action: "REQUEST_MANUAL_AUDIT",
            action_status: "applied",
            previous_status: "AUTONOMOUS_SENTENCED",
            current_status: "PENDING_HUMAN_AUDIT",
            audit_event_id: "evt-1",
          }),
        });
      },
    );

    await page.goto(`/dashboard/audit/${ingestionId}`);

    await expect(page.getByText("PROJETO VIÁVEL — TIR > WACC (GOLDEN RULE)")).toBeVisible();
    await page.getByRole("button", { name: "Auditoria Manual" }).click();

    await expect(page.getByText("Enviado para auditoria manual.", { exact: true })).toBeVisible();
    await expect(page.getByText("PENDING HUMAN AUDIT")).toBeVisible();
    expect(actionCalls).toBe(1);
  });

  test("confirms sentence from terminal audit view", async ({ page }) => {
    const ingestionId = "ing-confirm-action-123";
    let body = { ...terminalAuditBody };
    let actionCalls = 0;

    await page.route(`**/api/v7/ingestion/${ingestionId}`, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          id: ingestionId,
          ingestion_id: ingestionId,
          ...body,
        }),
      });
    });

    await page.route(
      `**/api/v7/ingestion/${ingestionId}/confirm-sentence`,
      async (route) => {
        actionCalls += 1;
        body = {
          ...body,
          sentence_confirmed_at: "2026-05-03T12:00:00Z",
          sentence_confirmed_by: "user-1",
        };
        await route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify({
            ingestion_id: ingestionId,
            action: "CONFIRM_SENTENCE",
            action_status: "applied",
            previous_status: "AUTONOMOUS_SENTENCED",
            current_status: "AUTONOMOUS_SENTENCED",
            sentence_confirmed_at: "2026-05-03T12:00:00Z",
            sentence_confirmed_by: "user-1",
            audit_event_id: "evt-2",
          }),
        });
      },
    );

    await page.goto(`/dashboard/audit/${ingestionId}`);

    await expect(page.getByText("PROJETO VIÁVEL — TIR > WACC (GOLDEN RULE)")).toBeVisible();
    await page.getByRole("button", { name: "Confirmar Sentença" }).click();

    await expect(page.getByText("Sentença confirmada com trilha de auditoria.", { exact: true })).toBeVisible();
    await expect(page.getByRole("button", { name: "Sentença Confirmada" })).toBeDisabled();
    expect(actionCalls).toBe(1);
  });

  test("shows manual-assisted review panel and enables confirmation after approval", async ({
    page,
  }) => {
    const ingestionId = "ing-manual-assisted-123";
    let body = {
      ...terminalAuditBody,
      status: "MANUAL_ASSISTED",
      manual_review_completed_at: null,
      manual_review_verdict: null,
    };
    let completeCalls = 0;

    await page.route(`**/api/v7/ingestion/${ingestionId}`, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          id: ingestionId,
          ingestion_id: ingestionId,
          ...body,
        }),
      });
    });

    await page.route(
      `**/api/v7/ingestion/${ingestionId}/complete-manual-review`,
      async (route) => {
        completeCalls += 1;
        body = {
          ...body,
          manual_review_completed_at: "2026-05-03T13:00:00Z",
          manual_review_completed_by: "user-1",
          manual_review_verdict: "APPROVE_WITH_NOTES",
          manual_review_notes: "Premissas revisadas.",
        };
        await route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify({
            ingestion_id: ingestionId,
            action: "COMPLETE_MANUAL_REVIEW",
            action_status: "applied",
            previous_status: "MANUAL_ASSISTED",
            current_status: "MANUAL_ASSISTED",
            manual_review_completed_at: "2026-05-03T13:00:00Z",
            manual_review_completed_by: "user-1",
            manual_review_verdict: "APPROVE_WITH_NOTES",
            audit_event_id: "evt-3",
          }),
        });
      },
    );

    await page.goto(`/dashboard/audit/${ingestionId}`);

    await expect(page.getByText("Revisão Humana")).toBeVisible();
    await expect(page.getByLabel("Notas da revisão")).toBeVisible();
    await expect(page.getByRole("button", { name: "Confirmar Sentença" })).toBeDisabled();

    await page.getByLabel("Notas da revisão").fill("Premissas revisadas.");
    await page.getByRole("button", { name: "Concluir Revisao" }).click();

    await expect(
      page.getByText("Revisão concluída. Confirmação de sentença liberada.", {
        exact: true,
      }),
    ).toBeVisible();
    await expect(page.getByRole("button", { name: "Confirmar Sentença" })).toBeEnabled();
    expect(completeCalls).toBe(1);
  });

  for (const status of ["KILLED", "FAILED"]) {
    test(`${status} disables audit action buttons`, async ({ page }) => {
      const ingestionId = `ing-${status.toLowerCase()}-123`;

      await mockAuditResponse(page, ingestionId, {
        ...terminalAuditBody,
        status,
        kill_reasons: status === "KILLED" ? ["Corte por regra de risco."] : [],
      });

      await page.goto(`/dashboard/audit/${ingestionId}`);

      await expect(page.getByText(status)).toBeVisible();
      await expect(page.getByRole("button", { name: "Auditoria Manual" })).toBeDisabled();
      await expect(page.getByRole("button", { name: "Confirmar Sentença" })).toBeDisabled();
      await expect(page.getByText("Ações bloqueadas", { exact: false })).toBeVisible();
    });
  }

  test("keeps sentence confirmation idempotent once confirmed", async ({ page }) => {
    const ingestionId = "ing-already-confirmed-123";
    let confirmCalls = 0;

    await mockAuditResponse(page, ingestionId, {
      ...terminalAuditBody,
      sentence_confirmed_at: "2026-05-03T12:00:00Z",
      sentence_confirmed_by: "user-1",
    });

    await page.route(
      `**/api/v7/ingestion/${ingestionId}/confirm-sentence`,
      async (route) => {
        confirmCalls += 1;
        await route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify({
            ingestion_id: ingestionId,
            action: "CONFIRM_SENTENCE",
            action_status: "idempotent_noop",
            previous_status: "AUTONOMOUS_SENTENCED",
            current_status: "AUTONOMOUS_SENTENCED",
            sentence_confirmed_at: "2026-05-03T12:00:00Z",
          }),
        });
      },
    );

    await page.goto(`/dashboard/audit/${ingestionId}`);

    await expect(page.getByRole("button", { name: "Sentença Confirmada" })).toBeDisabled();
    expect(confirmCalls).toBe(0);
  });
});
