import type { Reporter, TestCase, TestResult, FullResult, FullConfig } from '@playwright/test/reporter';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

type Status = 'Pass' | 'Fail' | 'Needs review';
const manualReview = [
  { id: 'MAN-01', selector: 'main, nav, dialog', rule: 'Screen reader semantics', procedure: 'NVDA + Firefox/Chrome and VoiceOver + Safari: read headings/landmarks, labels, description, dialog name and modal boundary.' },
  { id: 'MAN-02', selector: '#amount, #amount-error, #status', rule: 'Announcements and recovery', procedure: 'With screen reader enabled, submit empty/invalid form, correct it and complete simulation. Verify error and success are announced once at the right time.' },
  { id: 'MAN-03', selector: ':focus-visible, #review-dialog', rule: 'Practical focus usability', procedure: 'Keyboard through all controls; inspect visible, unobscured focus, sensible reading order and modal entry/exit at zoom and with assistive technology.' },
  { id: 'MAN-04', selector: 'body', rule: 'Responsive usability and zoom', procedure: 'Check 200%/400% browser zoom, text spacing, landscape, touch targets, forced colors and real mobile devices. 320px overflow smoke does not establish conformance.' },
  { id: 'MAN-05', selector: 'body', rule: 'Content and full WCAG coverage', procedure: 'Review instructions, error clarity, contrast in all states and remaining applicable WCAG 2.2 A/AA criteria; record reviewer, browser/AT versions and evidence.' }
].map(item => ({ ...item, status: 'Needs review' as Status, impact: null, error: null }));

export default class EvidenceReporter implements Reporter {
  private rows: unknown[] = [];
  private output = '';
  onBegin(config: FullConfig) {
    this.output = join(config.rootDir, '../reports/playwright');
    mkdirSync(this.output, { recursive: true });
    // Overwrite stale success at start, including runs that are interrupted later.
    writeFileSync(join(this.output, 'evidence.json'), JSON.stringify({ runStatus: 'running', status: 'Needs review', automated: [], manualReview }, null, 2));
    writeFileSync(join(this.output, 'summary.md'), '# Accessibility evidence\n\nRun in progress. Needs review.\n');
  }
  onTestEnd(test: TestCase, result: TestResult) {
    const status: Status = result.status === 'passed' ? 'Pass' : ['failed', 'timedOut'].includes(result.status) ? 'Fail' : 'Needs review';
    const scans = result.attachments.filter(a => a.name === 'axe-evidence' && a.body).map(a => {
      const { state, negativeControl, results } = JSON.parse(a.body!.toString());
      const flatten = (rules: any[], status: Status) => rules.flatMap(rule => rule.nodes.map((node: any) => ({
        selector: node.target, rule: rule.id, impact: node.impact ?? rule.impact, status,
        error: node.failureSummary ?? null, html: node.html, help: rule.help, helpUrl: rule.helpUrl,
        checks: { any: node.any, all: node.all, none: node.none }
      })));
      return {
        state, negativeControl, url: results.url, timestamp: results.timestamp,
        engine: results.testEngine, environment: results.testEnvironment,
        status: results.violations.length ? 'Fail' : results.incomplete.length ? 'Needs review' : 'Pass',
        violations: flatten(results.violations, 'Fail'), incomplete: flatten(results.incomplete, 'Needs review'),
        passedRules: results.passes.map((r: any) => r.id), inapplicableRules: results.inapplicable.map((r: any) => r.id)
      };
    });
    const selectors: Record<string, string[]> = {
      'AXE-01': ['header', 'nav', 'main', 'h1', 'footer'],
      'KEY-01': ['#skip', '#nav-swap', '#nav-about', '#main', '#amount', '#review', '#cancel', '#confirm', '#status'],
      'FORM-01': ['label[for="amount"]', '#amount', '#amount-error', '#estimate', '#review-dialog'],
      'DIALOG-01': ['#review-dialog', '#cancel', '#confirm', '#review'],
      'RESP-01': ['html', '#amount', '#review-dialog', '#confirm'],
      'CONTROL-01': ['#negative-control']
    };
    this.rows.push({ selector: selectors[test.title.split(' ')[0]], rule: test.title.split(' ')[0], impact: null, test: test.title, project: test.parent.project()?.name, status, durationMs: result.duration,
      retry: result.retry, errors: result.errors.map(e => e.message), scans });
  }
  onEnd(result: FullResult) {
    const report = { schemaVersion: 1, generatedAt: new Date().toISOString(), runStatus: result.status,
      status: result.status === 'passed' ? 'Needs review' : 'Fail',
      scope: 'Local simulated swap only. Automated pass is not WCAG conformance. Negative controls are isolated detector checks.',
      automated: this.rows, manualReview };
    writeFileSync(join(this.output, 'evidence.json'), JSON.stringify(report, null, 2));
    const lines = ['# Accessibility E2E evidence', '', `Run: **${result.status}** · Overall: **${report.status}**`, '', report.scope, '', '## Automated checks', ''];
    // JSON blocks avoid unsafe/unescaped HTML and Markdown table delimiters from page evidence.
    for (const row of this.rows as any[]) {
      lines.push(`### ${row.project} / ${row.test} — ${row.status}`, '');
      for (const error of row.errors) lines.push('```text', error.replaceAll('```', "'''"), '```', '');
      for (const scan of row.scans) {
        lines.push(`State: ${scan.state} — ${scan.status}${scan.negativeControl ? ' (expected injected defect; isolated negative control)' : ''}`, '', `Passed rules: ${scan.passedRules.length}; violations: ${scan.violations.length}; incomplete nodes: ${scan.incomplete.length}.`, '');
        for (const finding of [...scan.violations, ...scan.incomplete]) lines.push('```json', JSON.stringify(finding, null, 2).replaceAll('```', "'''"), '```', '');
      }
    }
    lines.push('## Manual review — not executed', '');
    for (const item of manualReview) lines.push(`- **${item.id} / ${item.status}** — ${item.rule} (${item.selector}): ${item.procedure}`);
    writeFileSync(join(this.output, 'summary.md'), lines.join('\n') + '\n');
  }
}
