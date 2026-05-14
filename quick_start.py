#!/usr/bin/env python
"""
quick_start.py
--------------
Quick start guide and demo for the subscription manager system.

This script will:
1. Check all dependencies
2. Test the notification system
3. Demonstrate the web search engine
4. Give you options to start the system
"""

import sys
import subprocess
import time
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if all required packages are installed."""
    logger.info("📋 Checking dependencies...\n")

    required_packages = {
        "flask": "Flask (web server)",
        "win10toast": "win10toast (notifications)",
        "apscheduler": "APScheduler (background tasks)",
        "google_api_python_client": "Google API Client (Gmail)",
        "google_auth_oauthlib": "Google OAuth (Gmail auth)",
    }

    all_installed = True
    for module, name in required_packages.items():
        try:
            __import__(module)
            logger.info(f"✅ {name}")
        except ImportError:
            logger.warning(f"❌ {name} - NOT INSTALLED")
            all_installed = False

    if not all_installed:
        logger.error("\n⚠️  Some packages are missing!")
        logger.info("Install with: pip install -r requirements.txt")
        return False

    logger.info("\n✅ All dependencies installed!\n")
    return True


def demo_web_search():
    """Demo the web search engine."""
    logger.info("🔍 Demo: Web Search Engine\n")

    try:
        from web_search_engine import WebSearchEngine

        engine = WebSearchEngine()

        # Demo 1: Search for VPN
        logger.info("Searching for VPN services...")
        vpn_services = engine.search_service("vpn")
        logger.info(f"Found {len(vpn_services)} VPN options:")
        for service in vpn_services:
            logger.info(f"  • {service['name']}: {service['price']}")

        # Demo 2: Find cheaper alternative
        logger.info("\nFinding cheaper alternative to ChatGPT Plus ($20/mo)...")
        alternative = engine.find_cheaper_alternative("ChatGPT Plus", "$20/mo")
        if alternative:
            logger.info(f"✅ Found: {alternative['name']} ({alternative['price']})")
            logger.info(f"   Savings: {alternative['savings']}")
        else:
            logger.info("No cheaper alternative found")

        logger.info()

    except Exception as e:
        logger.error(f"Demo failed: {e}")


def demo_notifications():
    """Demo the notification system."""
    logger.info("🔔 Demo: Notification System\n")

    try:
        from notification_handler import NotificationHandler

        notifier = NotificationHandler()

        logger.info("Sending test notifications...\n")

        # Demo notification
        notifier.simple_notification(
            title="💰 Subscription Manager Test",
            message="If you see this notification, the system is working!",
            duration=5,
        )

        logger.info("✅ Test notification sent to Windows")
        logger.info("   Check your Windows notification area\n")

    except Exception as e:
        logger.error(f"Notification demo failed: {e}\n")


def show_menu():
    """Show main menu."""
    print("\n" + "=" * 60)
    print("💰 Subscription Manager - Quick Start")
    print("=" * 60)
    print("\nOptions:")
    print("  1. 🚀 Start full system (background + chatbot)")
    print("  2. 🔔 Background agent only (monitoring & notifications)")
    print("  3. 🤖 Chatbot only (web interface)")
    print("  4. 📖 View documentation")
    print("  5. ❌ Exit")
    print("\n" + "=" * 60)

    choice = input("Enter your choice (1-5): ").strip()
    return choice


def start_system(mode="both"):
    """Start the subscription manager system."""
    logger.info(f"\n🚀 Starting {mode} mode...\n")

    try:
        if mode in ["both", "background"]:
            logger.info("Starting background agent...")
            subprocess.Popen([sys.executable, "background_agent.py"])
            logger.info("✅ Background agent started")
            time.sleep(2)

        if mode in ["both", "chatbot"]:
            logger.info("Starting chatbot interface...")
            subprocess.Popen([sys.executable, "chatbot_ui.py"])
            logger.info("✅ Chatbot started")

        if mode == "chatbot" or mode == "both":
            logger.info("\n📍 Open your browser to: http://localhost:5000")

        logger.info("\n✅ System started successfully!")
        logger.info("Press Ctrl+C to stop\n")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n✓ System stopped")

    except Exception as e:
        logger.error(f"Failed to start: {e}")


def show_docs():
    """Show documentation options."""
    docs = {
        "CHATBOT_INTERFACE_README.md": "Complete system documentation",
        "GMAIL_INVOICE_READER_README.md": "Gmail invoice reader guide",
        "GMAIL_AGENT_USAGE.md": "Gmail agent usage examples",
    }

    print("\n📚 Documentation Files:\n")
    for i, (file, desc) in enumerate(docs.items(), 1):
        print(f"  {i}. {file} - {desc}")

    choice = input("\nOpen file (1-3) or press Enter to skip: ").strip()
    if choice in ["1", "2", "3"]:
        files = list(docs.keys())
        filename = files[int(choice) - 1]
        logger.info(f"Opening {filename}...")
        import webbrowser

        webbrowser.open(Path(__file__).parent / filename)


def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("🎉 Welcome to Subscription Manager!")
    print("=" * 60)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Run demos
    demo_web_search()
    demo_notifications()

    # Show menu
    while True:
        choice = show_menu()

        if choice == "1":
            start_system("both")
        elif choice == "2":
            start_system("background")
        elif choice == "3":
            start_system("chatbot")
        elif choice == "4":
            show_docs()
        elif choice == "5":
            logger.info("Goodbye! 👋")
            sys.exit(0)
        else:
            logger.error("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
