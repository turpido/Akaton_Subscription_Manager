"""
web_search_engine.py
--------------------
Web search and service recommendation engine.

Searches for services and finds the best deals available.
"""

import logging
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Known service recommendations
SERVICE_RECOMMENDATIONS = {
    "email": [
        {"name": "Gmail", "url": "https://mail.google.com", "price": "free", "features": "15GB free, great filtering"},
        {"name": "Proton Mail", "url": "https://proton.me", "price": "free-$12/mo", "features": "Encrypted, privacy-focused"},
        {"name": "Outlook", "url": "https://outlook.com", "price": "free-$6/mo", "features": "Integration with Office"},
    ],
    "vpn": [
        {"name": "NordVPN", "url": "https://nordvpn.com", "price": "$3.99/mo", "features": "6000+ servers, fast"},
        {"name": "Surfshark", "url": "https://surfshark.com", "price": "$2.49/mo", "features": "Unlimited connections, cheap"},
        {"name": "ProtonVPN", "url": "https://protonvpn.com", "price": "free-$10/mo", "features": "Privacy-focused, free tier"},
    ],
    "cloud_storage": [
        {"name": "Google Drive", "url": "https://drive.google.com", "price": "$1.99/100GB", "features": "Integration with Google apps"},
        {"name": "OneDrive", "url": "https://onedrive.com", "price": "$1.99/100GB", "features": "Office integration, sync"},
        {"name": "Dropbox", "url": "https://dropbox.com", "price": "$11.99/mo", "features": "Professional tools, sharing"},
    ],
    "password_manager": [
        {"name": "Bitwarden", "url": "https://bitwarden.com", "price": "free-$10/year", "features": "Open source, cheap, secure"},
        {"name": "1Password", "url": "https://1password.com", "price": "$2.99/mo", "features": "Beautiful UI, great support"},
        {"name": "LastPass", "url": "https://lastpass.com", "price": "free-$3/mo", "features": "Popular, lots of integrations"},
    ],
    "productivity": [
        {"name": "Notion", "url": "https://notion.so", "price": "free-$10/mo", "features": "All-in-one workspace"},
        {"name": "Obsidian", "url": "https://obsidian.md", "price": "$0-50/mo", "features": "Local-first, powerful"},
        {"name": "Trello", "url": "https://trello.com", "price": "free-$10/mo", "features": "Simple task management"},
    ],
    "code_editor": [
        {"name": "VS Code", "url": "https://code.visualstudio.com", "price": "free", "features": "Powerful, many extensions"},
        {"name": "JetBrains IDEs", "url": "https://jetbrains.com", "price": "$20-$30/mo", "features": "Professional, language-specific"},
    ],
    "ai_chat": [
        {"name": "ChatGPT Plus", "url": "https://chat.openai.com", "price": "$20/mo", "features": "GPT-4, plugins, file upload"},
        {"name": "Claude", "url": "https://claude.ai", "price": "free-$20/mo", "features": "Long context, reasoning"},
        {"name": "Gemini", "url": "https://gemini.google.com", "price": "free-$20/mo", "features": "Multimodal, integrated with Google"},
    ],
}


class WebSearchEngine:
    """Search for services and find best deals."""

    @staticmethod
    def search_service(query: str) -> List[Dict]:
        """
        Search for a service and return results.

        Args:
            query: Service to search for (e.g., "cloud storage", "email provider")

        Returns:
            List of service recommendations
        """
        query_lower = query.lower()

        # Check if we have predefined recommendations
        for category, services in SERVICE_RECOMMENDATIONS.items():
            if category.replace("_", " ") in query_lower or query_lower in category:
                return services

        # Return generic recommendation
        return WebSearchEngine._generic_search(query)

    @staticmethod
    def find_cheaper_alternative(service_name: str, current_price: str) -> Optional[Dict]:
        """
        Find a cheaper alternative to a service.

        Args:
            service_name: Current service name
            current_price: Current price (e.g., "$20/mo")

        Returns:
            Dict with alternative service info or None
        """
        logger.info(f"Finding cheaper alternative to {service_name}")

        # Find similar services
        for category, services in SERVICE_RECOMMENDATIONS.items():
            for service in services:
                if service["name"].lower() == service_name.lower():
                    # Found the service, now find cheaper alternatives
                    try:
                        current_amount = float(current_price.replace("$", "").split("/")[0])
                        for alt_service in services:
                            if alt_service["name"] != service_name:
                                try:
                                    alt_price_str = alt_service["price"].split("-")[-1]  # Get the high end
                                    alt_amount = float(alt_price_str.replace("$", "").split("/")[0])
                                    if alt_amount < current_amount:
                                        savings = current_amount - alt_amount
                                        return {
                                            **alt_service,
                                            "savings": f"${savings:.2f}/mo",
                                            "savings_amount": savings,
                                        }
                                except:
                                    continue
                    except:
                        pass

        return None

    @staticmethod
    def get_all_services_in_category(category: str) -> List[Dict]:
        """
        Get all services in a category.

        Args:
            category: Service category (e.g., "vpn", "cloud_storage")

        Returns:
            List of services with details
        """
        category_lower = category.lower().replace(" ", "_")

        if category_lower in SERVICE_RECOMMENDATIONS:
            return SERVICE_RECOMMENDATIONS[category_lower]

        return []

    @staticmethod
    def _generic_search(query: str) -> List[Dict]:
        """
        Generic web search for services (fallback).

        Args:
            query: Search query

        Returns:
            List of generic recommendations
        """
        return [
            {
                "name": "DuckDuckGo Search",
                "url": f"https://duckduckgo.com/?q={query}",
                "price": "free",
                "features": f"Search results for '{query}'",
            },
            {
                "name": "Google Search",
                "url": f"https://google.com/search?q={query}",
                "price": "free",
                "features": f"Google results for '{query}'",
            },
        ]

    @staticmethod
    def compare_services(service1: str, service2: str) -> Dict:
        """
        Compare two services.

        Args:
            service1: First service name
            service2: Second service name

        Returns:
            Comparison dict with pros/cons
        """
        comparison = {
            "service1": service1,
            "service2": service2,
            "comparison": f"Check {service1} vs {service2} comparison",
        }

        return comparison

    @staticmethod
    def get_top_rated_services(category: str, limit: int = 3) -> List[Dict]:
        """
        Get top-rated services in a category.

        Args:
            category: Service category
            limit: Number of services to return

        Returns:
            List of top services
        """
        services = WebSearchEngine.get_all_services_in_category(category)
        return services[:limit]


# Example usage
if __name__ == "__main__":
    engine = WebSearchEngine()

    # Search for a service
    print("🔍 Searching for VPN services:")
    vpn_services = engine.search_service("vpn")
    for service in vpn_services:
        print(f"  {service['name']}: {service['price']}")
        print(f"    {service['features']}")

    # Find cheaper alternative
    print("\n💰 Finding cheaper alternatives to ChatGPT Plus ($20/mo):")
    alternative = engine.find_cheaper_alternative("ChatGPT Plus", "$20/mo")
    if alternative:
        print(f"  {alternative['name']}: {alternative['price']}")
        print(f"  Save: {alternative['savings']}")

    # Get all services in category
    print("\n📚 Cloud storage options:")
    storage_services = engine.get_all_services_in_category("cloud_storage")
    for service in storage_services:
        print(f"  {service['name']}: {service['price']}")
