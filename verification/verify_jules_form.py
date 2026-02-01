from playwright.sync_api import Page, expect, sync_playwright

def verify_jules_form(page: Page):
    # Navigate to the app
    page.goto("http://localhost:5173/")

    # Scroll to consultation section
    page.locator("#consultation").scroll_into_view_if_needed()

    # Check for the correct labels
    expect(page.get_by_label("Body Shape")).to_be_visible()
    expect(page.get_by_label("Fit Preference")).to_be_visible()

    # Ensure "Height (cm)" and "Weight (kg)" are NOT visible
    expect(page.get_by_text("Height (cm)")).not_to_be_visible()
    expect(page.get_by_text("Weight (kg)")).not_to_be_visible()

    # Take screenshot of the form
    page.screenshot(path="verification/jules_form_verification.png")
    print("Screenshot taken.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_jules_form(page)
        finally:
            browser.close()
