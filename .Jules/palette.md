## 2025-05-15 - [Form Accessibility & Visual Contrast]
**Learning:** Initial forms lacked semantic labels and proper input associations, hindering screen reader usability. High-luxury dark themes often sacrifice text contrast in footers, failing WCAG accessibility standards.
**Action:** Always wrap form inputs in groups with explicit `<label>` elements and matching `id` attributes. Use `aria-required` for mandatory fields. Ensure footer text opacity provides sufficient contrast against dark backgrounds (at least 0.7 for light-on-dark).
