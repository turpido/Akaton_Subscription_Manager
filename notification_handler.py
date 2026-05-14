"""
notification_handler.py
-----------------------
Windows notification handler with clickable actions.

Sends desktop notifications and handles user interactions.
"""

import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)

try:
    from win10toast import ToastNotifier
    TOAST_AVAILABLE = True
except ImportError:
    TOAST_AVAILABLE = False


class NotificationHandler:
    """Handle Windows system notifications."""

    def __init__(self):
        """Initialize notification handler."""
        if TOAST_AVAILABLE:
            self.toaster = ToastNotifier()
        else:
            logger.warning("win10toast not installed. Install with: pip install win10toast")

    def notify_cancellation_opportunity(
        self,
        service_name: str,
        reason: str,
        action_callback: Optional[Callable] = None,
    ) -> bool:
        """
        Send notification about cancellation opportunity.

        Args:
            service_name: Name of the service
            reason: Why it should be cancelled
            action_callback: Function to call when clicked

        Returns:
            True if notification sent successfully
        """
        if not TOAST_AVAILABLE:
            return False

        title = f"💰 Cancel {service_name}?"
        message = f"{reason}\n\nClick to discuss cancellation options"

        try:
            self.toaster.show_toast(
                title=title,
                msg=message,
                duration=10,
                threaded=True,
            )
            logger.info(f"Notification sent for {service_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False

    def notify_better_deal(
        self,
        current_service: str,
        better_service: str,
        savings: str,
        action_callback: Optional[Callable] = None,
    ) -> bool:
        """
        Send notification about better deal available.

        Args:
            current_service: Current service name
            better_service: Better alternative service
            savings: Estimated savings
            action_callback: Function to call when clicked

        Returns:
            True if notification sent successfully
        """
        if not TOAST_AVAILABLE:
            return False

        title = f"🎯 Better Deal Found!"
        message = (
            f"Save {savings}/month!\n"
            f"{current_service} → {better_service}\n"
            f"Click to learn more"
        )

        try:
            self.toaster.show_toast(
                title=title,
                msg=message,
                duration=10,
                threaded=True,
            )
            logger.info(f"Better deal notification sent: {current_service} → {better_service}")
            return True
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False

    def notify_subscription_expiring(
        self, service_name: str, days_left: int, action_callback: Optional[Callable] = None
    ) -> bool:
        """
        Send notification about expiring subscription.

        Args:
            service_name: Service name
            days_left: Days until expiration
            action_callback: Function to call when clicked

        Returns:
            True if notification sent successfully
        """
        if not TOAST_AVAILABLE:
            return False

        title = f"⏰ {service_name} expires in {days_left} days"
        message = f"Click to discuss renewal or cancellation"

        try:
            self.toaster.show_toast(
                title=title,
                msg=message,
                duration=10,
                threaded=True,
            )
            logger.info(f"Expiration notification sent for {service_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False

    @staticmethod
    def simple_notification(title: str, message: str, duration: int = 5) -> bool:
        """
        Send a simple notification.

        Args:
            title: Notification title
            message: Notification message
            duration: Duration in seconds

        Returns:
            True if successful
        """
        if not TOAST_AVAILABLE:
            return False

        try:
            toaster = ToastNotifier()
            toaster.show_toast(
                title=title,
                msg=message,
                duration=duration,
                threaded=True,
            )
            return True
        except Exception as e:
            logger.error(f"Notification failed: {e}")
            return False
