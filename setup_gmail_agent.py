"""
setup_gmail_agent.py
--------------------
Setup script for Gmail invoice reader agent.

This script will:
1. Check if credentials exist
2. Guide you through Google Cloud Console setup
3. Test the Gmail connection
4. Run a sample invoice search

Usage:
  python setup_gmail_agent.py
"""

import os
import sys
import webbrowser
from pathlib import Path

def check_credentials():
    """Check if Gmail credentials file exists."""
    credentials_file = "gmail_credentials.json"
    if os.path.exists(credentials_file):
        print(f"✅ Found credentials file: {credentials_file}")
        return True
    else:
        print(f"❌ Missing credentials file: {credentials_file}")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    required_imports = [
        ("google_auth_oauthlib", "google-auth-oauthlib"),
        ("google_auth_httplib2", "google-auth-httplib2"),
        ("googleapiclient", "google-api-python-client")
    ]

    missing = []
    for import_name, package_name in required_imports:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)

    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages installed")
        return True

def open_google_console():
    """Open Google Cloud Console in browser."""
    url = "https://console.cloud.google.com"
    print(f"🌐 Opening Google Cloud Console: {url}")
    webbrowser.open(url)

def main():
    """Main setup function."""
    print("🚀 Gmail Invoice Reader Agent Setup")
    print("=" * 50)

    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Please install missing packages first.")
        sys.exit(1)

    # Check credentials
    print("\n🔑 Checking Gmail credentials...")
    has_credentials = check_credentials()

    if not has_credentials:
        print("\n📋 You need to set up Google Cloud credentials:")
        print("\nStep 1: Create Google Cloud Project")
        print("  - Go to https://console.cloud.google.com")
        print("  - Click 'Create Project'")
        print("  - Name it 'Gmail Invoice Reader' or similar")
        print("  - Wait for project creation")

        print("\nStep 2: Enable Gmail API")
        print("  - In the search bar, type 'Gmail API'")
        print("  - Click on 'Gmail API' result")
        print("  - Click 'Enable'")

        print("\nStep 3: Create OAuth Credentials")
        print("  - Left sidebar → 'APIs & Services' → 'Credentials'")
        print("  - Click '+ Create Credentials' → 'OAuth 2.0 Client ID'")
        print("  - If prompted: Configure OAuth consent screen")
        print("    • User Type: External")
        print("    • App name: 'Gmail Invoice Reader'")
        print("    • Add scope: Gmail API (readonly)")
        print("  - Application type: 'Desktop application'")
        print("  - Click 'Create'")

        print("\nStep 4: Download Credentials")
        print("  - In Credentials page, click download icon")
        print("  - Save as 'gmail_credentials.json' in this folder")

        input("\n⏳ Press Enter after downloading credentials...")

        if not check_credentials():
            print("❌ Still no credentials file found. Please try again.")
            sys.exit(1)

    # Test the agent
    print("\n🧪 Testing Gmail connection...")
    try:
        from gmail_invoice_reader import GmailInvoiceReader

        print("📧 Connecting to Gmail (this will open a browser for authorization)...")
        agent = GmailInvoiceReader()

        print("🔎 Testing invoice search...")
        invoices = agent.find_invoices(days_back=30, max_results=5)

        print(f"\n✅ Success! Found {len(invoices)} invoice emails in the last 30 days.")

        if invoices:
            print("\n📄 Sample invoice:")
            invoice = invoices[0]
            print(f"  Subject: {invoice['subject']}")
            print(f"  From: {invoice['from']}")
            print(f"  Amount: {invoice['amount'] or 'Not found'}")

        print("\n🎉 Setup complete! You can now run:")
        print("  python gmail_invoice_reader.py")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("💡 Check your credentials and internet connection.")
        sys.exit(1)

if __name__ == "__main__":
    main()
