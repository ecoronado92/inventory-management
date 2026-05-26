# Design Tokens — SaaS UI Redesign

Canonical CSS custom properties for the redesigned UI. The `:root` block below is added **once**, at the top of the global (unscoped) `<style>` block in `client/src/App.vue`, before the `*` reset rule. Every other stylesheet (global or scoped) consumes these via `var(...)`.

## Token block (copy-paste ready)

```css
:root {
  /* Surfaces & borders */
  --color-bg-app: #f8fafc;          /* app background */
  --color-bg-subtle: #f1f5f9;       /* hover fills, table header bg, progress tracks */
  --color-surface: #ffffff;         /* cards, sidebar, dropdowns */
  --color-border: #e2e8f0;          /* default borders, dividers */
  --color-border-strong: #cbd5e1;   /* input borders, hovered card borders */

  /* Text */
  --color-heading-strong: #0f172a;  /* page titles, KPI values, primary emphasis */
  --color-heading: #1e293b;         /* body default (set on body) */
  --color-text: #334155;            /* table cells, standard copy */
  --color-text-label: #475569;      /* table headers, section titles */
  --color-text-secondary: #64748b;  /* subtitles, labels, secondary copy */
  --color-text-muted: #94a3b8;      /* placeholders, disabled, tertiary */

  /* Brand / primary */
  --color-primary: #2563eb;         /* active nav, links, primary buttons */
  --color-primary-strong: #1e40af;  /* active text on subtle bg, gradients */
  --color-primary-soft: #3b82f6;    /* focus rings, info accents, chart blue */
  --color-primary-subtle: #eff6ff;  /* active nav bg, selected row bg */

  /* Status — solid */
  --color-success: #10b981;
  --color-success-strong: #059669;
  --color-warning: #f59e0b;
  --color-warning-strong: #ea580c;
  --color-danger: #ef4444;
  --color-danger-strong: #dc2626;
  --color-info: #3b82f6;

  /* Status — badge tints (background / text pairs) */
  --color-success-bg: #d1fae5;
  --color-success-text: #065f46;
  --color-warning-bg: #fed7aa;
  --color-warning-text: #92400e;
  --color-danger-bg: #fecaca;
  --color-danger-text: #991b1b;
  --color-info-bg: #dbeafe;
  --color-info-text: #1e40af;
  --color-neutral-bg: #e0e7ff;      /* "stable" badge */
  --color-neutral-text: #3730a3;

  /* Spacing — 4px/8px scale */
  --space-1: 0.25rem;   /* 4px  */
  --space-2: 0.5rem;    /* 8px  */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */

  /* Radii */
  --radius-sm: 6px;     /* badges, inputs, nav links */
  --radius-md: 8px;     /* buttons, dropdown items, error banners */
  --radius-lg: 10px;    /* cards, dropdown panels, modals */
  --radius-full: 9999px;/* avatars, pills */

  /* Shadows (slate-tinted) */
  --shadow-sm: 0 1px 3px 0 rgba(15, 23, 42, 0.06);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.08);
  --shadow-lg: 0 10px 25px rgba(15, 23, 42, 0.12);

  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
               'Helvetica Neue', Arial, sans-serif;
  --text-xs: 0.75rem;     /* badges, table headers, filter labels */
  --text-sm: 0.875rem;    /* table cells, secondary copy, buttons */
  --text-base: 1rem;      /* nav links, section titles, card body */
  --text-lg: 1.125rem;    /* card titles */
  --text-xl: 1.375rem;    /* brand / logo */
  --text-2xl: 1.875rem;   /* page titles */
  --text-3xl: 2.25rem;    /* stat / KPI values */

  /* Layout */
  --sidebar-width: 240px;
  --content-max-width: 1600px;
}
```

## Hex → token mapping

When you encounter a hard-coded value in any file you are editing, replace it with the token. Values are listed by frequency of current use.

### Slate scale

| Hex | Token |
|---|---|
| `#f8fafc` | `--color-bg-app` |
| `#f1f5f9` | `--color-bg-subtle` |
| `#ffffff` / `white` | `--color-surface` |
| `#e2e8f0` | `--color-border` |
| `#cbd5e1` | `--color-border-strong` |
| `#94a3b8` | `--color-text-muted` |
| `#64748b` | `--color-text-secondary` |
| `#475569` | `--color-text-label` |
| `#334155` | `--color-text` |
| `#1e293b` | `--color-heading` |
| `#0f172a` | `--color-heading-strong` |

