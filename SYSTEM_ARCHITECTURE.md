# System Architecture Diagram

## How It All Works Together

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SUBSCRIPTION MANAGER SYSTEM                      │
└─────────────────────────────────────────────────────────────────────┘

                          ┌──────────────────┐
                          │  interface.py    │
                          │  (Entry Point)   │
                          └────────┬─────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
                ▼                  ▼                  ▼
        ┌─────────────────┐ ┌──────────────┐ ┌──────────────────┐
        │ background_     │ │  chatbot_    │ │   notification_  │
        │ agent.py        │ │  ui.py       │ │   handler.py     │
        │                 │ │ (Flask)      │ │                  │
        │ • Monitor       │ │              │ │ • Windows        │
        │ • Check deals   │ │ • Web chat   │ │   notifications  │
        │ • Schedules     │ │ • Port 5000  │ │ • Alerts user    │
        └────────┬────────┘ └──────┬───────┘ └────────┬─────────┘
                 │                 │                  │
                 │                 │                  │
                 └────────────┬────┴──────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │ web_search_       │
                    │ engine.py         │
                    │                   │
                    │ • Service DB      │
                    │ • Recommendations │
                    │ • Pricing info    │
                    │ • Better deals    │
                    └────────┬──────────┘
                             │
                    ┌────────▼──────────┐
                    │  azure_db_        │
                    │  manager.py       │
                    │                   │
                    │ • Subscriptions   │
                    │ • Usage history   │
                    │ • Billing info    │
                    └───────────────────┘
```

---

## User Flow Diagram

```
┌──────────────┐
│ User starts  │
│ system       │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────┐
│ Background Agent runs             │
│ • Monitors subscriptions          │
│ • Checks for better deals         │
│ • Sends notifications             │
└──────┬───────────────────────────┘
       │
       ├─ Better deal found?
       │     │
       │     ▼
       │  ┌─────────────────────┐
       │  │ Send notification:  │
       │  │ "Save $10/month!"   │
       │  └────────┬────────────┘
       │           │
       │           ▼
       │  ┌──────────────────────┐
       │  │ User clicks alert    │
       │  └────────┬─────────────┘
       │           │
       │           ▼
       │  ┌──────────────────────┐
       │  │ Chatbot opens:       │
       │  │ http://localhost:5000│
       │  └────────┬─────────────┘
       │           │
       │           ▼
       │  ┌──────────────────────────┐
       │  │ Chat about subscription: │
       │  │ • Why should I switch?   │
       │  │ • How do I cancel?       │
       │  │ • Show alternatives      │
       │  └────────┬─────────────────┘
       │           │
       │           ▼
       │  ┌──────────────────────┐
       │  │ Get direct links:    │
       │  │ • Cancel link        │
       │  │ • New service site   │
       │  │ • Comparison         │
       │  └────────┬─────────────┘
       │           │
       │           ▼
       │  ┌──────────────────────┐
       │  │ Save money!          │
       │  │ 💰💰💰              │
       │  └──────────────────────┘
       │
       └─ No better deal?
            │
            ▼
         Check again
         in 1 hour
```

---

## Daily Timeline

```
MONDAY - FRIDAY (Weekday)
├─ 8:00 AM
│  └─ Spending analysis
│     └─ Check all subscriptions
│        └─ Generate daily report
├─ 9:00 AM - 5:00 PM
│  └─ Continuous monitoring
│     ├─ Every hour: Check deals
│     ├─ If better deal found: NOTIFY
│     └─ If expiring soon: NOTIFY
└─ Background runs 24/7

SATURDAY
├─ Same as weekday
└─ Monthly spending review

SUNDAY - MONDAY
├─ 8:00 AM (Monday)
│  └─ Weekly report generated
│     ├─ All active subscriptions
│     ├─ Total monthly cost
│     ├─ Savings opportunities
│     └─ NOTIFY user
```

---

## Data Flow

```
Gmail Emails
    │
    ▼
┌─────────────────────┐
│ gmail_invoice_      │
│ reader.py           │
│                     │
│ • Read emails       │
│ • Extract invoices  │
│ • Find amounts      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────┐
│ gmail_to_db_sync.py     │
│                         │
│ • Parse invoice data    │
│ • Extract service name  │
│ • Calculate billing     │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Azure Database              │
│                             │
│ subscriptions table:        │
│ ├─ service_name             │
│ ├─ amount                   │
│ ├─ billing_date             │
│ ├─ billing_cycle            │
│ └─ email_from               │
└──────────┬──────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ background_agent.py          │
│                              │
│ Analyzes data:               │
│ ├─ Find alternatives         │
│ ├─ Calculate savings         │
│ ├─ Generate reports          │
│ └─ Create notifications      │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ notification_handler.py      │
│                              │
│ Sends to Windows:            │
│ • Notification popups        │
│ • Action Center              │
│ • System tray                │
└──────────────────────────────┘
```

---

## Service Recommendation Engine

```
User asks: "Find me a VPN"
    │
    ▼
