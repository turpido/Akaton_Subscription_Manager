"""
gmail_invoice_reader.py
-----------------------
Simple Gmail invoice reader agent.

This is a simplified version of the Gmail agent that focuses on:
1. Connecting to Gmail via OAuth2
2. Searching for invoice emails
3. Extracting and displaying invoice information

Usage:
  python gmail_invoice_reader.py
"""

import logging
import os
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_python_client import discovery
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Gmail API scopes - readonly access only
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Credentials file path
CREDENTIALS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE", "gmail_credentials.json")
TOKEN_PICKLE = "gmail_token.pickle"


class GmailInvoiceReader:
    """Simple agent to read invoice emails from Gmail."""

    def __init__(self, credentials_file: str = CREDENTIALS_FILE):
        """
        Initialize Gmail API client with OAuth2 authentication.

        Args:
            credentials_file: Path to Google OAuth2 credentials JSON file
        """
        self.credentials_file = credentials_file
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API using OAuth2."""
        creds = None

        # Load token from pickle if it exists
        if os.path.exists(TOKEN_PICKLE):
            with open(TOKEN_PICKLE, "rb") as token:
                creds = pickle.load(token)

        # If credentials are invalid or expired, refresh or re-authenticate
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif not creds or not creds.valid:
            if not os.path.exists(self.credentials_file):
                raise FileNotFoundError(
                    f"Gmail credentials file not found: {self.credentials_file}\n"
                    "Download from Google Cloud Console and save as 'gmail_credentials.json'"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, SCOPES
            )
            creds = flow.run_local_server(port=0)

            # Save token for future use
            with open(TOKEN_PICKLE, "wb") as token:
                pickle.dump(creds, token)

        self.service = discovery.build("gmail", "v1", credentials=creds)
        logger.info("✓ Gmail API authenticated successfully")

    def find_invoices(self, days_back: int = 90, max_results: int = 20) -> List[Dict]:
        """
        Search Gmail for invoice emails.

        Args:
            days_back: Search emails from the last N days (default 90)
            max_results: Maximum number of results to return (default 20)

        Returns:
            List of invoice dicts with: id, from, subject, date, amount, snippet
        """
        if not self.service:
            raise RuntimeError("Gmail API not authenticated")

        # Search query for invoices
        query_parts = [
            'invoice',  # Must contain "invoice"
            f'after:{(datetime.now() - timedelta(days=days_back)).strftime("%Y/%m/%d")}'
        ]
        query = " ".join(query_parts)

        logger.info(f"Searching Gmail for invoices: {query}")

        try:
            # Search for emails
            results = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, maxResults=max_results)
                .execute()
            )

            messages = results.get("messages", [])

            if not messages:
                logger.info("No invoice emails found")
                return []

            logger.info(f"Found {len(messages)} invoice emails, fetching details...")

            # Fetch full details for each email
            invoices = []
            for msg in messages:
                invoice_data = self._get_invoice_details(msg["id"])
                if invoice_data:
                    invoices.append(invoice_data)

            return invoices

        except Exception as e:
            logger.error(f"Error searching Gmail: {e}")
            return []

    def _get_invoice_details(self, message_id: str) -> Optional[Dict]:
        """
        Fetch and parse a single invoice email.

        Args:
            message_id: Gmail message ID

        Returns:
            Dict with invoice metadata: from, subject, date, amount, snippet
        """
        try:
            msg = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )

            headers = msg["payload"]["headers"]
            snippet = msg.get("snippet", "")

            # Extract key fields
            invoice_dict = {
                "id": message_id,
                "from": self._get_header(headers, "From"),
                "subject": self._get_header(headers, "Subject"),
                "date": self._get_header(headers, "Date"),
                "snippet": snippet,
                "amount": self._extract_amount(snippet),
                "service": self._extract_service_name(
                    self._get_header(headers, "From"),
                    self._get_header(headers, "Subject")
                ),
            }

            return invoice_dict

        except Exception as e:
            logger.warning(f"Error fetching message {message_id}: {e}")
            return None

    @staticmethod
    def _get_header(headers: List[Dict], name: str) -> str:
        """Extract header value from email headers."""
        for header in headers:
            if header["name"] == name:
                return header["value"]
        return ""

    @staticmethod
    def _extract_amount(text: str) -> Optional[str]:
        """
        Extract currency amount from email text.

        Matches patterns like: $99.99, £10.00, €50, etc.
        """
        import re
        match = re.search(r"[$£€¥₹₽][\d,]+\.?\d*", text)
        return match.group(0) if match else None

    @staticmethod
    def _extract_service_name(from_email: str, subject: str) -> Optional[str]:
        """
        Extract service name from sender email.

        Examples:
          billing@stripe.com → Stripe
          noreply@github.com → GitHub
        """
        from_email = from_email.lower()

        # Common service mappings
        mappings = {
            "stripe": ["stripe.com"],
            "github": ["github.com"],
            "aws": ["aws.amazon.com", "amazon.com"],
            "azure": ["microsoft.com", "azure.microsoft.com"],
            "google": ["google.com"],
            "apple": ["apple.com"],
            "netflix": ["netflix.com"],
            "spotify": ["spotify.com"],
        }

        for service, domains in mappings.items():
            for domain in domains:
                if domain in from_email:
                    return service.capitalize()

        # Fallback: extract domain name
        if "@" in from_email:
            domain = from_email.split("@")[1].split(".")[0]
            if domain and domain not in ["noreply", "no-reply", "mail", "notification"]:
                return domain.capitalize()

        return None


def main():
    """Simple demo of the Gmail invoice reader."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
    )

    print("🔍 Gmail Invoice Reader Agent")
    print("=" * 40)

    try:
        # Initialize the agent
        print("📧 Connecting to Gmail...")
        agent = GmailInvoiceReader()

        # Search for invoices
        print("🔎 Searching for invoice emails...")
        invoices = agent.find_invoices(days_back=90, max_results=15)

        if invoices:
            print(f"\n✅ Found {len(invoices)} invoice emails:\n")

            for i, invoice in enumerate(invoices, 1):
                print(f"{i}. 📄 {invoice['subject']}")
                print(f"   🏢 Service: {invoice['service'] or 'Unknown'}")
                print(f"   👤 From: {invoice['from']}")
                print(f"   📅 Date: {invoice['date']}")
                print(f"   💰 Amount: {invoice['amount'] or 'Not found'}")
                print(f"   📝 Preview: {invoice['snippet'][:80]}...")
                print()

        else:
            print("\n❌ No invoice emails found.")
            print("💡 Try increasing 'days_back' or check your Gmail for invoice emails.")

    except FileNotFoundError as e:
        print(f"\n❌ Setup required: {e}")
        print("\n📋 To set up:")
        print("1. Go to https://console.cloud.google.com")
        print("2. Create a new project")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 Desktop credentials")
        print("5. Download JSON and save as 'gmail_credentials.json'")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check your internet connection and credentials.")


if __name__ == "__main__":
    main()