### Blue / primary

| Hex | Token |
|---|---|
| `#2563eb` | `--color-primary` |
| `#1e40af` | `--color-primary-strong` (also info badge text → `--color-info-text`) |
| `#3b82f6` | `--color-primary-soft` (or `--color-info` in status contexts) |
| `#eff6ff` | `--color-primary-subtle` |
| `#dbeafe` | `--color-info-bg` |

### Status colors

| Hex | Token |
|---|---|
| `#10b981` | `--color-success` |
| `#059669` / `#16a34a` | `--color-success-strong` |
| `#d1fae5` | `--color-success-bg` |
| `#065f46` / `#166534` | `--color-success-text` |
| `#f59e0b` | `--color-warning` |
| `#ea580c` / `#d97706` | `--color-warning-strong` |
| `#fed7aa` | `--color-warning-bg` |
| `#92400e` | `--color-warning-text` |
| `#ef4444` | `--color-danger` |
| `#dc2626` | `--color-danger-strong` |
| `#fecaca` | `--color-danger-bg` |
| `#991b1b` | `--color-danger-text` |
| `#e0e7ff` | `--color-neutral-bg` |
| `#3730a3` | `--color-neutral-text` |

### Special cases

| Hex | Action |
|---|---|
| `#667eea`, `#764ba2`, `#8b5cf6`, `#c4b5fd`, `#f5f3ff` | Off-palette purple/violet (dead task-button styles in `Dashboard.vue` and stray accents). Delete the dead rules; if a live usage remains, map to `--color-primary` / `--color-primary-subtle`. |
| `#fef2f2`, `#fee2e2`, `#fffbeb`, `#fef3c7`, `#f0fdf4`, `#dcfce7` | Pale alert/section backgrounds (error banner, soft highlights). Map to the nearest status `*-bg` token or keep only if a token would visibly change the design; do not introduce new tokens for one-offs. |
| `#fcd34d`, `#86efac`, `#a7f3d0`, `#93c5fd`, `#60a5fa`, `#bfdbfe` | One-off chart/sparkline tints. Leave as-is unless the file is being restyled anyway; then map to the nearest status/primary token. |

### Spacing, radii, typography

| Current value | Token |
|---|---|
| `0.25rem` | `--space-1` |
| `0.313rem`, `0.4rem`, `0.5rem` | `--space-2` |
| `0.625rem`, `0.75rem`, `0.875rem` | `--space-3` (or `--space-2` for tight paddings — keep visual density) |
| `1rem` | `--space-4` |
| `1.25rem` | `--space-5` |
| `1.5rem` | `--space-6` |
| `2rem` | `--space-8` |
| `3rem` | `--space-12` |
| `border-radius: 6px` | `--radius-sm` |
| `border-radius: 8px` | `--radius-md` |
| `border-radius: 10px` | `--radius-lg` |
| `50%` (avatars) | `--radius-full` |
| Font sizes `0.75 / 0.813 / 0.875 / 0.938 / 1 / 1.125 / 1.375 / 1.875 / 2–2.25rem` | Nearest of `--text-xs / --text-xs / --text-sm / --text-sm / --text-base / --text-lg / --text-xl / --text-2xl / --text-3xl` |
| `box-shadow` one-offs | Nearest of `--shadow-sm / --shadow-md / --shadow-lg` |

Off-scale values (`0.313rem`, `0.4rem`, `0.813rem`, `0.938rem`) are normalized to the nearest token — that is the point of the consistency pass; small visual shifts are expected and acceptable.

## Usage rules

1. **New styles always use tokens.** No new hard-coded hex values, px paddings, or ad-hoc shadows.
2. **Migrate on touch.** When a file is edited for any phase of the redesign, replace its hard-coded values with tokens per the tables above. Files not being touched do not need a dedicated migration pass.
3. **Don't grow the palette.** If a needed value has no token, choose the nearest existing token rather than adding a new one; only add a token when at least three call sites need the same new value.
4. **Component-local variables are allowed** for genuinely local concerns (e.g. a chart's segment colors), but they must be defined from global tokens, not new hex values.
