"use client";

import jsPDF from "jspdf";
import html2canvas from "html2canvas";

export interface ReportMetadata {
  title: string;
  subtitle?: string;
  projectName: string;
  generatedAt: Date;
  version: string;
}

export interface KPIData {
  label: string;
  value: string;
  change?: string;
  trend?: "up" | "down" | "neutral";
}

export interface ReportConfig {
  metadata: ReportMetadata;
  kpis: KPIData[];
  chartElementIds: string[];
  includeDisclaimer?: boolean;
}

// VERTIV Brand Colors
const COLORS = {
  primary: "#6366f1", // Indigo
  secondary: "#22c55e", // Green
  danger: "#ef4444", // Red
  dark: "#0f172a",
  muted: "#64748b",
  white: "#ffffff",
};

/**
 * VERTIV Global Report Generator
 * Enterprise-grade PDF generation with branding and professional layout
 */
export class ReportGenerator {
  private pdf: jsPDF;
  private pageWidth: number;
  private pageHeight: number;
  private margin: number = 20;
  private currentY: number = 20;

  constructor() {
    this.pdf = new jsPDF({
      orientation: "portrait",
      unit: "mm",
      format: "a4",
    });
    this.pageWidth = this.pdf.internal.pageSize.getWidth();
    this.pageHeight = this.pdf.internal.pageSize.getHeight();
  }

  /**
   * Generate a complete report
   */
  async generateReport(config: ReportConfig): Promise<void> {
    // Page 1: Cover + KPIs
    this.addCoverPage(config.metadata);
    this.addKPISection(config.kpis);

    // Page 2+: Charts
    for (const elementId of config.chartElementIds) {
      await this.addChartFromElement(elementId);
    }

    // Final Page: Disclaimer
    if (config.includeDisclaimer !== false) {
      this.addDisclaimerPage();
    }

    // Add page numbers
    this.addPageNumbers();

    // Download
    const fileName = `VERTIV_Report_${config.metadata.projectName.replace(/\s+/g, "_")}_${this.formatDate(config.metadata.generatedAt)}.pdf`;
    this.pdf.save(fileName);
  }

  /**
   * Cover Page with VERTIV branding
   */
  private addCoverPage(metadata: ReportMetadata): void {
    // Header gradient bar
    this.pdf.setFillColor(15, 23, 42); // Dark slate
    this.pdf.rect(0, 0, this.pageWidth, 60, "F");

    // Logo text (VERTIV.global)
    this.pdf.setTextColor(255, 255, 255);
    this.pdf.setFontSize(28);
    this.pdf.setFont("helvetica", "bold");
    this.pdf.text("VERTIV", this.margin, 25);
    this.pdf.setTextColor(99, 102, 241); // Primary indigo
    this.pdf.text(".global", this.margin + 42, 25);

    // Version badge
    this.pdf.setFontSize(10);
    this.pdf.setTextColor(100, 116, 139);
    this.pdf.text(`v${metadata.version}`, this.margin, 35);

    // Timestamp
    this.pdf.setFontSize(9);
    this.pdf.text(
      `Generated: ${this.formatDateTime(metadata.generatedAt)}`,
      this.pageWidth - this.margin - 50,
      35
    );

    // Main Title
    this.currentY = 90;
    this.pdf.setTextColor(15, 23, 42);
    this.pdf.setFontSize(32);
    this.pdf.setFont("helvetica", "bold");
    this.pdf.text(metadata.title, this.margin, this.currentY);

    // Subtitle
    if (metadata.subtitle) {
      this.currentY += 15;
      this.pdf.setFontSize(14);
      this.pdf.setTextColor(100, 116, 139);
      this.pdf.setFont("helvetica", "normal");
      this.pdf.text(metadata.subtitle, this.margin, this.currentY);
    }

    // Project Name Box
    this.currentY += 25;
    this.pdf.setFillColor(248, 250, 252);
    this.pdf.roundedRect(
      this.margin,
      this.currentY,
      this.pageWidth - 2 * this.margin,
      20,
      3,
      3,
      "F"
    );
    this.pdf.setFontSize(12);
    this.pdf.setTextColor(15, 23, 42);
    this.pdf.setFont("helvetica", "bold");
    this.pdf.text("PROJECT:", this.margin + 5, this.currentY + 13);
    this.pdf.setFont("helvetica", "normal");
    this.pdf.text(metadata.projectName, this.margin + 35, this.currentY + 13);

    this.currentY += 35;
  }

