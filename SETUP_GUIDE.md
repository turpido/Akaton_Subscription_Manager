# 🚀 Subscription Manager - Complete Setup & Usage Guide

## What You Just Got

You now have a complete AI-powered subscription management system with:

✅ **Background Agent** - Runs silently and monitors your subscriptions
✅ **Smart Notifications** - Alerts you about better deals and expiring subscriptions
✅ **Chatbot Interface** - Beautiful web chat to discuss subscriptions with AI
✅ **Web Search** - Find best deals and service alternatives
✅ **Gmail Integration** - Automatically reads your invoice emails

---

## ⚡ 5-Minute Quick Start

### Step 1: Install Dependencies (First Time Only)

```bash
pip install -r requirements.txt
```

### Step 2: Start the System

**Easy way - Interactive menu:**
```bash
python quick_start.py
```

Then choose option 1: "Start full system"

**Or direct command:**
```bash
python interface.py start
```

### Step 3: Use the Chatbot

Open your browser to: **http://localhost:5000**

That's it! You're ready to go. 🎉

---

## 🤖 Using the Chatbot

The chatbot understands natural language. Try these:

### Search for Services
```
"Find me a VPN"
"Show me password managers"
"What cloud storage options are there?"
"Best email providers"
```

### Cancel Services
```
"How do I cancel Netflix?"
"Cancel Spotify"
"Unsubscribe from ChatGPT Plus"
```

### Find Better Deals
```
"Is there a cheaper alternative to $20/month?"
"Show me cheaper options"
"I want to save money"
"Compare these two services"
```

### Explore
```
"What's the best project management tool?"
"Recommend a VPN"
"Find me a password manager"
```

---

## 🔔 Background Notifications

When the background agent is running, you'll see notifications on your screen like:

### 💰 Better Deal Found
```
Title: Better Deal Found!
Message: Save $10/month! ChatGPT Plus → Claude
Click to open chatbot and learn more
```

### ⏰ Subscription Expiring
```
Title: Netflix expires in 3 days
Message: Click to discuss renewal or cancellation
```

### 📊 Weekly Report
```
Title: Weekly Subscription Report
Message: You have 12 active subscriptions
Total monthly: $247.33
```

---

## 📁 System Components

### **interface.py** - Main Entry Point
```bash
python interface.py start       # Start everything
python interface.py background  # Background agent only
python interface.py chat        # Chatbot only
```

### **quick_start.py** - Easy Setup
```bash
python quick_start.py  # Interactive menu with demos
```

### **background_agent.py** - Background Service
- Monitors subscriptions
- Finds better deals
- Sends notifications
- Generates reports
- Runs automatically at set intervals

### **chatbot_ui.py** - Web Interface
- Beautiful chat interface
- HTTP server on localhost:5000
- React to user questions
- Provide service recommendations
- Link directly to services

### **notification_handler.py** - Windows Alerts
- Sends desktop notifications
- Click-through to chatbot
- Customizable messages

### **web_search_engine.py** - Service Database
- Database of popular services
- Pricing and features
- Finds cheaper alternatives
- Recommendations engine

---

## 🎮 Example Workflows

### Workflow 1: Find a VPN

