import type { Reporter, TestCase, TestResult, FullResult, FullConfig, TestError } from '@playwright/test/reporter';
import type { AxeResults, Result } from 'axe-core';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import type { Coverage } from '../test.js';

type Status = 'Pass' | 'Fail' | 'Needs review';
type ScanAttachment = { state: string; negativeControl: boolean; results: AxeResults };
function flatten(rules: Result[], status: Status) {
  return rules.flatMap(rule => rule.nodes.map(node => ({
    selector: node.target, rule: rule.id, impact: node.impact ?? rule.impact, status,
    error: node.failureSummary ?? null, html: node.html, help: rule.help, helpUrl: rule.helpUrl,
    checks: { any: node.any, all: node.all, none: node.none }
  })));
}
function scanEvidence({ state, negativeControl, results }: ScanAttachment) {
  return { state, negativeControl, url: results.url, timestamp: results.timestamp,
    engine: results.testEngine, environment: results.testEnvironment,
    status: (results.violations.length ? 'Fail' : results.incomplete.length ? 'Needs review' : 'Pass') as Status,
    violations: flatten(results.violations, 'Fail'), incomplete: flatten(results.incomplete, 'Needs review'),
    passedRules: results.passes.map(r => r.id), inapplicableRules: results.inapplicable.map(r => r.id)
  };
}
type Row = {
  id: string; test: string; project: string; suite: string; status: Status; durationMs: number;
  api: unknown[]; errors: string[]; coverage: Coverage[]; runtime: unknown[]; scans: ReturnType<typeof scanEvidence>[];
};
type Options = { reportDir: string; target: { app: string; baseURL: string; apiBaseURL: string; manualReview: string }; mode: string };
export default class EvidenceReporter implements Reporter {
  private rows: Row[] = [];
  private fatalErrors: string[] = [];
  private manualReview: unknown[] = [];
  private matrix: unknown[] = [];
  constructor(private options: Options) {}
  onBegin(config: FullConfig) {
    this.manualReview = JSON.parse(readFileSync(this.options.target.manualReview, 'utf8'));
    this.matrix = config.projects.map(p => ({ project: p.name, browser: p.name === 'api' ? null : p.use.browserName,
      viewport: p.use.viewport ?? null, isMobile: p.use.isMobile ?? false, hasTouch: p.use.hasTouch ?? false,
      deviceScaleFactor: p.use.deviceScaleFactor ?? 1, userAgent: p.use.userAgent ?? null, physicalDevice: false }));
    mkdirSync(this.options.reportDir, { recursive: true });
    this.save('evidence.json', JSON.stringify({ runStatus: 'running', status: 'Needs review', automated: [], manualReview: this.manualReview }, null, 2));
    this.save('summary.md', '# Web QA evidence\n\nRun in progress. Needs review.\n');
  }
  private save(name: string, content: string) { writeFileSync(join(this.options.reportDir, name), content); }
  onError(error: TestError) { this.fatalErrors.push(error.message ?? String(error)); }
  onTestEnd(test: TestCase, result: TestResult) {
    function attachments<T>(name: string): T[] {
      return result.attachments.filter(a => a.name === name).map(a => JSON.parse((a.body ?? readFileSync(a.path!)).toString()) as T);
    }
    const status: Status = result.status === 'passed' ? 'Pass' : ['failed', 'timedOut'].includes(result.status) ? 'Fail' : 'Needs review';
    this.rows.push({ id: test.id, test: test.title, project: test.parent.project()!.name,
      suite: relative(process.cwd(), test.location.file).replaceAll('\\', '/').split('/').at(-2)!,
      status, durationMs: result.duration, api: attachments<unknown>('api-evidence'), errors: result.errors.map(e => e.message ?? String(e)),
      coverage: attachments<Coverage>('coverage'), runtime: attachments<unknown>('runtime-environment'),
      scans: attachments<ScanAttachment>('axe-evidence').map(scanEvidence) });
  }
  onEnd(result: FullResult) {
    const baselineScans = this.rows.flatMap(r => r.scans).filter(s => !s.negativeControl);
    const controls = this.rows.flatMap(r => r.scans).filter(s => s.negativeControl);
    const summary = {
      tests: this.rows.length, passed: this.rows.filter(r => r.status === 'Pass').length,
      failed: this.rows.filter(r => r.status === 'Fail').length, needsReview: this.rows.filter(r => r.status === 'Needs review').length,
      baselineScans: baselineScans.length, baselineViolations: baselineScans.reduce((n, s) => n + s.violations.length, 0),
      incompleteNodes: baselineScans.reduce((n, s) => n + s.incomplete.length, 0),
      negativeControlScans: controls.length, expectedControlViolations: controls.reduce((n, s) => n + s.violations.length, 0)
    };
    const report = { schemaVersion: 2, generatedAt: new Date().toISOString(), runStatus: result.status,
      status: result.status === 'passed' && summary.failed === 0 ? 'Needs review' : 'Fail',
      target: this.options.target.app, mode: this.options.mode,
      urls: { ui: this.options.target.baseURL, api: this.options.target.apiBaseURL },
      scope: 'Selected UI/API/accessibility/responsive cases. Browser/device profiles are emulation, not physical-device results. Automated pass is not WCAG conformance.',
      summary, matrix: this.matrix, errors: this.fatalErrors, automated: this.rows, manualReview: this.manualReview };
    this.save('evidence.json', JSON.stringify(report, null, 2));
    const lines = ['# Web QA framework evidence', '', `Target: ${report.target} · Matrix: ${report.mode}`, '', `Run: **${result.status}** · Accessibility overall: **${report.status}**`, '', report.scope, '', '## Counts', '', '```json', JSON.stringify(summary, null, 2), '```', '', '## Automated checks', ''];
    for (const row of this.rows) {
      lines.push(`### ${row.project} / ${row.test} — ${row.status}`, '');
      for (const coverage of row.coverage) lines.push(`Coverage: ${coverage.rule} · ${coverage.selector.join(', ')} · ${coverage.detail}`, '');
      if (row.api.length) lines.push('API responses:', '', '```json', JSON.stringify(row.api, null, 2).replaceAll('```', "'''"), '```', '');
      for (const error of row.errors) lines.push('```text', error.replaceAll('```', "'''"), '```', '');
      for (const scan of row.scans) {
        lines.push(`State: ${scan.state} — ${scan.status}${scan.negativeControl ? ' (expected injected defect; isolated detector control)' : ''}`, '', `Passed rules: ${scan.passedRules.length}; violations: ${scan.violations.length}; incomplete nodes: ${scan.incomplete.length}.`, '');
        for (const finding of [...scan.violations, ...scan.incomplete]) lines.push('```json', JSON.stringify(finding, null, 2).replaceAll('```', "'''"), '```', '');
      }
    }
    lines.push('## Infrastructure errors', '', ...this.fatalErrors.map(e => e.replaceAll('```', "'''")), '', '## Manual review — not executed', '', '```json', JSON.stringify(this.manualReview, null, 2), '```', '');
    this.save('summary.md', lines.join('\n'));
  }
}
