"""
VVIT Website Scraper — Playwright Edition
==========================================
VVIT (vvitu.ac.in) is a React Single Page Application (SPA).
Regular requests/BeautifulSoup only retrieves the empty HTML shell.
This scraper uses Playwright (headless Chromium) to fully render each page
and extract real content.

Setup (one-time):
    pip install playwright
    playwright install chromium

Run:
    python scraper.py

Output: data/vvit_data.json
"""

import json
import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

BASE_URL    = "https://vvitu.ac.in"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "data", "vvit_data.json")

TARGET_PAGES = {
    "about_administration": [
        "/", "/about-us", "/chancellor", "/pro_chancellor", "/vice-chancellor",
        "/secretary", "/jt-secretary", "/registrar", "/board_of_management",
        "/governing_body", "/accreditation-and-approvals", "/mandatory-disclosures"
    ],
    "admissions": [
        "/admissions", "/admissions/ug-programs",
        "/admissions/ug-programs/btech-cse",
        "/admissions/ug-programs/btech-cse-ai-ml",
        "/admissions/ug-programs/btech-cse-ai-ds",
        "/admissions/ug-programs/btech-cse-iot",
        "/admissions/ug-programs/btech-ece",
        "/admissions/ug-programs/btech-eee",
        "/admissions/ug-programs/btech-mec",
        "/admissions/ug-programs/btech-civil",
        "/admissions/ug-programs/btech-bba",
        "/admissions/pg-programs",
        "/admissions/pg-programs/mtech-cse",
        "/admissions/pg-programs/mtech-cse-ai-ds",
        "/admissions/pg-programs/mtech-cse-ai",
        "/admissions/pg-programs/mtech-eee",
        "/admissions/pg-programs/mtech-ece",
        "/admissions/pg-programs/mtech-mec",
        "/admissions/pg-programs/mtech-civil",
        "/admissions/pg-programs/mtech-mca",
        "/admissions/pg-programs/mtech-mba",
        "/admissions/phd-programs",
        "/admissions/phd-programs/phd-cse-ai",
        "/admissions/phd-programs/phd-ece",
        "/admissions/phd-programs/phd-eee",
        "/admissions/phd-programs/phd-mec",
        "/admissions/phd-programs/phd-civil"
    ],
    "placements_careers": [
        "/placement", "/statistics"
    ],
    "campus_facilities": [
        "/hostels", "/library", "/transport", "/canteen"
    ],
    "student_life": [
        "/student-clubs", "/student-council", "/NCC", "/NSS",
        "/IUCEE", "/IIC", "/IDEA-Labs", "/UIF",
        "/SGRC", "/FSGRC", "/contact-us"
    ]
}

NAV_NOISE = {
    "Light Mode", "Dark Mode", "Student Login", "Staff Login",
    "Examinations", "About VVITU", "Administration", "Admissions",
    "Academics", "Career Guidance", "Campus Life", "Contact Us",
    "Admission 2026 - Apply", "Notifications",
}

PAGE_WAIT_MS   = 2500
PAGE_TIMEOUT   = 20000

# ─────────────────────────────────────────────
# Text Cleaning
# ─────────────────────────────────────────────

def clean_text(raw: str) -> str:
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line in NAV_NOISE:
            continue
        if len(line) < 20:
            # Important exceptions for metrics like '29 LPA' or '600+'
            whitelist = ["LPA", "CTC", "₹", "600+", "90+", "Average", "Highest", "Lowest", "Placements", "Companies", "AY."]
            if not any(x in line for x in whitelist):
                continue
        if all(c in "•·–—-|/\\" for c in line):
            continue
        lines.append(line)
    return "\n".join(lines)

def scrape_dynamic_statistics(page, url):
    """
    Specialized scraper for the statistics page to handle JS dashboard cards
    and academic year tabs.
    """
    print("     ⚡ Running Interaction Scraper for Statistics...")
    try:
        page.goto(url, wait_until="networkidle", timeout=PAGE_TIMEOUT)
    except PlaywrightTimeout:
        pass
    
    # Wait for dashboard cards to be visible
    page.wait_for_timeout(3000) 
    
    all_text_segments = []
    
    # 1. Capture Dashboard Summary
    summary = page.inner_text("body").split("Placement Details")[0]
    all_text_segments.append(f"OVERALL SUMMARY - PLACEMENT STATISTICS DASHBOARD:\n{summary}")
    
    # 2. Iterate through Academic Year Tabs
    buttons = page.query_selector_all("button")
    year_buttons = [b for b in buttons if "AY." in b.inner_text()]
    
    for btn in year_buttons:
        year_label = btn.inner_text().strip()
        print(f"        → Clicking tab & injecting context: {year_label}")
        try:
            btn.click()
            page.wait_for_timeout(2000) # Wait for table to swap
            
            # Capture the table area
            body_text = page.inner_text("body")
            if "Placement Details" in body_text:
                table_content = body_text.split("Placement Details")[1]
            else:
                table_content = body_text
            
            # FORCE CONTEXT INJECTION: Prepend the year to EVERY line in this section
            # This ensures that any chunk taken from here will know its year.
            contextualized_lines = []
            for line in table_content.splitlines():
                clean_l = line.strip()
                if clean_l:
                    contextualized_lines.append(f"[{year_label}] {clean_l}")
            
            all_text_segments.append(f"\nDETAILED PLACEMENT DATA FOR {year_label}:\n" + "\n".join(contextualized_lines))
                
        except Exception as e:
            print(f"        ⚠ Failed to click/scrape {year_label}: {e}")
            
    return "\n\n".join(all_text_segments)

# ─────────────────────────────────────────────
# Main Scraper
# ─────────────────────────────────────────────

def scrape_all() -> list[dict]:
    documents = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()

        for category, paths in TARGET_PAGES.items():
            print(f"\n📂 Category: {category}")

            for path in paths:
                url = f"{BASE_URL}{path}"
                print(f"  → Scraping: {url}")

                try:
                    if "statistics" in path:
                        raw_text = scrape_dynamic_statistics(page, url)
                    else:
                        try:
                            page.goto(url, wait_until="networkidle", timeout=PAGE_TIMEOUT)
                        except PlaywrightTimeout:
                            print("     ⚠ Network idle timeout reached, attempting to scrape rendered DOM anyway...")
                        raw_text = page.inner_text("body")

                    text = clean_text(raw_text)

                    if len(text) < 100:
                        print(f"     ⚠ Too little content ({len(text)} chars), skipping")
                        continue

                    title = page.title().strip()
                    if not title or title == "Vasireddy Venkatadri International Technological University":
                        title = path.strip("/").replace("-", " ").replace("/", " — ").title()

                    documents.append({
                        "category": category,
                        "title":    title,
                        "url":      url,
                        "text":     text,
                    })
                    print(f"     ✓ {title} ({len(text)} chars)")

                except PlaywrightTimeout:
                    print(f"     ✗ Timeout on {url}")
                except Exception as e:
                    print(f"     ✗ Error on {url}: {e}")

                time.sleep(0.5)

        browser.close()

    return documents

# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────

def main():
    print("=" * 60)
    print("VVIT Helpdesk Agent — Playwright Web Scraper (v2.0)")
    print("=" * 60)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    documents = scrape_all()

    print(f"\n{'='*60}")
    print(f"✅ Total pages scraped: {len(documents)}")
    for cat in TARGET_PAGES:
        count = sum(1 for d in documents if d["category"] == cat)
        print(f"   {cat}: {count} pages")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Saved to: {OUTPUT_FILE}")
    print("Next step → Run: python build_index.py")

if __name__ == "__main__":
    main()
