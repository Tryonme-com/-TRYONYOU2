## 2024-03-21 - [Accessibility for Custom Components]
**Learning:** Custom interactive elements (e.g., product selection divs) must include role="button", tabindex="0", descriptive aria-label, and support for 'Enter' and 'Space' keydown events for full keyboard operability.
**Action:** Always check for non-semantic buttons and apply these attributes and listeners to ensure accessibility.

## 2024-03-21 - [Dynamic Content Announcement]
**Learning:** Assign 'aria-live="polite"' to containers where dynamic content (like AI results) is injected to notify screen readers of updates.
**Action:** Implement aria-live on all async feedback containers.

## 2024-03-21 - [Focus Visibility]
**Learning:** Implement a global ':focus-visible' style with a clear outline to ensure keyboard navigation visibility while maintaining aesthetics for mouse users.
**Action:** Ensure a gold outline with sufficient offset is applied globally to :focus-visible.
