# How to Add Gemini API Key to Streamlit Secrets

## 🔐 Two Methods: Local Development & Streamlit Cloud

---

## Method 1: Local Development (For Testing)

### Step 1: Create `.streamlit/secrets.toml` file

1. **Create the directory** (if it doesn't exist):
   ```bash
   mkdir -p .streamlit
   ```

2. **Create the secrets file**:
   ```bash
   touch .streamlit/secrets.toml
   ```

3. **Add your API key** to `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "AIzaSyAHgKT76yU7qKQ76-uCxDdR-0YcStFhs0k"
   ```

### Step 2: Update .gitignore

Make sure `.streamlit/secrets.toml` is in your `.gitignore` so you don't commit it:

```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

### Step 3: Test

Run your app and the API key will be automatically loaded from secrets!

```bash
streamlit run main_app.py
```

---

## Method 2: Streamlit Cloud (For Deployment)

### Step 1: Go to Streamlit Cloud Dashboard

1. Visit: https://share.streamlit.io
2. Sign in with your GitHub account
3. Find your AQUASense app

### Step 2: Open App Settings

1. Click on your app
2. Click the **"⋮" (three dots)** menu in the top right
3. Select **"Settings"**

### Step 3: Add Secret

1. Scroll down to the **"Secrets"** section
2. Click **"Edit secrets"** or **"Add secret"**
3. You'll see a text editor with TOML format

### Step 4: Enter Your API Key

Add this to the secrets file:

```toml
GEMINI_API_KEY = "AIzaSyAHgKT76yU7qKQ76-uCxDdR-0YcStFhs0k"
```

**Full example:**
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "AIzaSyAHgKT76yU7qKQ76-uCxDdR-0YcStFhs0k"
```

### Step 5: Save

1. Click **"Save"**
2. Your app will automatically redeploy with the new secret

---

## ✅ Verification

After adding the secret, your app will:
- ✅ Use the API key from secrets (more secure)
- ✅ Override the hardcoded key
- ✅ Work automatically without code changes

---

## 🔒 Security Benefits

Using secrets instead of hardcoding:
- ✅ API key not visible in source code
- ✅ Can be changed without code updates
- ✅ Different keys for different environments
- ✅ Better security practices

---

## 📝 Quick Reference

### Local Development
```bash
# Create secrets file
mkdir -p .streamlit
echo 'GEMINI_API_KEY = "AIzaSyAHgKT76yU7qKQ76-uCxDdR-0YcStFhs0k"' > .streamlit/secrets.toml

# Add to .gitignore
echo ".streamlit/secrets.toml" >> .gitignore
```

### Streamlit Cloud
1. Go to: https://share.streamlit.io
2. App → Settings → Secrets
3. Add: `GEMINI_API_KEY = "AIzaSyAHgKT76yU7qKQ76-uCxDdR-0YcStFhs0k"`
4. Save

---

## 🎯 That's It!

Your API key is now securely stored and will be used automatically by the app!

