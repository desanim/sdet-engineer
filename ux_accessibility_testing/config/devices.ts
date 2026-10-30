import { devices, type Project } from '@playwright/test';
const desktop = { viewport: { width: 1440, height: 900 } };
const uiMatch = /(?:functional|accessibility|responsive)[/\\].*\.spec\.ts$/;
export const deviceProjects: Project[] = [
  { name: 'desktop-chromium', use: { ...desktop, browserName: 'chromium' } },
  { name: 'desktop-firefox', use: { ...desktop, browserName: 'firefox' } },
  { name: 'desktop-webkit', use: { ...desktop, browserName: 'webkit' } },
  { name: 'tablet-ipad-portrait', use: { ...devices['iPad (gen 7)'], browserName: 'webkit' } },
  { name: 'tablet-ipad-landscape', use: { ...devices['iPad (gen 7) landscape'], browserName: 'webkit' } },
  { name: 'mobile-android-portrait', use: { ...devices['Pixel 7'], browserName: 'chromium' } },
  { name: 'mobile-iphone-portrait', use: { ...devices['iPhone 13'], browserName: 'webkit' } },
  { name: 'mobile-iphone-landscape', use: { ...devices['iPhone 13 landscape'], browserName: 'webkit' } }
].map(project => ({ ...project, testMatch: uiMatch, testIgnore: project.name === 'desktop-chromium' ? [] : ['**/breakpoints.spec.ts'] }));
const smoke = new Set(['desktop-chromium', 'tablet-ipad-portrait', 'mobile-android-portrait']);
export function projectsFor(mode: string, apiBaseURL: string): Project[] {
  return [
    { name: 'api', testMatch: /api[/\\].*\.spec\.ts$/, use: { baseURL: apiBaseURL } },
    ...deviceProjects.filter(project => mode === 'full' || smoke.has(project.name!))
  ];
}
