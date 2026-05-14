"""
chatbot_ui.py
-------------
Web-based chatbot interface using Flask.

Runs as a local web server (http://localhost:5000) that opens in the browser.
"""

import logging
import json
from datetime import datetime
from typing import List, Dict, Optional
from flask import Flask, render_template, request, jsonify
from web_search_engine import WebSearchEngine
import webbrowser
import threading
import time

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Store conversation history
conversation_history: List[Dict] = []
current_context: Dict = {
    "service": None,
    "reason": None,
    "mode": None,  # "cancellation", "better_deal", "search_service"
}


@app.route("/")
def index():
    """Main chatbot page."""
    return render_template("chatbot.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Handle chat messages.

    Expected JSON:
        {
            "message": "user message",
            "context": {optional context data}
        }
    """
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Add user message to history
    conversation_history.append({"role": "user", "message": user_message, "timestamp": datetime.now().isoformat()})

    # Generate bot response
    bot_response = generate_response(user_message)

    # Add bot response to history
    conversation_history.append({"role": "bot", "message": bot_response["text"], "timestamp": datetime.now().isoformat()})

    return jsonify(bot_response)


@app.route("/api/init-cancellation", methods=["POST"])
def init_cancellation():
    """Initialize cancellation conversation."""
    data = request.json
    service_name = data.get("service_name", "")
    reason = data.get("reason", "")

    current_context["mode"] = "cancellation"
    current_context["service"] = service_name
    current_context["reason"] = reason

    response_text = (
        f"I can help you with cancelling {service_name}. 🤔\n\n"
        f"**Issue:** {reason}\n\n"
        f"Here are your options:\n\n"
        f"1. **Get Cancellation Link** - I'll find the cancellation process for you\n"
        f"2. **Find Alternatives** - Let me suggest better services\n"
        f"3. **Negotiate** - Ways to get better pricing without cancelling\n\n"
        f"What would you like to do?"
    )

    return jsonify({
        "text": response_text,
        "actions": [
            {"label": "Get Cancellation Link", "action": "get_cancellation_link"},
            {"label": "Find Alternatives", "action": "find_alternatives"},
            {"label": "Negotiate Pricing", "action": "negotiate"},
        ],
    })


@app.route("/api/init-better-deal", methods=["POST"])
def init_better_deal():
    """Initialize better deal conversation."""
    data = request.json
    current_service = data.get("current_service", "")
    better_service = data.get("better_service", "")
    savings = data.get("savings", "")

    current_context["mode"] = "better_deal"
    current_context["service"] = current_service

    response_text = (
        f"Great! I found a better deal for you! 💰\n\n"
        f"**Current:** {current_service}\n"
        f"**Better Option:** {better_service}\n"
        f"**Potential Savings:** {savings}/month\n\n"
        f"What would you like to do?\n\n"
        f"1. **See the Link** - Open {better_service}'s website\n"
        f"2. **Compare Features** - See detailed comparison\n"
        f"3. **Cancel Current** - Help me switch services\n"
        f"4. **Not Interested** - Keep current service"
    )

    return jsonify({
        "text": response_text,
        "actions": [
            {"label": f"See {better_service} →", "action": "show_link", "url": f"https://{better_service.lower().replace(' ', '')}.com"},
            {"label": "Compare", "action": "compare_services"},
            {"label": "Cancel Current", "action": "initiate_cancellation"},
            {"label": "Keep Current", "action": "decline_offer"},
        ],
    })


@app.route("/api/search-service", methods=["POST"])
def search_service():
    """Search for a new service."""
    data = request.json
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Empty query"}), 400

    current_context["mode"] = "search_service"

    # Search for services
    services = WebSearchEngine.search_service(query)

    response_text = f"I found **{len(services)}** great options for {query}:\n\n"

    for i, service in enumerate(services, 1):
        response_text += f"**{i}. {service['name']}** - {service['price']}\n"
        response_text += f"   {service['features']}\n\n"

    return jsonify({
        "text": response_text,
        "services": services,
        "actions": [{"label": f"Learn More →", "action": "open_service", "url": s["url"]} for s in services],
    })


@app.route("/api/get-cancellation-link", methods=["POST"])
def get_cancellation_link():
    """Get cancellation link for a service."""
    service = current_context.get("service", "")

    # Service-specific cancellation links
    cancellation_links = {
        "netflix": "https://www.netflix.com/account/cancel",
        "spotify": "https://www.spotify.com/account/cancel",
        "hulu": "https://www.hulu.com/account/cancel",
        "chatgpt": "https://platform.openai.com/account/billing/overview",
        "github": "https://github.com/settings/billing",
        "stripe": "https://dashboard.stripe.com/settings",
        "aws": "https://console.aws.amazon.com/billing/",
        "azure": "https://portal.azure.com/#blade/Microsoft_Azure_Billing",
    }

    # Find matching link
    link = cancellation_links.get(service.lower())

    if link:
        response_text = (
            f"**Cancellation Instructions for {service}:**\n\n"
            f"1. Click the link below to go to your account settings\n"
            f"2. Look for 'Billing', 'Subscriptions', or 'Account Settings'\n"
            f"3. Find the option to 'Cancel Subscription' or 'Manage Billing'\n"
            f"4. Follow the prompts (may ask for reason/feedback)\n\n"
            f"**Direct Link:** {link}"
        )

        return jsonify({
            "text": response_text,
            "link": link,
            "actions": [{"label": "Open Link →", "action": "open_link", "url": link}],
        })
    else:
        response_text = (
            f"I don't have a direct link for {service}, but here's how to find it:\n\n"
            f"1. Go to {service}'s website\n"
            f"2. Log into your account\n"
            f"3. Look for: Settings → Billing → Subscriptions → Cancel\n"
            f"4. Or search '{service} how to cancel'\n\n"
            f"Would you like me to search for it?"
        )

        return jsonify({
            "text": response_text,
            "actions": [
                {"label": "Search Instructions", "action": "search_cancellation"},
                {"label": "Contact Support", "action": "contact_support"},
            ],
        })


def generate_response(user_message: str) -> Dict:
    """
    Generate bot response based on user message with enhanced NLP logic.
    """
    logger.info(f"Generating response for user message: {user_message}")
    message_lower = user_message.lower()

    # Small talk and greetings
    greetings = ["hello", "hi", "hey", "greetings", "good morning", "good evening", "yo"]
    if any(greet in message_lower for greet in greetings) and len(message_lower.split()) < 3:
        return {
            "text": "Hello there! 👋 I'm your personal subscription concierge. How can I help you optimize your spending today?",
            "actions": [
                {"label": "💰 View Savings", "action": "find_better_deal"},
                {"label": "❌ Cancel Service", "action": "cancel_service"},
                {"label": "🔍 Find New App", "action": "search"}
            ]
        }

    # Help intent
    if "help" in message_lower or "what can you do" in message_lower:
        return {
            "text": "I'm here to help you manage your digital life! 🚀\n\nI can:\n• **Find better deals** on VPNs, Cloud Storage, and more.\n• **Guide you through cancellations** with direct links.\n• **Analyze your invoices** from Gmail.\n• **Monitor spending** in the background.\n\nTry asking 'Find me a cheap VPN' or 'How do I cancel Netflix?'",
            "actions": [
                {"label": "Search VPNs", "action": "search_vpn"},
                {"label": "Cancel Netflix", "action": "cancel_netflix"}
            ]
        }

    # Context-aware responses
    if current_context.get("mode") == "cancellation":
        # ...existing code...
        if "link" in message_lower or "cancel" in message_lower:
            # ...existing code...
            return get_cancellation_link()

        elif "alternative" in message_lower or "better" in message_lower or "switch" in message_lower:
            # ...existing code...
            response_text = (
                f"I've got you covered! switching from **{current_context.get('service')}** can save you significant money. 💸\n\n"
                f"I recommend looking at these categories:\n"
                f"• Cloud Storage\n• VPN\n• Productivity Tools\n• AI Chat\n\n"
                f"Which one should we explore first?"
            )
            return {
                "text": response_text,
                "actions": [
                    {"label": "Cloud Storage", "action": "search_storage"},
                    {"label": "VPN Options", "action": "search_vpn"},
                    {"label": "AI Assistants", "action": "search_ai"}
                ]
            }

    # Search mode (Enhanced)
    search_triggers = ["search", "find", "looking for", "recommend", "show me", "best", "cheap"]
    if any(trigger in message_lower for trigger in search_triggers):
        # ...existing code...
        keywords = {
            "vpn": ["vpn", "proxy", "nord", "surfshark"],
            "storage": ["storage", "drive", "cloud", "dropbox", "backup"],
            "email": ["email", "gmail", "outlook", "mail"],
            "chat": ["chat", "ai", "gpt", "claude", "bot"],
            "password": ["password", "manager", "bitwarden", "lastpass"],
            "productivity": ["productivity", "notion", "trello", "obsidian"]
        }
        
        for category, synonyms in keywords.items():
            if any(syn in message_lower for syn in synonyms):
                services = WebSearchEngine.search_service(category)
                response_text = f"I've curated the top **{len(services)}** {category} options for you! 🎯\n\n"
                for i, service in enumerate(services, 1):
                    response_text += f"**{i}. {service['name']}** - {service['price']}\n   *{service['features']}*\n\n"
                
                return {
                    "text": response_text + "Does one of these fit your needs?",
                    "actions": [{"label": f"Get {s['name']}", "action": "open_url", "url": s["url"]} for s in services]
                }

    # Fallback to generic but more polite response
    return {
        "text": f"I'm not quite sure I follow, but I'm eager to help! 🧐\n\nYou mentioned something about '{user_message[:50]}'. Would you like me to:\n1. Find a **better deal**?\n2. Help you **cancel** something?\n3. **Search** for a new service?",
        "actions": [
            {"label": "💰 Better Deal", "action": "find_better_deal"},
            {"label": "❌ Cancel Service", "action": "cancel_service"},
            {"label": "🔍 New Search", "action": "search"}
        ]
    }


def open_browser():
    """Open the chatbot in the default browser."""
    time.sleep(2)  # Give server time to start
    webbrowser.open("http://localhost:5000")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("🤖 Starting Chatbot Server...")
    print("📍 Open http://localhost:5000 in your browser")

    # Open browser automatically
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    app.run(debug=True, use_reloader=False, host="localhost", port=5000)
