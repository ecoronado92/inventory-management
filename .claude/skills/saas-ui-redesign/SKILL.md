---
name: saas-ui-redesign
description: Procedure for redesigning the inventory app's Vue 3 UI into a modern SaaS layout with a fixed left sidebar and CSS design tokens. Use this skill when asked to redesign the UI, modernize the interface, add sidebar navigation, introduce design tokens, or do a visual/spacing consistency pass on the client.
---

# SaaS UI Redesign — Sidebar Layout & Design Tokens

This skill converts the app's current top-nav layout into a modern SaaS-style shell with a **fixed, always-expanded left sidebar (240px)** and formalizes the existing slate/blue palette into **CSS design tokens**, then applies a spacing/consistency pass across all views.

## 0. Purpose & scope

- Changes are limited to `client/` — never touch `server/`, mock data, or API contracts.
- No new npm dependencies, no CSS frameworks, no icon libraries. Icons are inline SVG.
- No emojis anywhere in the UI.
- EN and JA locales must both keep working (`useI18n`, `client/src/locales/en.js` / `ja.js`).
- All existing routes, filters, and data behavior stay functionally identical — this is a visual/structural redesign only.
- Responsive behavior (collapsing the sidebar below ~1024px, off-canvas drawer) is **out of scope** unless the user explicitly asks for it. The app currently has zero media queries; do not add them as part of this skill.

**Verify before applying:** read `client/src/App.vue` first and confirm the current state (top nav `header.top-nav` still present; the unscoped `<style>` block in App.vue is still the only global stylesheet; no `:root` tokens yet). If the codebase has already drifted from what this skill describes, adapt the steps to what actually exists rather than following them blindly.

## 1. Process rules (non-negotiable)

1. **Every creation or significant modification of a `.vue` file is delegated to the `vue-expert` subagent** (mandated by the root CLAUDE.md). The orchestrating session plans the phases, edits non-`.vue` files (`client/index.html`, `client/src/locales/*.js`), and verifies results.
2. Each vue-expert delegation prompt must include: the exact file(s) to change, the relevant section(s) of this skill (paste them in), and an instruction to read `.claude/skills/saas-ui-redesign/design-tokens.md` before writing any CSS.
3. Browser verification uses **Playwright MCP tools** against `http://localhost:3000` (frontend) and `http://localhost:8001` (API), per the root CLAUDE.md.
4. Icons: inline SVG only, heroicons-outline style (`fill="none" stroke="currentColor" stroke-width="2"`), sized via CSS — consistent with the SVGs already used in FilterBar, ProfileMenu, and LanguageSwitcher.
5. Work in the phase order of Section 6. Each phase must leave the app rendering and usable before the next begins.

## 2. Design tokens

The full `:root` token block and the hex→token mapping tables live in [design-tokens.md](design-tokens.md). Summary of the convention:

- Tokens are CSS custom properties declared once in the global (unscoped) `<style>` block of `client/src/App.vue`.
- Groups: surfaces/borders, text, primary, status (solid + badge tints), spacing (`--space-1` … `--space-12` on a 4/8px scale), radii, shadows, typography (`--font-sans`, `--text-xs` … `--text-3xl`), layout (`--sidebar-width: 240px`, `--content-max-width: 1600px`).
- New styles always use tokens; existing hard-coded values are migrated whenever a file is touched.
- The font stack already names `'Inter'` but the font is never loaded. Fix: add the Google Fonts `<link>` for Inter (weights 400, 500, 600, 700) to `client/index.html` (`<head>`). This is a plain HTML edit, not a dependency.

## 3. Target layout architecture (app shell)

`client/src/App.vue` is restructured from `header.top-nav` + `FilterBar` + `main` into a sidebar + content layout. The `header.top-nav`, `.nav-container`, and `.nav-tabs` markup and CSS are **removed entirely** — there is no longer a 70px header.

Template skeleton:

```html
<div class="app-layout">
  <aside class="sidebar">
    <div class="sidebar-brand">
      <h1>{{ t('nav.companyName') }}</h1>
      <span class="sidebar-subtitle">{{ t('nav.subtitle') }}</span>
    </div>
    <nav class="sidebar-nav">
      <!-- 6 router-links, each: inline SVG icon (20x20) + label -->
    </nav>
    <div class="sidebar-footer">
      <LanguageSwitcher />
      <ProfileMenu @show-profile-details="..." @show-tasks="..." />
    </div>
  </aside>
  <div class="content-area">
    <FilterBar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
  <!-- ProfileDetailsModal and TasksModal stay at the root, unchanged -->
</div>
```

