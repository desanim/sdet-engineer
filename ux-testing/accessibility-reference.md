# Accessibility QA Reference Library

Curated study and working references for a QA engineer moving from general UX testing into digital accessibility testing. Links checked on 26 October 2026. Use official standards and laws as the source of truth; community resources and tools help explain or test them. For a Vietnamese explanation of what each source contains and how QA should use it, see [Accessibility QA Reference Library — Vietnamese guide](accessibility-reference-vi.md).

## How to use this library

1. Learn how disabled people use the web and where barriers arise.
2. Read WCAG 2.2 through the W3C Quick Reference. Keep the full standard open for exact wording.
3. Practice keyboard and screen-reader checks on a small, complete user journey.
4. Use automated tools to find some issues, then verify manually.
5. Record the exact page/state, affected user goal, method, evidence, and applicable success criterion.
6. Treat legal applicability as market- and service-specific. Confirm local implementation and scope with qualified counsel or compliance owners when the work requires a legal conclusion.

## 1. Standards and implementation guidance

| Resource | Why it is useful |
|---|---|
| [WCAG 2 Overview (W3C WAI)](https://www.w3.org/WAI/standards-guidelines/wcag/) | Explains WCAG 2 versions, supporting documents, and how it relates to other standards |
| [How to Meet WCAG 2: Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) | Daily lookup for success criteria, levels, techniques, and failures |
| [WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/) | Normative requirements; use exact criterion language when reporting |
| [ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/) | Interaction patterns and keyboard behavior for common widgets |
| [WAI-ARIA 1.2](https://www.w3.org/TR/wai-aria-1.2/) | Technical specification for roles, states, and properties |

Use standards precisely: ARIA communicates semantics and states; it does not by itself make an interaction accessible. Prefer native HTML when it provides the required behavior. APG is implementation guidance for patterns, while WCAG success criteria are the conformance requirements.

## 2. Learn user context and practical techniques

- [WAI Accessibility Fundamentals](https://www.w3.org/WAI/fundamentals/) — people, disabilities, assistive technology, and accessibility basics.
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility) — HTML and browser-focused technical explanations.
- [The A11Y Project](https://www.a11yproject.com/) — concise checklists and explanations; use WCAG for normative decisions.
- [Deque University](https://dequeuniversity.com/) — courses and reference material; some material may require an account or payment.
- [WebAIM](https://webaim.org/) — practical articles and tools, including the [Contrast Checker](https://webaim.org/resources/contrastchecker/).

Practice with real tasks: move through a flow by keyboard, inspect focus, listen to labels and state changes with a screen reader, zoom and reflow the page, and check errors and recovery. A simulated impairment exercise is not a substitute for feedback from disabled users.

## 3. Testing tools

| Tool | Good for | Limit |
|---|---|---|
| [axe DevTools / axe-core](https://www.deque.com/axe/) | Automated rule checks in browser or test suites | Does not judge every criterion, context, or interaction |
| [WAVE](https://wave.webaim.org/) | Visual overlay for some structural and contrast issues | Findings require human verification |
| [Lighthouse](https://developer.chrome.com/docs/lighthouse/accessibility/) | Quick browser audit and regression signal | A score is not a WCAG conformance result |
| [NVDA](https://www.nvaccess.org/) | Free Windows screen reader for manual testing | Results depend on browser, app semantics, and tester method |
| VoiceOver | Built-in on macOS and iOS; use with Safari for relevant journeys | Platform and browser behavior differ; test the actual support matrix |

There is no universal percentage that describes how many accessibility defects an automated scan catches. Coverage depends on the tool, rules, markup, and product. Pair automation with keyboard, screen-reader, zoom/reflow, and expert review.

## 4. Standards and law: what the names mean

| Framework | Practical interpretation |
|---|---|
| WCAG 2.2 | W3C accessibility guideline with Level A, AA, and AAA success criteria. Agree the target level and scope before an audit. |
| ISO/IEC 40500:2025 | WCAG 2.2's October 2023 version was approved as ISO/IEC 40500:2025. Do not assume that every later WCAG update is included in that ISO edition. |
| EN 301 549 | European ICT accessibility standard used in legal and procurement contexts. Check the applicable edition and requirements for the specific product/service. |
| European Accessibility Act (EAA) | Applies from 28 June 2025 to specified products and services, with scope and exceptions defined in the Directive and national implementation. It does not make every website subject to identical requirements. |
| U.S. Section 508 | Revised standards incorporate WCAG 2.0 Level A and AA for covered ICT. Check current agency requirements and whether the product is in scope. |
| China GB/T 37668-2019 | Current recommended national standard for internet content accessibility technical requirements and conformance testing; includes web/mobile web and app applicability. Read the official record and standard text. |

This table is an orientation, not legal advice or a complete jurisdictional comparison. Product type, provider, audience, exceptions, procurement rules, and national implementation can change obligations. Use the precise law/standard named by the project.

## 5. China-focused references

### Standards and policy

- [Official national standard record: GB/T 37668-2019](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=35ECC696805C1A67C93B74FB6D0D8EFB) — 《信息技术 互联网内容无障碍可访问性技术要求与测试方法》; listed as current, effective 1 March 2020.
- [MIIT & China Disabled Persons' Federation guidance, 工信部联管函〔2020〕146号](https://www.miit.gov.cn/jgsj/xgj/wjfb/art/2020/art_457a63f75df24c749ea2a8a44c713161.html) — policy direction on information accessibility.
- [MIIT special action plan for ageing-friendly and accessible internet applications](https://www.miit.gov.cn/jgsj/xgj/wjfb/art/2020/art_18a8b1029f724afc8b31264fcd0f4106.html) — historical one-year campaign; useful context, not a blanket statement of current legal duties.
- [W3C Chinese-language note on the national standard](https://www.w3.org/zh-hans/blog/2020/updated-chinese-accessibility-standard/) — background on GB/T 37668-2019.

### Organizations and practitioner material

- [信息无障碍研究会 / Accessibility Research Association](https://www.siaa.org.cn/) — Chinese-language research, events, and practice resources. Verify the date and scope of any material you cite.
- [联谛信息无障碍 / Link Accessibility](https://www.linkacce.com/) — practitioner service provider; useful as an industry example, not a normative authority.
- [Juejin](https://juejin.cn/) and [Zhihu](https://www.zhihu.com/) — search terms: 无障碍, 信息无障碍, 适老化, WCAG, ARIA, 屏幕阅读器. Treat community posts as implementation experiences and cross-check standards claims against primary sources.

## 6. Suggested study order

1. WAI Fundamentals → learn barriers and assistive-technology context.
2. WCAG 2 Overview → understand structure and conformance.
3. Quick Reference → study common Level A/AA criteria and link each to tests.
4. Semantic HTML, keyboard, and forms → practice on a complete journey.
5. APG → learn a widget only when it appears in the product; test the documented keyboard model.
6. axe/WAVE/Lighthouse → run scans, verify findings, record tool/version.
7. NVDA + a supported browser → perform manual task-based checks. Add VoiceOver when available and relevant.
8. Audit and report → scope the review, map findings to criteria, document untested areas.

The accompanying [16-week QA-first roadmap](a11y-16-week-roadmap.md) turns this into weekly practice. Use the [accessibility audit report template](accessibility-audit-template.md) for the portfolio deliverable.

## Sources checked

Official status and scope references: [W3C WCAG overview](https://www.w3.org/WAI/standards-guidelines/wcag/), [W3C announcement on ISO/IEC 40500:2025](https://www.w3.org/WAI/news/2025-10-21/wcag22-iso/), [EUR-Lex EAA summary](https://eur-lex.europa.eu/EN/legal-content/summary/accessibility-of-products-and-services.html), [Section508.gov conformance requirements](https://www.section508.gov/develop/applicability-conformance/), and the [SAMR national standard record](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=35ECC696805C1A67C93B74FB6D0D8EFB).