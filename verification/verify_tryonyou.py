from playwright.sync_api import Page, expect, sync_playwright

def verify_tryonyou(page: Page):
    # Go to localhost
    page.goto("http://localhost:8080")

    # Check for Jules Consultation Section
    expect(page.locator("#consultation")).to_be_visible()
    expect(page.get_by_role("heading", name="AI Stylist Consultation (Jules)")).to_be_visible()

    # Check for Form inputs
    expect(page.locator("#height")).to_be_visible()
    expect(page.locator("#weight")).to_be_visible()
    expect(page.locator("#event_type")).to_be_visible()

    # Check for Lafayette Collection
    expect(page.get_by_text("Lafayette x TryOnYou Exclusive")).to_be_visible()

    # Check for the specific new items
    expect(page.get_by_text("Cubist Art Jacket")).to_be_visible()
    expect(page.get_by_text("Peacock Couture Blazer")).to_be_visible()

    # Take screenshot of the consultation section
    page.locator("#consultation").screenshot(path="verification/consultation.png")

    # Take screenshot of the collection section
    page.locator(".exclusive-collection").screenshot(path="verification/collection.png")

    # Take full page screenshot
    page.screenshot(path="verification/full_page.png", full_page=True)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_tryonyou(page)
            print("Verification successful!")
        except Exception as e:
            print(f"Verification failed: {e}")
        finally:
            browser.close()
