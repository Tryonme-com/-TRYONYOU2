## 2025-05-15 - [Visibility of Interactive States]
**Learning:** In luxury-themed dark UIs, standard browser focus rings are often invisible or clash with the aesthetic. Explicit `:focus-visible` styles using theme-consistent colors (like gold) are essential for both accessibility and brand cohesion.
**Action:** Always check for focus visibility in dark mode and implement a high-contrast `:focus-visible` state using `outline-offset` to prevent clipping.

## 2025-05-15 - [Loading Feedback for Async AI Actions]
**Learning:** Users perceive "AI" actions as high-effort; providing a visible loading spinner even for fast local/mocked responses reinforces that "work" is being done and prevents double-submission.
**Action:** Ensure all async form submissions have a defined loading state in CSS, even if the JS already toggles a class.
