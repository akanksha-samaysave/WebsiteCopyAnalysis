#!/usr/bin/env python
"""Verify that all required dependencies are installed."""

import sys

print("🔍 Verifying Python environment...\n")

errors = []

# Check core packages
packages_to_check = [
    ("fastapi", "FastAPI"),
    ("uvicorn", "Uvicorn"),
    ("sqlalchemy", "SQLAlchemy"),
    ("playwright", "Playwright"),
    ("textblob", "TextBlob"),
    ("vaderSentiment", "VADER Sentiment"),
    ("pandas", "Pandas"),
    ("numpy", "NumPy"),
    ("sklearn", "scikit-learn"),
    ("reportlab", "ReportLab"),
    ("bs4", "BeautifulSoup4"),
    ("requests", "Requests"),
]

for module_name, display_name in packages_to_check:
    try:
        __import__(module_name)
        print(f"✅ {display_name} - OK")
    except ImportError as e:
        print(f"❌ {display_name} - MISSING")
        errors.append(f"{display_name}: {str(e)}")

print("\n" + "="*50 + "\n")

# Check Playwright browsers
try:
    import subprocess
    result = subprocess.run(
        ["playwright", "install", "--with-deps", "chromium"],
        capture_output=True,
        text=True,
        timeout=120
    )
    if result.returncode == 0:
        print("✅ Playwright Chromium - Installed")
    else:
        print("⚠️  Playwright Chromium - May need installation")
        errors.append(f"Playwright install output: {result.stderr}")
except Exception as e:
    print(f"⚠️  Playwright Chromium - Could not verify: {str(e)}")

print("\n" + "="*50 + "\n")

if errors:
    print(f"❌ Found {len(errors)} issue(s):\n")
    for error in errors:
        print(f"  • {error}\n")
    print("Run: pip install -r requirements.txt")
    print("Then: playwright install chromium")
    sys.exit(1)
else:
    print("✅ All dependencies are installed!")
    print("\nYou can now run:")
    print("  python run.py")
    sys.exit(0)
