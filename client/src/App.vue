<template>
  <div class="app-layout" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <span class="sidebar-brand-mark">CC</span>
        <h1>{{ t('nav.companyName') }}</h1>
        <span class="sidebar-subtitle">{{ t('nav.subtitle') }}</span>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/" :class="{ active: $route.path === '/' }" :title="t('nav.overview')">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
            <path d="M9 21V12h6v9" />
          </svg>
          <span>{{ t('nav.overview') }}</span>
        </router-link>
        <router-link to="/inventory" :class="{ active: $route.path === '/inventory' }" :title="t('nav.inventory')">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z" />
            <path d="M3.27 6.96L12 12.01 20.73 6.96" />
            <path d="M12 22.08V12" />
          </svg>
          <span>{{ t('nav.inventory') }}</span>
        </router-link>
        <router-link to="/orders" :class="{ active: $route.path === '/orders' }" :title="t('nav.orders')">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2" />
            <rect x="9" y="3" width="6" height="4" rx="2" />
            <path d="M9 12h6M9 16h4" />
          </svg>
          <span>{{ t('nav.orders') }}</span>
        </router-link>
        <router-link to="/spending" :class="{ active: $route.path === '/spending' }" :title="t('nav.finance')">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="5" width="20" height="14" rx="2" />
            <path d="M2 10h20M7 15h2M12 15h4" />
          </svg>
          <span>{{ t('nav.finance') }}</span>
        </router-link>
        <router-link to="/demand" :class="{ active: $route.path === '/demand' }" :title="t('nav.demandForecast')">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 7l-8.5 8.5-5-5L2 17" />
            <path d="M16 7h6v6" />
          </svg>
          <span>{{ t('nav.demandForecast') }}</span>
        </router-link>
        <router-link to="/backlog" :class="{ active: $route.path === '/backlog' }" :title="t('nav.backlog')">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 2 7 12 12 22 7 12 2"/>
            <polyline points="2 17 12 22 22 17"/>
            <polyline points="2 12 12 17 22 12"/>
          </svg>
          <span>{{ t('nav.backlog') }}</span>
        </router-link>
        <router-link to="/reports" :class="{ active: $route.path === '/reports' }" :title="t('nav.reports')">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
            <path d="M14 2v6h6" />
            <path d="M8 18v-4M12 18v-8M16 18v-2" />
          </svg>
          <span>{{ t('nav.reports') }}</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <LanguageSwitcher />
        <ProfileMenu @show-profile-details="showProfileDetails = true" @show-tasks="showTasks = true" />
        <button
          class="sidebar-toggle"
          @click="toggleSidebar"
          aria-label="Toggle sidebar"
          :title="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        >
          <svg class="toggle-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 17l-5-5 5-5"/>
            <path d="M18 17l-5-5 5-5"/>
          </svg>
        </button>
      </div>
    </aside>
    <div class="content-area">
      <FilterBar />
      <main class="main-content">
        <router-view />
      </main>
    </div>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    const apiTasks = ref([])

    // Sidebar collapse — persisted to localStorage so the user's choice survives reload
    const sidebarCollapsed = ref(localStorage.getItem('sidebar-collapsed') === 'true')

    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
      localStorage.setItem('sidebar-collapsed', String(sidebarCollapsed.value))
    }

    // Auto-collapse on narrow viewports; restore user preference when wide again
    let mql = null

    const handleMediaChange = (e) => {
      if (e.matches) {
        sidebarCollapsed.value = true
      } else {
        sidebarCollapsed.value = localStorage.getItem('sidebar-collapsed') === 'true'
      }
    }

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    onMounted(() => {
      loadTasks()

      mql = window.matchMedia('(max-width: 1024px)')
      mql.addEventListener('change', handleMediaChange)
      // Apply correct initial state if the screen is already narrow on mount
      if (mql.matches) {
        sidebarCollapsed.value = true
      }
    })

    onUnmounted(() => {
      if (mql) {
        mql.removeEventListener('change', handleMediaChange)
      }
    })

    return {
      t,
      sidebarCollapsed,
      toggleSidebar,
      showProfileDetails,
      showTasks,
      tasks,
      addTask,
      deleteTask,
      toggleTask
    }
  }
}
</script>

<style>
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

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-sans);
  background: var(--color-bg-app);
  color: var(--color-heading);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ─── App shell ─────────────────────────────────────────── */

.app-layout {
  min-height: 100vh;
}

.sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  width: var(--sidebar-width);
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  z-index: 100;
  transition: width 0.2s ease;
  overflow: hidden;
}

.sidebar-brand {
  padding: var(--space-6) var(--space-5);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
}

.sidebar-brand h1 {
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--color-heading-strong);
  letter-spacing: -0.025em;
}

.sidebar-subtitle {
  display: block;
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  font-weight: 400;
  margin-top: var(--space-1);
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  font-weight: 500;
  text-decoration: none;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.sidebar-nav a:hover {
  background: var(--color-bg-subtle);
  color: var(--color-heading-strong);
}

.sidebar-nav a.active {
  background: var(--color-primary-subtle);
  color: var(--color-primary-strong);
  font-weight: 600;
}

.sidebar-nav a svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.sidebar-footer {
  border-top: 1px solid var(--color-border);
  padding: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.content-area {
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: margin-left 0.2s ease;
}

.main-content {
  flex: 1;
  max-width: var(--content-max-width);
  width: 100%;
  margin: 0 auto;
  padding: var(--space-6) var(--space-8);
}

/* ─── Page structure ────────────────────────────────────── */

.page-header {
  margin-bottom: var(--space-6);
}

.page-header h2 {
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--color-heading-strong);
  margin-bottom: var(--space-2);
  letter-spacing: -0.025em;
}

.page-header p {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

/* ─── Stat grid ─────────────────────────────────────────── */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-5);
  margin-bottom: var(--space-6);
}