┌─────────────────────────────────┐
│ chatbot_ui.py receives request  │
└────────────────┬────────────────┘
                 │
                 ▼
┌───────────────────────────────────────┐
│ web_search_engine.py                  │
│                                       │
│ SERVICE_RECOMMENDATIONS = {           │
│   "vpn": [                            │
│     {                                 │
│       "name": "NordVPN",              │
│       "price": "$3.99/mo",            │
│       "url": "https://...",           │
│       "features": "..."               │
│     },                                │
│     {                                 │
│       "name": "Surfshark",            │
│       "price": "$2.49/mo", ← CHEAPEST │
│       "url": "https://...",           │
│       "features": "..."               │
│     },                                │
│     ...                               │
│   ]                                   │
│ }                                     │
└────────────────┬────────────────────┘
                 │
                 ▼
┌──────────────────────────────────┐
│ Return to chatbot:               │
│ "Found 3 VPN options:            │
│  1. NordVPN - $3.99/mo           │
│  2. Surfshark - $2.49/mo         │
│  3. ProtonVPN - free-$10/mo      │
│                                  │
│  Best value: Surfshark 🎯        │
│  Try it →"                       │
└──────────────────────────────────┘
```

---

## Notification Flow

```
Background Agent detects better deal:
├─ ChatGPT Plus ($20/mo) vs Claude (free)
├─ Savings: $20/month
│
▼
notification_handler.py
├─ Creates notification
├─ Title: "Better Deal Found! 🎯"
├─ Message: "Save $20/month! ChatGPT Plus → Claude"
├─ Duration: 10 seconds
│
▼
Windows Notification System
├─ Shows popup on screen
├─ Adds to Action Center
│
▼
User clicks notification
│
▼
Chatbot opens automatically
├─ URL: http://localhost:5000
├─ Pre-loaded with:
│  ├─ Current service: ChatGPT Plus
│  ├─ Better option: Claude
│  └─ Savings: $20/month
│
▼
Chat interface shows:
├─ "Why should I switch?"
├─ "How do I cancel?"
├─ "Compare features"
│
User clicks links
│
▼
Get direct links to:
├─ Claude website
├─ ChatGPT cancellation page
├─ Feature comparison
```

---

## System Dependencies

```
┌─ Core
│  ├─ Python 3.8+
│  ├─ flask (web server)
│  ├─ APScheduler (background tasks)
│  └─ requests (HTTP client)
│
├─ Database
│  ├─ pyodbc (SQL Server driver)
│  └─ azure_db_manager (connection)
│
├─ Notifications
│  ├─ win10toast (Windows alerts)
│  └─ Python 3.8+ built-in subprocess
│
├─ Gmail Integration
│  ├─ google-auth-oauthlib (OAuth)
│  ├─ google-api-python-client (Gmail API)
│  └─ google-auth-httplib2 (HTTP)
│
└─ Web Scraping (optional)
   └─ beautifulsoup4 (HTML parsing)
```

---

## How Better Deal Detection Works

```
Loop every hour:
│
├─ Get all subscriptions from database
│  ├─ Netflix: $15.99/month
│  ├─ Spotify: $11.99/month
│  └─ ChatGPT Plus: $20/month
│
├─ For each subscription:
│  │
│  ├─ Find similar services
│  │  └─ ChatGPT Plus → Check Claude, Gemini, etc.
│  │
│  ├─ Compare prices
│  │  ├─ ChatGPT: $20.00
│  │  ├─ Claude: $0 (free tier) ✅ CHEAPER
│  │  └─ Gemini: $20.00
│  │
│  ├─ Calculate savings
│  │  └─ $20.00 - $0.00 = $20.00/month
│  │
│  └─ If savings > threshold:
│     └─ SEND NOTIFICATION
│
└─ Repeat every hour
   (or as configured)
```

---

## Context Management in Chat

```
Conversation:

User: "Cancel Netflix"
│
├─ Set context:
│  ├─ service = "Netflix"
│  ├─ reason = "Cancellation"
│  └─ mode = "cancellation"
│
▼ Bot replies with cancellation options

User: "How much would I save?"
│
├─ Remember context:
│  ├─ service = "Netflix" ✓ (still)
│  └─ Find alternatives to Netflix
│
├─ Search: cheaper alternatives to Netflix
│  ├─ Disney+ ($7.99)
│  ├─ Hulu ($7.99)
│  └─ Max ($16)
│
▼ Bot replies: "Switch to Disney+, save $8/month"

User: "Get me the link"
│
├─ Remember context:
│  ├─ service = "Netflix" ✓
│  ├─ alternative = "Disney+" ✓
│  └─ action = "get_link"
│
▼ Bot provides both Netflix cancellation link
  AND Disney+ signup link
```

This shows how the system remembers context throughout the conversation.
