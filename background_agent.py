"""
background_agent.py
-------------------
Background service that monitors subscriptions and sends notifications.

This service:
- Runs in the background
- Monitors subscription costs and expiration dates
- Sends notifications when actions are recommended
- Can be run as a scheduled task or Windows Service

Usage:
  python background_agent.py
  
Or import as a module:
  from background_agent import SubscriptionMonitor
  monitor = SubscriptionMonitor()
  monitor.start()
"""

import logging
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from notification_handler import NotificationHandler
from web_search_engine import WebSearchEngine
import azure_db_manager as db

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
)


class SubscriptionMonitor:
    """Monitor subscriptions and send notifications."""

    def __init__(self, check_interval_minutes: int = 60):
        """
        Initialize subscription monitor.

        Args:
            check_interval_minutes: How often to check subscriptions (default: 60 minutes)
        """
        self.db_manager = db.AzureDBManager()
        self.notifier = NotificationHandler()
        self.search_engine = WebSearchEngine()
        self.check_interval = check_interval_minutes
        self.scheduler = BackgroundScheduler()
        self.is_running = False

    def start(self):
        """Start the background monitoring service."""
        logger.info("🚀 Starting Subscription Monitor...")

        # Schedule subscription checks
        self.scheduler.add_job(
            self.check_all_subscriptions,
            "interval",
            minutes=self.check_interval,
            id="subscription_check",
            name="Check all subscriptions",
        )

        # Schedule daily analysis
        self.scheduler.add_job(
            self.analyze_spending,
            "cron",
            hour=9,  # 9 AM daily
            id="daily_analysis",
            name="Daily spending analysis",
        )

        # Schedule weekly report
        self.scheduler.add_job(
            self.generate_weekly_report,
            "cron",
            day_of_week="mon",
            hour=8,  # Every Monday at 8 AM
            id="weekly_report",
            name="Weekly subscription report",
        )

        self.scheduler.start()
        self.is_running = True
        logger.info(f"✅ Subscription Monitor started (checking every {self.check_interval} minutes)")

        # Keep the scheduler running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping Subscription Monitor...")
            self.stop()

    def stop(self):
        """Stop the background monitoring service."""
        self.scheduler.shutdown()
        self.is_running = False
        logger.info("✓ Subscription Monitor stopped")

    def check_all_subscriptions(self):
        """Check all subscriptions and send notifications."""
        logger.info("🔍 Checking all subscriptions...")

        try:
            # Get all subscriptions from database
            subscriptions = self.db_manager.query("SELECT * FROM subscriptions")

            if not subscriptions:
                logger.info("No subscriptions found")
                return

            logger.info(f"Found {len(subscriptions)} subscriptions to check")

            for sub in subscriptions:
                self._check_single_subscription(sub)

        except Exception as e:
            logger.error(f"Error checking subscriptions: {e}")

    def _check_single_subscription(self, subscription: Dict):
        """
        Check a single subscription and send notifications if needed.

        Args:
            subscription: Subscription data dict
        """
        try:
            service_name = subscription.get("service_name", "")
            amount = subscription.get("amount")
            billing_date = subscription.get("billing_date")
            status = subscription.get("status", "active")

            if status != "active":
                return

            # Check 1: Look for cheaper alternatives
            self._check_for_cheaper_alternatives(subscription)

            # Check 2: High usage warning
            self._check_high_usage(subscription)

            # Check 3: Subscription expiring soon
            self._check_expiration(subscription)

            # Check 4: Unused subscription
            self._check_usage_pattern(subscription)

        except Exception as e:
            logger.error(f"Error checking subscription: {e}")

    def _check_for_cheaper_alternatives(self, subscription: Dict):
        """Check if there are cheaper alternatives available."""
        service_name = subscription.get("service_name", "")
        amount_str = subscription.get("amount", "")

        if not amount_str:
            return

        alternative = self.search_engine.find_cheaper_alternative(service_name, amount_str)

        if alternative:
            savings = alternative.get("savings", "")
            logger.info(
                f"💰 Found cheaper alternative for {service_name}: "
                f"{alternative['name']} (save {savings})"
            )

            self.notifier.notify_better_deal(
                current_service=service_name,
                better_service=alternative["name"],
                savings=savings,
            )

    def _check_high_usage(self, subscription: Dict):
        """Check for unusually high usage patterns."""
        # This would check usage history if available
        pass

    def _check_expiration(self, subscription: Dict):
        """Check if subscription is expiring soon."""
        billing_date = subscription.get("billing_date")
        billing_cycle = subscription.get("billing_cycle", "monthly")

        if not billing_date:
            return

        try:
            # Parse billing date
            bill_datetime = datetime.fromisoformat(billing_date)
            today = datetime.now()

            # Calculate next billing date
            if billing_cycle == "yearly":
                next_bill = bill_datetime + timedelta(days=365)
            elif billing_cycle == "quarterly":
                next_bill = bill_datetime + timedelta(days=90)
            else:  # monthly
                next_bill = bill_datetime + timedelta(days=30)

            days_until_billing = (next_bill - today).days

            # Notify if billing is in 3 days or less
            if 0 < days_until_billing <= 3:
                logger.info(
                    f"⏰ {subscription['service_name']} "
                    f"will be billed in {days_until_billing} days"
                )
                self.notifier.notify_subscription_expiring(
                    service_name=subscription["service_name"],
                    days_left=days_until_billing,
                )

        except Exception as e:
            logger.warning(f"Could not check expiration: {e}")

    def _check_usage_pattern(self, subscription: Dict):
        """Check if subscription appears to be unused."""
        # This would check usage history
        # If no usage in last 30 days, suggest cancellation
        pass

    def analyze_spending(self):
        """Analyze total spending and identify patterns."""
        logger.info("📊 Analyzing spending patterns...")

        try:
            subscriptions = self.db_manager.query("SELECT * FROM subscriptions WHERE status = 'active'")

            if not subscriptions:
                return

            total_monthly = 0
            total_yearly = 0
            by_category = {}

            for sub in subscriptions:
                amount = sub.get("amount", "").replace("$", "").replace(",", "")
                try:
                    amount_float = float(amount.split("/")[0])
                    category = sub.get("category", "other")

                    total_monthly += amount_float
                    total_yearly += amount_float * 12

                    if category not in by_category:
                        by_category[category] = 0
                    by_category[category] += amount_float

                except:
                    pass

            logger.info(
                f"💰 Spending Summary:\n"
                f"  Monthly: ${total_monthly:.2f}\n"
                f"  Yearly: ${total_yearly:.2f}\n"
                f"  By Category: {by_category}"
            )

            # Send notification if spending is high
            if total_monthly > 100:
                self.notifier.simple_notification(
                    title="💸 High Subscription Spending",
                    message=f"You're spending ${total_monthly:.2f}/month on subscriptions. "
                    f"Click to review and optimize.",
                    duration=10,
                )

        except Exception as e:
            logger.error(f"Error analyzing spending: {e}")

    def generate_weekly_report(self):
        """Generate weekly subscription report."""
        logger.info("📈 Generating weekly report...")

        try:
            subscriptions = self.db_manager.query("SELECT * FROM subscriptions WHERE status = 'active'")

            if not subscriptions:
                return

            report = "📊 **Weekly Subscription Report**\n\n"
            report += f"Total Active Subscriptions: {len(subscriptions)}\n\n"

            total = 0
            for sub in subscriptions:
                amount = sub.get("amount", "?")
                report += f"- {sub['service_name']}: {amount}\n"
                try:
                    amount_float = float(amount.replace("$", "").split("/")[0])
                    total += amount_float
                except:
                    pass

            report += f"\n**Total Monthly: ${total:.2f}**"

            logger.info(report)
            self.notifier.simple_notification(
                title="📈 Weekly Subscription Report",
                message=report,
                duration=15,
            )

        except Exception as e:
            logger.error(f"Error generating report: {e}")


def run_as_background_service():
    """Run as a background Windows service."""
    monitor = SubscriptionMonitor(check_interval_minutes=60)
    monitor.start()


if __name__ == "__main__":
    monitor = SubscriptionMonitor(check_interval_minutes=5)  # Check every 5 minutes for testing
    monitor.start()
