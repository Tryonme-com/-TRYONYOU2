## 2025-05-15 - Accessible Custom Interactive Elements
**Learning:** For custom interactive elements (e.g., `div` as a product item), adding `role="button"` and `tabindex="0"` is only half the battle. To ensure full keyboard operability, explicit listeners for both 'Enter' and 'Space' must be implemented in JavaScript to mirror native button behavior.
**Action:** Always pair `tabindex="0"` on non-interactive elements with a `keydown` handler that triggers the primary action on 'Enter' and 'Space'.