  /**
   * KPI Summary Section
   */
  private addKPISection(kpis: KPIData[]): void {
    // Section Title
    this.pdf.setFontSize(16);
    this.pdf.setTextColor(15, 23, 42);
    this.pdf.setFont("helvetica", "bold");
    this.pdf.text("Executive Summary", this.margin, this.currentY);
    this.currentY += 10;

    // Divider line
    this.pdf.setDrawColor(226, 232, 240);
    this.pdf.line(this.margin, this.currentY, this.pageWidth - this.margin, this.currentY);
    this.currentY += 10;

    // KPI Cards Grid (2x2)
    const cardWidth = (this.pageWidth - 2 * this.margin - 10) / 2;
    const cardHeight = 30;
    let col = 0;
    let row = 0;

    kpis.forEach((kpi, index) => {
      const x = this.margin + col * (cardWidth + 10);
      const y = this.currentY + row * (cardHeight + 8);

      // Card background
      this.pdf.setFillColor(248, 250, 252);
      this.pdf.roundedRect(x, y, cardWidth, cardHeight, 2, 2, "F");

      // KPI Label
      this.pdf.setFontSize(9);
      this.pdf.setTextColor(100, 116, 139);
      this.pdf.setFont("helvetica", "normal");
      this.pdf.text(kpi.label, x + 5, y + 10);

      // KPI Value
      this.pdf.setFontSize(16);
      this.pdf.setFont("helvetica", "bold");

      // Color based on trend
      if (kpi.trend === "up") {
        this.pdf.setTextColor(34, 197, 94); // Green
      } else if (kpi.trend === "down") {
        this.pdf.setTextColor(239, 68, 68); // Red
      } else {
        this.pdf.setTextColor(15, 23, 42); // Dark
      }
      this.pdf.text(kpi.value, x + 5, y + 22);

      // Change indicator
      if (kpi.change) {
        this.pdf.setFontSize(8);
        this.pdf.text(kpi.change, x + cardWidth - 25, y + 22);
      }

      col++;
      if (col >= 2) {
        col = 0;
        row++;
      }
    });

    this.currentY += (Math.ceil(kpis.length / 2)) * (cardHeight + 8) + 15;
  }

  /**
   * Capture and add chart from DOM element
   */
  private async addChartFromElement(elementId: string): Promise<void> {
    const element = document.getElementById(elementId);
    if (!element) {
      console.warn(`Element #${elementId} not found for PDF export`);
      return;
    }

    try {
      // Check if we need a new page
      if (this.currentY > this.pageHeight - 100) {
        this.pdf.addPage();
        this.currentY = this.margin;
      }

      // Capture element as canvas
      const canvas = await html2canvas(element, {
        scale: 2,
        backgroundColor: "#ffffff",
        logging: false,
        useCORS: true,
      });

      // Calculate dimensions to fit page width
      const imgWidth = this.pageWidth - 2 * this.margin;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      // Check if image fits on current page
      if (this.currentY + imgHeight > this.pageHeight - this.margin) {
        this.pdf.addPage();
        this.currentY = this.margin;
      }

      // Add image to PDF
      const imgData = canvas.toDataURL("image/png");
      this.pdf.addImage(
        imgData,
        "PNG",
        this.margin,
        this.currentY,
        imgWidth,
        imgHeight
      );

      this.currentY += imgHeight + 15;
    } catch (error) {
      console.error(`Failed to capture element #${elementId}:`, error);
    }
  }

