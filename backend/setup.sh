#!/bin/bash
# Setup script for Landing Page Intelligence backend

echo "🚀 Installing Python dependencies..."
pip install -r requirements.txt

echo "📦 Installing Playwright browsers..."
playwright install chromium

echo "🔤 Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo "✅ Setup complete!"
echo ""
echo "To start the backend, run:"
echo "  python run.py"