1. Open chatbot (http://localhost:5000)
2. Type: "Find me a VPN"
3. Chatbot shows: NordVPN, Surfshark, ProtonVPN
4. Click on one to view pricing
5. Click "Open Link" to visit their website
6. Add to your subscriptions

### Workflow 2: Cancel Netflix

1. Get notification: "Better Deal Found! Hulu is cheaper"
2. Click notification → Chatbot opens
3. Ask: "How do I cancel Netflix?"
4. Chatbot provides:
   - Direct cancellation link
   - Step-by-step instructions
   - Alternative services
5. Click link to cancel

### Workflow 3: Analyze Spending

1. Background agent runs automatically
2. At 9 AM daily: Spending analysis
3. At 8 AM Monday: Weekly report
4. If spending > $100/month: Notification alert
5. Click to open chatbot and discuss optimization

---

## ⚙️ Configuration

### Change Check Frequency

Edit `background_agent.py`:

```python
# Check subscriptions every 30 minutes instead of 60
monitor = SubscriptionMonitor(check_interval_minutes=30)
```

### Add More Services

Edit `web_search_engine.py`, add to `SERVICE_RECOMMENDATIONS`:

```python
"your_category": [
    {
        "name": "Service Name",
        "url": "https://service.com",
        "price": "$9.99/mo",
        "features": "Description of features"
    },
]
```

### Customize Notifications

Edit `notification_handler.py`:

```python
def notify_custom(self):
    self.toaster.show_toast(
        title="Your Custom Title",
        msg="Your custom message",
        duration=10
    )
```

---

## 📱 Mobile Support

The chatbot works on mobile! Open `http://your-pc-ip:5000` from your phone.

To find your PC IP:
```bash
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

Then on phone browser:
```
http://192.168.1.100:5000
```

---

## 🔌 Integration with Other Tools

### Add to Your Windows Startup

Create a batch file `start_subscription_manager.bat`:

```batch
@echo off
cd C:\Users\YourUsername\Akaton_Subscription_Manager
python interface.py start
```

Then add to Windows Startup folder:
- Windows key + R
- Type: `shell:startup`
- Copy batch file to this folder

### Use with Other Applications

The system provides HTTP endpoints you can use:

```
POST http://localhost:5000/api/chat
{
  "message": "Find me a VPN"
}

POST http://localhost:5000/api/search-service
{
  "query": "cloud storage"
}
```

---

## 🐛 Troubleshooting

### Chatbot Won't Open (http://localhost:5000)

**Problem:** Browser shows "Cannot connect"

**Solutions:**
1. Make sure Flask is installed: `pip install Flask`
2. Check if port 5000 is in use:
   ```bash
   netstat -ano | findstr :5000
   ```
3. Kill the process using port 5000:
   ```bash
   taskkill /PID <PID> /F
   ```
4. Start fresh: `python interface.py chat`

### Notifications Not Showing

**Problem:** No Windows notifications appear

**Solutions:**
1. Install win10toast: `pip install win10toast`
2. Check Windows notification settings
3. Run as administrator
4. Test manually:
   ```python
   from notification_handler import NotificationHandler
   NotificationHandler.simple_notification("Test", "Message")
   ```

### Background Agent Won't Start

**Problem:** Background monitoring not running

**Solutions:**
1. Check logs for errors
2. Ensure APScheduler is installed: `pip install APScheduler`
3. Try: `python background_agent.py` directly
4. Check if another instance is already running

---

## 📊 Understanding the Data

### Subscription Fields

- **Service Name:** E.g., "Netflix", "ChatGPT Plus"
- **Amount:** E.g., "$19.99/month"
- **Billing Date:** When next charge occurs
- **Billing Cycle:** monthly, yearly, quarterly
- **Email From:** Sender of billing emails
- **Status:** active, cancelled, paused

### Reports Generated

- **Daily Analysis:** Spending patterns and trends
- **Weekly Report:** All active subscriptions and total cost
- **Better Deal Alert:** When cheaper alternative found
- **Expiration Alert:** When subscription expires in 3 days

---

## 🔐 Security & Privacy

✅ **What's Safe:**
- Notifications stay on your PC
- Data isn't sent anywhere
- Gmail read-only access
- Local database only

⚠️ **Keep Secure:**
- Don't share `.env` file
- Keep `gmail_token.pickle` private
- Don't commit credentials to git
- Use strong passwords

---

## 📞 Common Questions

**Q: Does this cost anything?**
A: No! It's completely free and open source.

**Q: Does it send my data to the cloud?**
A: No, everything runs locally on your PC.

**Q: Can I use it on multiple computers?**
A: Yes, install and run on each machine separately.

**Q: Will it work if my PC is off?**
A: No, it needs to be running. Consider using Windows Task Scheduler for automatic startup.

**Q: Can I customize the notifications?**
A: Yes, edit `notification_handler.py` and customize messages, timing, etc.

**Q: How often does it check subscriptions?**
A: By default every 60 minutes, configurable in `background_agent.py`

---

## 🎓 Learning More

### Explore the Code

1. **interface.py** - Main orchestration
2. **background_agent.py** - Monitoring logic
3. **chatbot_ui.py** - Flask web server
4. **web_search_engine.py** - Service recommendations
5. **notification_handler.py** - Windows notifications

### Modify and Extend

- Add more services to recommendations
- Create custom notification types
- Build API endpoints for other tools
- Create mobile app that connects to API
- Add machine learning for better recommendations

---

## 🚀 Next Steps

1. **Start the system:** `python quick_start.py`
2. **Test the chatbot:** Open http://localhost:5000
3. **Try a few queries:** Ask for services, cancellations, deals
4. **Let it monitor:** Background agent checks subscriptions
5. **Get notifications:** React to alerts about better deals
6. **Save money:** Switch to cheaper services with chatbot links

---

## 💡 Pro Tips

1. **Daily Check:** Ask chatbot about your spending every morning
2. **Monthly Review:** Let the system analyze a month of subscriptions
3. **Add to Startup:** Run automatically when PC starts
4. **Set Reminders:** Use notifications to remember renewal dates
5. **Compare Services:** Use chatbot to compare 2-3 options before switching

---

## 🎉 You're All Set!

Your subscription manager is ready to save you money and help optimize your spending!

**Start with:**
```bash
python quick_start.py
```

Then choose option 1 to start the full system.

**Questions?** Check the detailed documentation in:
- `CHATBOT_INTERFACE_README.md`
- `GMAIL_INVOICE_READER_README.md`
- `GMAIL_AGENT_USAGE.md`

**Happy saving!** 💰