  /**
   * Legal Disclaimer Page
   */
  private addDisclaimerPage(): void {
    this.pdf.addPage();
    this.currentY = this.margin;

    // Header
    this.pdf.setFontSize(14);
    this.pdf.setTextColor(15, 23, 42);
    this.pdf.setFont("helvetica", "bold");
    this.pdf.text("Important Disclaimers", this.margin, this.currentY);
    this.currentY += 10;

    // Divider
    this.pdf.setDrawColor(226, 232, 240);
    this.pdf.line(this.margin, this.currentY, this.pageWidth - this.margin, this.currentY);
    this.currentY += 10;

    // Disclaimer text
    this.pdf.setFontSize(9);
    this.pdf.setTextColor(100, 116, 139);
    this.pdf.setFont("helvetica", "normal");

    const disclaimers = [
      "FINANCIAL PROJECTIONS: All financial projections, including NPV, IRR, and cash flow estimates, are based on assumptions and historical data. Actual results may vary significantly from projections.",
      "",
      "REAL OPTIONS VALUATION: Real options analysis uses Black-Scholes-Merton methodology and Monte Carlo simulations. Volatility estimates are derived from market data and may not reflect future market conditions.",
      "",
      "MARKET CONDITIONS: This analysis assumes current market conditions. Economic cycles, regulatory changes, and macroeconomic factors may materially impact project viability.",
      "",
      "NOT INVESTMENT ADVICE: This report is for informational purposes only and does not constitute investment advice. Always consult qualified professionals before making investment decisions.",
      "",
      "CONFIDENTIALITY: This document contains proprietary analysis and projections. Distribution to unauthorized parties is strictly prohibited.",
      "",
      "DATA SOURCES: Market data, demographic information, and economic indicators are sourced from public databases and third-party providers. VERTIV does not guarantee the accuracy of third-party data.",
    ];

    disclaimers.forEach((text) => {
      if (text === "") {
        this.currentY += 5;
      } else {
        const lines = this.pdf.splitTextToSize(
          text,
          this.pageWidth - 2 * this.margin
        );
        this.pdf.text(lines, this.margin, this.currentY);
        this.currentY += lines.length * 4 + 3;
      }
    });

    // Footer
    this.currentY = this.pageHeight - 30;
    this.pdf.setFontSize(8);
    this.pdf.setTextColor(148, 163, 184);
    this.pdf.text(
      "VERTIV Global Real Estate Intelligence Platform",
      this.pageWidth / 2,
      this.currentY,
      { align: "center" }
    );
    this.currentY += 5;
    this.pdf.text(
      "Powered by Polars LazyFrames & Black-Scholes-Merton Engine",
      this.pageWidth / 2,
      this.currentY,
      { align: "center" }
    );
  }

  /**
   * Add page numbers to all pages
   */
  private addPageNumbers(): void {
    const totalPages = this.pdf.getNumberOfPages();

    for (let i = 1; i <= totalPages; i++) {
      this.pdf.setPage(i);
      this.pdf.setFontSize(8);
      this.pdf.setTextColor(148, 163, 184);
      this.pdf.text(
        `Page ${i} of ${totalPages}`,
        this.pageWidth / 2,
        this.pageHeight - 10,
        { align: "center" }
      );
    }
  }

  /**
   * Format date as YYYY-MM-DD
   */
  private formatDate(date: Date): string {
    return date.toISOString().split("T")[0];
  }

  /**
   * Format date and time
   */
  private formatDateTime(date: Date): string {
    return date.toLocaleString("pt-BR", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  }
}

/**
 * Quick export function for simple use cases
 */
export async function exportDashboardToPDF(
  projectName: string,
  kpis: KPIData[],
  chartIds: string[]
): Promise<void> {
  const generator = new ReportGenerator();

  await generator.generateReport({
    metadata: {
      title: "Real Options Analysis Report",
      subtitle: "Advanced Financial Modeling & Strategic Valuation",
      projectName,
      generatedAt: new Date(),
      version: "6.0.0",
    },
    kpis,
    chartElementIds: chartIds,
    includeDisclaimer: true,
  });
}