Layout rules:

- `.sidebar`: `position: fixed; top: 0; bottom: 0; left: 0; width: var(--sidebar-width)`, background `var(--color-surface)`, `border-right: 1px solid var(--color-border)`, `display: flex; flex-direction: column`. The brand block sits at the top, `.sidebar-nav` takes `flex: 1` with `overflow-y: auto`, `.sidebar-footer` is pinned at the bottom with a `border-top`.
- `.content-area`: `margin-left: var(--sidebar-width)`, normal window scrolling. `.main-content` keeps `max-width: var(--content-max-width)`, padding from tokens (`var(--space-6) var(--space-8)`).
- Scroll model: the window scrolls the content; the sidebar is fixed and does not scroll with it.

Navigation links — same six routes as today (`/`, `/inventory`, `/orders`, `/spending`, `/demand`, `/reports`), labels from i18n (`nav.overview`, `nav.inventory`, `nav.orders`, `nav.finance`, `nav.demandForecast`, `nav.reports`):

```css
.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  font-weight: 500;
}
.sidebar-nav a:hover { background: var(--color-bg-subtle); color: var(--color-heading-strong); }
.sidebar-nav a.active { background: var(--color-primary-subtle); color: var(--color-primary-strong); font-weight: 600; }
```

- Active state: keep the existing `:class="{ active: $route.path === '...' }"` exact-match approach (or use `router-link-exact-active` for `/`) so Overview is highlighted only on `/`, never on other routes.
- Icon assignments (heroicons outline, drawn inline, 20×20, `stroke="currentColor"`): Overview = home, Inventory = cube/archive-box, Orders = clipboard-document-list, Finance = banknotes, Demand Forecast = arrow-trending-up, Reports = document-chart-bar.
- i18n fix: the Reports tab label is currently hard-coded English. Add `reports` to the `nav` section of `client/src/locales/en.js` (`'Reports'`) and `ja.js` (`'レポート'`), and use `t('nav.reports')` in the sidebar link.

FilterBar (`client/src/components/FilterBar.vue`):

- It currently uses `position: sticky; top: 70px`, coupled to the removed header height. Change to `top: 0`.
- Keep it full-width within the content column, background `var(--color-bg-app)` or `var(--color-surface)`, bottom border `var(--color-border)`.
- Align `.filters-container` max-width with `var(--content-max-width)` and migrate its paddings/gaps/font sizes to tokens.

## 4. Component relocation: LanguageSwitcher & ProfileMenu

Both components currently render white pill buttons designed for a top-right header position, with dropdowns positioned `top: calc(100% + 0.5rem); right: 0` (opening downward, right-aligned). Moving them into `.sidebar-footer` requires:

