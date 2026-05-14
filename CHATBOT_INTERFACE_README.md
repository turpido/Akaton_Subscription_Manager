# 💰 Subscription Manager - Chatbot Interface & Background Agent

A complete system that runs in the background of your PC and intelligently manages your subscriptions with AI-powered recommendations and a beautiful chatbot interface.

## 🎯 Features

### 🤖 **Chatbot Interface**
- Beautiful web-based chat interface (http://localhost:5000)
- Ask questions naturally: "Find me a VPN", "Cancel Netflix", "Show me cheaper alternatives"
- Direct links to services and cancellation pages
- Personalized recommendations based on your subscriptions

### 🔔 **Background Notifications**
- Windows notifications for important events
- 💰 Better deal alerts when cheaper alternatives are found
- ⏰ Subscription expiration reminders
- 📊 Weekly spending reports
- ❌ Cancellation opportunity alerts

### 🔍 **Smart Monitoring**
- Continuously monitors your subscriptions
- Detects expensive or underused services
- Finds cheaper alternatives automatically
- Tracks spending patterns
- Weekly and daily analysis

### 🌐 **Web Search Integration**
- Search for new services and best deals
- Compare pricing across providers
- Get curated recommendations
- Direct links to services and pricing

---

## ⚡ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the System

**Option A: Interactive Menu**
```bash
python interface.py
```
Then choose option 3 (Start both services)

**Option B: Direct Command**
```bash
python interface.py start
```

**Option C: Individual Services**
```bash
# Background agent only (monitoring & notifications)
python interface.py background

# Chatbot only (web interface)
python interface.py chat
```

### 3. Access the Chatbot

Open your browser to: **http://localhost:5000**

---

## 🎮 How to Use

### Chatbot Examples

**Search for Services:**
```
"Find me a VPN"
→ Shows best VPN options with pricing

"What password managers are there?"
→ Lists top password managers with comparisons

"Show me cloud storage options"
→ Displays storage services with features
```

**Cancel Services:**
```
"How do I cancel Netflix?"
→ Provides direct cancellation link and instructions

"Cancel Spotify"
→ Shows cancellation process and alternatives
```

**Find Better Deals:**
```
"Is there a cheaper alternative to ChatGPT Plus?"
→ Shows alternatives and potential savings

"I'm spending too much on subscriptions"
→ Analyzes spending and suggests optimizations
```

**Ask for Recommendations:**
```
"What's the best email provider?"
→ Lists top email services

"I need a productivity tool"
→ Recommends Notion, Obsidian, Trello, etc.
```

### Notification Examples

When running the background agent:

- **New Better Deal** 🎯
  ```
  Title: Better Deal Found!
  Message: Save $10.67/month! ChatGPT Plus → Claude
  Click to learn more
  ```

- **Subscription Expiring** ⏰
  ```
  Title: Netflix expires in 3 days
  Message: Click to discuss renewal or cancellation
  ```

- **High Spending Alert** 💸
  ```
  Title: High Subscription Spending
  Message: You're spending $247.33/month...
  ```

---

## 📁 System Structure

```
├── interface.py                    # Main entry point
├── background_agent.py             # Background monitoring service
├── chatbot_ui.py                   # Chatbot web server (Flask)
├── notification_handler.py         # Windows notifications
├── web_search_engine.py            # Service recommendations
├── templates/
│   └── chatbot.html                # Chatbot UI (HTML/CSS/JS)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🔧 Configuration

### Adjust Monitoring Frequency

Edit `background_agent.py`:

```python
# Change check interval (in minutes)
monitor = SubscriptionMonitor(check_interval_minutes=30)  # Check every 30 min
```

### Customize Notifications

Edit `notification_handler.py`:

```python
# Customize notification messages, duration, etc.
self.notifier.notify_better_deal(
    current_service="Netflix",
    better_service="Disney+",
    savings="$5/month"
)
```

### Add More Services

Edit `web_search_engine.py` `SERVICE_RECOMMENDATIONS`:

```python
SERVICE_RECOMMENDATIONS = {
    "your_category": [
        {
            "name": "Service Name",
            "url": "https://example.com",
            "price": "$X.XX/month",
            "features": "Description..."
        },
        # ... more services
    ]
}
```

---

## 📊 Services Database

The system comes with recommendations for:

- **Email:** Gmail, Proton Mail, Outlook
- **VPN:** NordVPN, Surfshark, ProtonVPN
- **Cloud Storage:** Google Drive, OneDrive, Dropbox
- **Password Managers:** Bitwarden, 1Password, LastPass
- **Productivity:** Notion, Obsidian, Trello
- **Code Editors:** VS Code, JetBrains IDEs
- **AI Chat:** ChatGPT Plus, Claude, Gemini

---

## 💻 Running as Windows Service (Advanced)

To run the background agent as a Windows Service that starts automatically:

```bash
# Install NSSM (Non-Sucking Service Manager)
choco install nssm

# Install service
nssm install SubscriptionManager "C:\path\to\python.exe" "C:\path\to\background_agent.py"

# Start service
nssm start SubscriptionManager

# Stop service
nssm stop SubscriptionManager

# Remove service
nssm remove SubscriptionManager
```

---

## 🔌 API Endpoints

### Chat Endpoint
```
POST /api/chat
{
  "message": "Find me a VPN"
}

Response:
{
  "text": "I found 3 great VPN options...",
  "services": [...],
  "actions": [...]
}
```

### Initialize Cancellation
```
POST /api/init-cancellation
{
  "service_name": "Netflix",
  "reason": "Too expensive"
}
```

### Search Services
```
POST /api/search-service
{
  "query": "cloud storage"
}
```

---

## 🐛 Troubleshooting

### Notifications Not Showing
```python
# Check if win10toast is installed
pip install win10toast

# Or test notifications manually:
from notification_handler import NotificationHandler
NotificationHandler.simple_notification(
    "Test", 
    "This is a test notification"
)
```

### Chatbot Won't Open
```bash
# Check if Flask is installed
pip install Flask

# Try direct URL:
http://localhost:5000

# Check if port 5000 is in use:
netstat -ano | findstr :5000
```

### Database Connection Error
```bash
# Ensure Azure credentials are in .env:
AZURE_SQL_SERVER=your-server.database.windows.net
AZURE_SQL_DATABASE=your-database
AZURE_SQL_USERNAME=admin
AZURE_SQL_PASSWORD=your-password
```

---

## 📝 Logging

Logs are printed to console with timestamp and level:

```
2026-05-15 10:30:45 [INFO] background_agent – ✅ Subscription Monitor started
2026-05-15 10:30:45 [INFO] notification_handler – ✓ Gmail API authenticated successfully
2026-05-15 10:31:00 [INFO] chatbot_ui – 🤖 Starting Chatbot Server...
```

---

## 🚀 Advanced Features

### Scheduled Tasks

The system automatically runs:

- **Every Hour:** Check all subscriptions for better deals
- **Every Day at 9 AM:** Analyze spending patterns
- **Every Monday at 8 AM:** Generate weekly report

### Conversation History

The chatbot maintains conversation history and context:
- Remembers which service you're discussing
- Can reference previous messages
- Provides contextual recommendations

### Smart Recommendations

Based on your current subscriptions:
- Finds cheaper alternatives
- Detects spending patterns
- Suggests consolidation opportunities
- Warns about unused services

---

## 🔐 Security & Privacy

✅ **Safe and Secure:**
- Gmail data is read-only (no modifications)
- Notifications stay on your local PC
- No data sent to external servers
- Database connection is encrypted
- Token stored locally (never uploaded)

⚠️ **Keep Secure:**
- Don't share `.env` file with credentials
- Keep `gmail_token.pickle` private
- Don't commit sensitive files to git

---

## 📚 Example Workflows

### Workflow 1: Reduce Spending
1. Background agent detects you're spending $300+/month
2. Notification appears: "High Subscription Spending"
3. You click notification → Chatbot opens
4. Ask: "How can I save money?"
5. Chatbot shows cheaper alternatives for each service
6. One-click links to switch services

### Workflow 2: Find Better Deal
1. Background agent finds cheaper alternative to ChatGPT Plus
2. Notification: "Better Deal Found! Save $10/month"
3. You click → Chatbot opens with comparison
4. View features side-by-side
5. Choose to switch with one click
6. Get link to cancellation process for old service

### Workflow 3: Search New Service
1. You open chatbot manually
2. Ask: "What's the best project management tool?"
3. Chatbot shows Notion, Asana, Monday.com, etc.
4. Click "Learn More" on Notion
5. Opens pricing page in browser
6. Add to your subscriptions

---

## 🤝 Contributing

To add more features:
1. Edit `web_search_engine.py` for more services
2. Edit `background_agent.py` for new checks
3. Edit `chatbot_ui.py` for new chat features
4. Edit `templates/chatbot.html` for UI changes

---

## 📞 Support

**Not working?**
1. Check logs for error messages
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Try restarting all services
4. Check `.env` file has correct credentials

**Questions?**
- Check the README files in each module
- Review code comments
- Test with the examples above

---

## 🎉 Enjoy!

Your subscription manager is now running with:
- ✅ Automatic background monitoring
- ✅ Smart cost optimization alerts
- ✅ Beautiful chatbot interface
- ✅ Web search integration
- ✅ Windows notifications

**Save money and never miss a better deal again!** 💰
