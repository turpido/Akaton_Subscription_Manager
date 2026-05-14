# Gmail Invoice Reader Agent

A simple Python agent that connects to your Gmail account and finds invoice emails automatically.

## What It Does

✅ **Reads your Gmail** using secure OAuth2 authentication
✅ **Finds invoice emails** from the last 90 days (or any time period)
✅ **Extracts key information**: sender, subject, date, amount, service name
✅ **Displays results** in an easy-to-read format

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Google Credentials
```bash
python setup_gmail_agent.py
```
This will:
- Open Google Cloud Console in your browser
- Guide you through creating OAuth credentials
- Test the Gmail connection

### Step 3: Run the Agent
```bash
python gmail_invoice_reader.py
```

**That's it!** The agent will search your Gmail for invoices and display them.

---

## Manual Setup (If Auto-Setup Fails)

### 1. Create Google Cloud Project
1. Go to [https://console.cloud.google.com](https://console.cloud.google.com)
2. Click **"Create Project"**
3. Name it `Gmail Invoice Reader`
4. Click **"Create"**

### 2. Enable Gmail API
1. In the search bar, type **"Gmail API"**
2. Click the **"Gmail API"** result
3. Click **"Enable"**

### 3. Create OAuth Credentials
1. Left sidebar → **"APIs & Services"** → **"Credentials"**
2. Click **"+ Create Credentials"** → **"OAuth 2.0 Client ID"**
3. **Configure OAuth consent screen** (if prompted):
   - User Type: **External**
   - App name: **Gmail Invoice Reader**
   - Add scope: Search for "Gmail API" and select readonly
4. Application type: **Desktop application**
5. Click **"Create"**

### 4. Download Credentials
1. In Credentials page, click the **download icon** (JSON)
2. Save as **`gmail_credentials.json`** in your project folder

### 5. Run the Agent
```bash
python gmail_invoice_reader.py
```

---

## Sample Output

```
🔍 Gmail Invoice Reader Agent
========================================
📧 Connecting to Gmail...
🔎 Searching for invoice emails...

✅ Found 3 invoice emails:

1. 📄 Invoice #1234 – Monthly Subscription
   🏢 Service: Stripe
   👤 From: billing@stripe.com
   📅 Date: Mon, 13 May 2026 10:32:00 +0000
   💰 Amount: $99.00
   📝 Preview: Thank you for using Stripe. Your invoice is attached...

2. 📄 Receipt: GitHub Copilot Subscription
   🏢 Service: GitHub
   👤 From: noreply@github.com
   📅 Date: Sun, 12 May 2026 15:22:00 +0000
   💰 Amount: $19.99
   📝 Preview: Thank you for your purchase of GitHub Copilot...

3. 📄 AWS Monthly Billing Statement
   🏢 Service: Aws
   👤 From: no-reply@aws.amazon.com
   📅 Date: Sat, 11 May 2026 08:15:00 +0000
   💰 Amount: $45.67
   📝 Preview: Your AWS account billing statement is ready...
```

---

## Customization

### Change Search Period
```python
from gmail_invoice_reader import GmailInvoiceReader

agent = GmailInvoiceReader()

# Search last 30 days
invoices = agent.find_invoices(days_back=30)

# Search last year
invoices = agent.find_invoices(days_back=365)
```

### Change Number of Results
```python
# Get up to 50 invoices
invoices = agent.find_invoices(max_results=50)
```

### Search by Specific Sender
```python
# Only from Stripe
invoices = agent.search_by_sender("billing@stripe.com")
```

---

## Security Notes

🔒 **Your data is safe:**
- Uses **read-only** Gmail access (cannot send emails)
- OAuth2 tokens are stored locally (never uploaded)
- Credentials file should be kept private

⚠️ **Important:**
- Add `gmail_credentials.json` to `.gitignore`
- Never share your OAuth tokens
- The agent only reads emails, never modifies them

---

## Troubleshooting

### "gmail_credentials.json not found"
- Run `python setup_gmail_agent.py` for guided setup
- Or follow the manual setup steps above

### "Invalid grant: Token has been revoked"
- Delete `gmail_token.pickle` file
- Run the agent again to re-authenticate

### "403 Forbidden"
- Make sure Gmail API is enabled in Google Cloud Console
- Check that OAuth consent screen is configured

### No emails found
- Try increasing `days_back` (default is 90 days)
- Check that you have invoice emails in Gmail
- Some emails might use different keywords

### Browser doesn't open for authentication
- Copy the URL from terminal and paste in browser manually
- Make sure you're logged into the correct Google account

---

## Files Overview

- **`gmail_invoice_reader.py`** – Main agent code
- **`setup_gmail_agent.py`** – Guided setup script
- **`gmail_credentials.json`** – Your OAuth credentials (download from Google)
- **`gmail_token.pickle`** – Auto-generated auth token (don't share)
- **`requirements.txt`** – Python dependencies

---

## Next Steps

After getting invoices, you can:
- **Save to database**: Use `gmail_to_db_sync.py` to store in your subscription manager
- **Add to FastAPI**: Integrate with your web API (see `GMAIL_AGENT_USAGE.md`)
- **Schedule automatic runs**: Set up daily/weekly invoice checks
- **Export to CSV**: Add export functionality for accounting

---

**Need help?** Check the troubleshooting section or run `python setup_gmail_agent.py` for guided setup.