- **Dropdown direction**: open upward — `bottom: calc(100% + var(--space-2)); top: auto` — and left-aligned (`left: 0; right: auto`). Constrain width so the panel stays usable next to a 240px sidebar (e.g. `min-width: 200px`, max-width that doesn't overflow the viewport); it may overhang the sidebar's right edge over the content as long as it is fully visible.
- **Trigger styling**: restyle the pill buttons as full-width sidebar rows (flex, `padding: var(--space-2) var(--space-3)`, `border-radius: var(--radius-md)`, transparent background, hover `var(--color-bg-subtle)`) so they read as part of the sidebar rather than floating chips. Keep the avatar circle and user name in ProfileMenu; keep the globe + language label in LanguageSwitcher.
- **Stacking**: the sidebar is `position: fixed`; ensure the dropdown panels have a z-index above the FilterBar (currently z-index 90) and page content, and use `var(--shadow-lg)`.
- Emitted events (`show-profile-details`, `show-tasks`) and the modals they open are unchanged.

## 5. Spacing & consistency pass (per-view checklist)

Views must rely on the global classes defined in App.vue's global style block — `.page-header`, `.stats-grid`, `.stat-card` (+ `.warning/.success/.danger/.info`), `.card`, `.card-header`, `.card-title`, `.table-container`, table/`thead`/`th`/`td`, `.badge` (+ variants), `.loading`, `.error` — and must **not** shadow them with scoped re-definitions.

Known shadowing/duplication to remove (verify each before deleting):

- `client/src/views/Dashboard.vue`: scoped `.page-header` re-definition (differs from the global); dead off-palette purple-gradient task-button styles (`#667eea` → `#764ba2`) — delete; normalize `.kpi-grid`, `.kpi-card`, `.section-title`, `.charts-grid` paddings/gaps to tokens.
- `client/src/views/Inventory.vue`: scoped re-definitions of `.page-header`, `.card-header`, `.card-title`, `.loading`, `.error` — delete and rely on globals.
- `.clickable-row` is duplicated in Dashboard.vue and Inventory.vue — promote a single definition into the App.vue global block and delete the scoped copies.
- Replace inline `style="cursor: pointer;"` and inline color ternaries with classes where straightforward; don't refactor chart internals beyond tokenizing their colors.

Normalization targets (apply via tokens):

| Element | Target |
|---|---|
| `.page-header` bottom margin | `var(--space-6)` |
| `.card` / `.chart-card` padding | `var(--space-6)` |
| Grid gaps (`.stats-grid`, `.kpi-grid`, `.charts-grid`) | `var(--space-4)` or `var(--space-6)` |
| Table cell padding | `var(--space-3) var(--space-4)` |
| `.stat-card` / `.kpi-card` padding | `var(--space-5)` |
| Radii / shadows / font sizes | nearest token (see design-tokens.md) |

View order for the pass: `Dashboard.vue`, `Inventory.vue`, `Orders.vue`, `Spending.vue`, `Demand.vue`, `Reports.vue`. The unrouted `Backlog.vue` and the detail modal components (`InventoryDetailModal`, `ProductDetailModal`, `BacklogDetailModal`, `CostDetailModal`, `ProfileDetailsModal`, `TasksModal`) are optional follow-ups — not required for "done".

## 6. Execution order (phases)

1. **Tokens** — vue-expert adds the `:root` block from design-tokens.md to App.vue's global style block and switches `body`/global rules to tokens; orchestrator adds the Inter `<link>` to `client/index.html`.
2. **App shell** — vue-expert rewrites App.vue's template/styles into the sidebar + content layout (Section 3), including nav icons and active states, and removes all `.top-nav`/`.nav-container`/`.nav-tabs` CSS; orchestrator adds `nav.reports` to `en.js`/`ja.js`.
3. **FilterBar** — vue-expert updates the sticky offset, max-width, and token migration.
4. **LanguageSwitcher & ProfileMenu** — vue-expert applies the sidebar-footer styling and upward-opening dropdowns (Section 4).
5. **Per-view consistency passes** — one vue-expert task per view (or batches of 2–3 views), per Section 5.
6. **Verification** — Section 7.

Verify Phase 2 in the browser before continuing — it is the highest-risk change.

## 7. Verification & definition of done

Setup: both servers running (use the `/start` command — frontend on 3000, backend on 8001).

Using Playwright MCP, for **each** route — `/`, `/inventory`, `/orders`, `/spending`, `/demand`, `/reports`:

- The sidebar is visible and fixed on the left; no remnant of the old top nav is rendered.
- Exactly one nav item is highlighted, and it matches the current route (Overview only on `/`).
- No horizontal overflow: `document.body.scrollWidth <= window.innerWidth`.
- The FilterBar sticks to the top of the content column when scrolling, and changing a filter still updates the page's data.
- No console errors.

Plus, once overall:

- LanguageSwitcher toggles EN ↔ JA and every nav label translates (including Reports); layout doesn't break with Japanese strings.
- ProfileMenu and LanguageSwitcher dropdowns open upward from the sidebar footer and are fully visible above other content.
- No hard-coded hex values remain in `App.vue`, `FilterBar.vue`, `LanguageSwitcher.vue`, or `ProfileMenu.vue` for values that have tokens; the scoped shadow styles listed in Section 5 are gone.
- Backend behavior untouched (`server/` has no diff); backend tests still pass if run (use the repo's `/test` command or `pytest tests/backend/`).

**Done** = all of the above hold on every route in both locales.
