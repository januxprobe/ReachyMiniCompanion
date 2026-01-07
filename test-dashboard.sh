#!/bin/bash
# Test script for Reachy Mini Companion
# Automates the HuggingFace testing workflow

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Reachy Mini Companion - Testing Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Check app structure
echo -e "${YELLOW}[1/3] Running app structure checks...${NC}"
if reachy-mini-app-assistant check --path .; then
    echo -e "${GREEN}✅ All checks passed!${NC}"
else
    echo -e "${RED}❌ Checks failed! Fix the issues above before continuing.${NC}"
    exit 1
fi
echo ""

# Step 2: Reinstall app
echo -e "${YELLOW}[2/3] Reinstalling app...${NC}"
pip install -e . > /dev/null 2>&1
echo -e "${GREEN}✅ App reinstalled successfully!${NC}"
echo ""

# Step 3: Check if daemon is running
echo -e "${YELLOW}[3/3] Checking dashboard status...${NC}"
if curl -s http://127.0.0.1:8000/health-check > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Dashboard is already running!${NC}"
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}Ready to test!${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo "1. Open browser: http://127.0.0.1:8000/"
    echo "2. Go to Applications tab"
    echo "3. Click 'Run' on 'Reachy Mini Companion'"
    echo ""
    echo "The app should test all 4 emotions then go into idle mode."
    echo ""
else
    echo -e "${YELLOW}⚠️  Dashboard is not running${NC}"
    echo ""
    echo "Start the dashboard with:"
    echo ""
    echo "  ${GREEN}Option A (Recommended - See robot movements):${NC}"
    echo "  ${GREEN}mjpython -m reachy_mini.daemon.app.main --sim${NC}"
    echo ""
    echo "  ${GREEN}Option B (Headless - No visual):${NC}"
    echo "  ${GREEN}reachy-mini-daemon --sim --headless${NC}"
    echo ""
    echo "Then run this script again, or open:"
    echo "  http://127.0.0.1:8000/"
    echo ""
fi