.stat-card {
  background: var(--color-surface);
  padding: var(--space-5);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: var(--color-border-strong);
  box-shadow: var(--shadow-md);
}

.stat-label {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: var(--space-3);
}

.stat-value {
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--color-heading-strong);
  letter-spacing: -0.025em;
}

.stat-card.warning .stat-value {
  color: var(--color-warning-strong);
}

.stat-card.success .stat-value {
  color: var(--color-success-strong);
}

.stat-card.danger .stat-value {
  color: var(--color-danger-strong);
}

.stat-card.info .stat-value {
  color: var(--color-primary);
}

/* ─── Cards ─────────────────────────────────────────────── */

.card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  border: 1px solid var(--color-border);
  margin-bottom: var(--space-5);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-border);
}

.card-title {
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-heading-strong);
  letter-spacing: -0.025em;
}

/* ─── Tables ─────────────────────────────────────────────── */

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--color-bg-app);
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

th {
  text-align: left;
  padding: var(--space-3) var(--space-4);
  font-weight: 600;
  color: var(--color-text-label);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: var(--space-3) var(--space-4);
  border-top: 1px solid var(--color-bg-subtle);
  color: var(--color-text);
  font-size: var(--text-sm);
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: var(--color-bg-app);
}

.clickable-row {
  cursor: pointer;
}

.clickable-row:hover {
  background: var(--color-primary-subtle);
}

/* ─── Badges ─────────────────────────────────────────────── */

.badge {
  display: inline-block;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge.success {
  background: var(--color-success-bg);
  color: var(--color-success-text);
}

.badge.warning {
  background: var(--color-warning-bg);
  color: var(--color-warning-text);
}

.badge.danger {
  background: var(--color-danger-bg);
  color: var(--color-danger-text);
}

.badge.info {
  background: var(--color-info-bg);
  color: var(--color-info-text);
}

.badge.increasing {
  background: var(--color-success-bg);
  color: var(--color-success-text);
}

.badge.decreasing {
  background: var(--color-danger-bg);
  color: var(--color-danger-text);
}

.badge.stable {
  background: var(--color-neutral-bg);
  color: var(--color-neutral-text);
}

.badge.high {
  background: var(--color-danger-bg);
  color: var(--color-danger-text);
}

.badge.medium {
  background: var(--color-warning-bg);
  color: var(--color-warning-text);
}

.badge.low {
  background: var(--color-info-bg);
  color: var(--color-info-text);
}

/* ─── Loading / error states ────────────────────────────── */

.loading {
  text-align: center;
  padding: var(--space-12);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

.error {
  background: var(--color-danger-bg);
  border: 1px solid var(--color-danger-bg);
  color: var(--color-danger-text);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  margin: var(--space-4) 0;
  font-size: var(--text-sm);
}

/* ─── Sidebar collapse ──────────────────────────────────── */

/* Narrow the sidebar and shift the content in one token change */
.app-layout.sidebar-collapsed {
  --sidebar-width: 64px;
}

/* ── Brand mark (compact monogram, shown only when collapsed) ── */

.sidebar-brand-mark {
  display: none;
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-heading-strong);
  text-align: center;
  width: 100%;
  white-space: nowrap;
}

.app-layout.sidebar-collapsed .sidebar-brand {
  padding: var(--space-4) var(--space-2);
  align-items: center;
  justify-content: center;
}

.app-layout.sidebar-collapsed .sidebar-brand h1,
.app-layout.sidebar-collapsed .sidebar-brand .sidebar-subtitle {
  display: none;
}

.app-layout.sidebar-collapsed .sidebar-brand .sidebar-brand-mark {
  display: block;
}

/* ── Nav links: icon-only, centered ── */

.app-layout.sidebar-collapsed .sidebar-nav a {
  justify-content: center;
  padding: var(--space-2);
}

.app-layout.sidebar-collapsed .sidebar-nav a span {
  display: none;
}

/* ── Footer widgets: hide text, center trigger buttons ── */

/* LanguageSwitcher — hide locale label and chevron */
.app-layout.sidebar-collapsed .sidebar-footer .language-label {
  display: none;
}

.app-layout.sidebar-collapsed .sidebar-footer .language-button .chevron {
  display: none;
}

/* Center the language-button trigger */
.app-layout.sidebar-collapsed .sidebar-footer .language-button {
  justify-content: center;
  padding: var(--space-2);
}

/* ProfileMenu — hide name and chevron */
.app-layout.sidebar-collapsed .sidebar-footer .profile-name {
  display: none;
}

.app-layout.sidebar-collapsed .sidebar-footer .profile-button .chevron {
  display: none;
}

/* Center the profile-button trigger */
.app-layout.sidebar-collapsed .sidebar-footer .profile-button {
  justify-content: center;
  padding: var(--space-2);
}

/* ── Toggle button ── */

.sidebar-toggle {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  background: transparent;
  border: none;
  border-top: 1px solid var(--color-border);
  border-radius: 0;
  cursor: pointer;
  color: var(--color-text-secondary);
  font-family: inherit;
  font-size: var(--text-sm);
  transition: background-color 0.15s ease, color 0.15s ease;
  margin-top: var(--space-1);
}

.sidebar-toggle:hover {
  background: var(--color-bg-subtle);
  color: var(--color-heading-strong);
}

.sidebar-toggle svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* When collapsed: center the icon and rotate to point right */
.app-layout.sidebar-collapsed .sidebar-toggle {
  justify-content: center;
  padding: var(--space-2);
}

.app-layout.sidebar-collapsed .sidebar-toggle .toggle-icon {
  transform: rotate(180deg);
}
</style>
