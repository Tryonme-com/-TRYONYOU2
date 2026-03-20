# Palette's Journal

## 2025-05-15 - [Interactive Accessibility Patterns]
**Learning:** Custom interactive elements like product selection divs in this luxury dark theme were missing standard accessibility markers, making them unreachable via keyboard.
**Action:** Always ensure custom interactive divs have role="button", tabindex="0", and both click and keydown (Enter/Space) event handlers.

## 2025-05-15 - [Dynamic Content Announcements]
**Learning:** The AI consultation results were injected dynamically without notifying screen readers, causing a disconnect for assistive technology users.
**Action:** Assign 'aria-live="polite"' to containers where dynamic content or search results are injected.

## 2025-05-15 - [High-Contrast Focus Indicators]
**Learning:** The dark anthracite background requires explicit, high-contrast focus indicators for accessibility compliance.
**Action:** Implement a global ':focus-visible' style with 'outline: 2px solid var(--accent-gold); outline-offset: 4px;' to ensure keyboard navigation visibility.
