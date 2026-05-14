"""
interface.py
------------
Main interface entry point for the subscription management system.

This file orchestrates:
- Background monitoring service
- Notification system
- Chatbot interface
- Web search integration

Usage:
  python interface.py
  
Commands:
  - start: Start background agent
  - chat: Start chatbot interface
  - both: Start both services
"""

import sys
import logging
import threading
import subprocess
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
)
logger = logging.getLogger(__name__)


class SubscriptionInterface:
    """Main interface for subscription management system."""

    def __init__(self):
        """Initialize the interface."""
        self.bg_process = None
        self.chat_process = None

    def start_background_agent(self):
        """Start the background monitoring agent."""
        logger.info("🚀 Starting background agent...")

        try:
            self.bg_process = subprocess.Popen(
                [sys.executable, "background_agent.py"],
                cwd=Path(__file__).parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logger.info(f"✅ Background agent started (PID: {self.bg_process.pid})")
            return True
        except Exception as e:
            logger.error(f"Failed to start background agent: {e}")
            return False

    def start_chatbot(self):
        """Start the chatbot web interface."""
        logger.info("🤖 Starting chatbot interface...")

        try:
            self.chat_process = subprocess.Popen(
                [sys.executable, "chatbot_ui.py"],
                cwd=Path(__file__).parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logger.info(f"✅ Chatbot started (PID: {self.chat_process.pid})")
            logger.info("📍 Chatbot available at http://localhost:5000")
            return True
        except Exception as e:
            logger.error(f"Failed to start chatbot: {e}")
            return False

    def start_both(self):
        """Start both background agent and chatbot."""
        logger.info("=" * 50)
        logger.info("🎯 Starting Complete Subscription Manager System")
        logger.info("=" * 50)

        if self.start_background_agent():
            time.sleep(2)  # Give background agent time to start

        if self.start_chatbot():
            logger.info("\n" + "=" * 50)
            logger.info("✅ System Started Successfully!")
            logger.info("=" * 50)
            logger.info("\n📍 Access the chatbot at: http://localhost:5000")
            logger.info("🔔 Background notifications will appear on your screen")
            logger.info("📊 Subscriptions are being monitored...")
            logger.info("\nPress Ctrl+C to stop all services\n")

    def stop_all(self):
        """Stop all services."""
        logger.info("\n⏹️  Stopping all services...")

        if self.bg_process:
            try:
                self.bg_process.terminate()
                self.bg_process.wait(timeout=5)
                logger.info("✓ Background agent stopped")
            except:
                self.bg_process.kill()
                logger.info("✓ Background agent killed")

        if self.chat_process:
            try:
                self.chat_process.terminate()
                self.chat_process.wait(timeout=5)
                logger.info("✓ Chatbot stopped")
            except:
                self.chat_process.kill()
                logger.info("✓ Chatbot killed")

        logger.info("\n✅ All services stopped")

    def interactive_menu(self):
        """Show interactive menu."""
        print("\n" + "=" * 60)
        print("💰 Subscription Manager - Main Interface")
        print("=" * 60)
        print("\nOptions:")
        print("  1. 🚀 Start background agent (monitoring only)")
        print("  2. 🤖 Start chatbot (web interface only)")
        print("  3. 🎯 Start both services (recommended)")
        print("  4. ⚙️  Settings")
        print("  5. ❌ Exit")
        print("\n" + "=" * 60)

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            self.start_background_agent()
            self._keep_running()
        elif choice == "2":
            self.start_chatbot()
            self._keep_running()
        elif choice == "3":
            self.start_both()
            self._keep_running()
        elif choice == "4":
            self.show_settings()
        elif choice == "5":
            logger.info("Goodbye! 👋")
            sys.exit(0)
        else:
            logger.error("Invalid choice")
            time.sleep(1)
            self.interactive_menu()

    def _keep_running(self):
        """Keep services running."""
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_all()
            sys.exit(0)

    def show_settings(self):
        """Show settings menu."""
        print("\n" + "=" * 60)
        print("⚙️  Settings")
        print("=" * 60)
        print("\nAvailable settings:")
        print("  1. Notification frequency (1-60 minutes)")
        print("  2. Daily analysis time")
        print("  3. Weekly report day")
        print("  4. Minimum savings threshold")
        print("  5. Back to main menu")
        print("\n" + "=" * 60)

        choice = input("Enter your choice (1-5): ").strip()

        if choice in ["1", "2", "3", "4"]:
            logger.info(f"Setting {choice} - coming soon!")
        elif choice == "5":
            self.interactive_menu()
        else:
            logger.error("Invalid choice")
            self.show_settings()


def main():
    """Main entry point."""
    # Check dependencies
    logger.info("📋 Checking dependencies...")

    required_packages = {
        "flask": "Flask",
        "win10toast": "win10toast",
        "apscheduler": "APScheduler",
    }

    missing = []
    for module, name in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(name)

    if missing:
        logger.warning(f"⚠️  Missing packages: {', '.join(missing)}")
        logger.info(f"Install with: pip install {' '.join(missing)}")
        response = input("\nContinue anyway? (y/n): ").strip().lower()
        if response != "y":
            sys.exit(1)

    logger.info("✅ Dependencies check complete\n")

    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        interface = SubscriptionInterface()

        if command == "start":
            interface.start_both()
            interface._keep_running()
        elif command == "background":
            interface.start_background_agent()
            interface._keep_running()
        elif command == "chat":
            interface.start_chatbot()
            interface._keep_running()
        else:
            print("Usage: python interface.py [start|background|chat]")
            print("\nCommands:")
            print("  start      - Start both background and chatbot")
            print("  background - Start only background agent")
            print("  chat       - Start only chatbot interface")
            sys.exit(1)
    else:
        # Show interactive menu
        interface = SubscriptionInterface()
        interface.interactive_menu()


if __name__ == "__main__":
    main()
