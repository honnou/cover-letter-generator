#!/bin/bash

echo "=========================================="
echo "   Cover Letter Generator - Startup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Installation failed. Trying with --break-system-packages flag..."
    pip3 install -r requirements.txt --break-system-packages
fi

echo ""
echo "=========================================="
echo "   Starting Server and Opening Browser"
echo "=========================================="
echo ""

# Start the server
echo "🚀 Starting backend server on http://localhost:8080"
echo ""
echo "💡 Tips:"
echo "   - Set ANTHROPIC_API_KEY for AI-powered generation"
echo "   - Press Ctrl+C to stop the server"
echo ""

# Open browser after a short delay
(sleep 3 && open index.html 2>/dev/null || xdg-open index.html 2>/dev/null) &

# Start the server
python3 server.py
