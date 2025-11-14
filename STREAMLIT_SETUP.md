# 🎨 Streamlit Setup Guide

Welcome to the Git-Helper web interface! This guide helps you set up and run the interactive Streamlit dashboard.

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## ⚡ Quick Start (2 minutes)

### Option 1: Automatic Setup
```bash
# Install all dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_app.py
```

The app will open automatically at: `http://localhost:8501`

### Option 2: Docker Setup
```bash
# Build Docker image
docker build -t git-helper-ui .

# Run the container
docker run -p 8501:8501 git-helper-ui
```

Then visit: `http://localhost:8501`

---

## 🗺️ App Navigation

### 🏠 Home Page
- **What it is**: Overview of Git-Helper
- **What you'll see**: Features, benefits, and call-to-action buttons
- **Good for**: Understanding the project at a glance

### 🚀 Quick Setup
- **What it is**: Step-by-step installation guide
- **What you'll see**: File downloads, installation instructions, checklist
- **Good for**: Setting up Git-Helper in your repository

### 📖 How It Works
- **What it is**: Deep dive into Git-Helper architecture
- **What you'll see**: Pipeline diagram, analysis details, generated files
- **Good for**: Understanding how Git-Helper analyzes your repo

### ❓ FAQ
- **What it is**: Common questions and answers
- **What you'll see**: Expandable Q&A sections
- **Good for**: Quick answers to setup questions

### ⚙️ Advanced
- **What it is**: Configuration reference
- **What you'll see**: Environment variables, custom configs, secrets setup
- **Good for**: Fine-tuning Git-Helper for your needs

---

## 🔧 Configuration

### Edit App Settings
The Streamlit app can be customized via `~/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#f0f2f6"
secondaryBackgroundColor = "#e0e4e8"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = false
toolbarMode = "minimal"
```

### Custom Environment Variables
Create a `.env` file in the root directory:

```bash
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_SERVER_HEADLESS=true
```

---

## 📊 Using the App

### Downloading Files
1. Navigate to **Quick Setup** page
2. Click on file download buttons
3. Files are downloaded to your `~/Downloads/` folder
4. Copy them to your repository:
   - `.env.example` → Repository root
   - `daily-analysis.yml` → `.github/workflows/`

### Checking Status
- The app shows current Git-Helper version
- Check GitHub repository link for latest updates
- All features work offline (no internet required)

---

## 🐛 Troubleshooting

### App Won't Start
```bash
# Clear Streamlit cache
streamlit cache clear

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run with verbose output
streamlit run streamlit_app.py --logger.level=debug
```

### Missing Dependencies
```bash
# Ensure all requirements are installed
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.11 or higher
```

### Port Already in Use
```bash
# Use a different port
streamlit run streamlit_app.py --server.port 8502
```

### Browser Won't Open
```bash
# Run in headless mode and get the URL
streamlit run streamlit_app.py --server.headless true

# Manually visit the URL shown in terminal (usually http://localhost:8501)
```

---

## 🚀 Deployment

### Deploy on Streamlit Cloud (Free)
1. Fork this repository on GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app" and select your fork
5. Point to `streamlit_app.py`
6. Deploy!

### Deploy on Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run streamlit_app.py" > Procfile

# Create Heroku app and deploy
heroku create git-helper-ui
git push heroku main
```

### Deploy on Railway
1. Connect your GitHub repository to [Railway](https://railway.app)
2. Set start command: `streamlit run streamlit_app.py`
3. Deploy!

---

## 📝 Features Overview

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Home** | Project overview | Learn what Git-Helper does |
| **Quick Setup** | Guided installation | New users setting up the tool |
| **How It Works** | Technical architecture | Understanding the pipeline |
| **FAQ** | Q&A section | Quick answers |
| **Advanced** | Configuration options | Power users customizing setup |

---

## 🔗 Integration with Git-Helper

The Streamlit app complements the core Git-Helper tool:

- **Git-Helper Scripts** → Analyze your repository
- **Streamlit App** → Guide users through setup
- **GitHub Actions** → Automate daily analysis
- **CodeRabbit** → Review code on pull requests

---

## 💡 Tips & Best Practices

### For Users
- Start with the **Quick Setup** page for guided installation
- Bookmark the FAQ page for quick reference
- Use the **Advanced** page only if customization is needed

### For Developers
- The app is fully responsive and mobile-friendly
- All text content is easy to update in `streamlit_app.py`
- Customize colors in the CSS styling section
- Add new pages by creating new `.py` files in `pages/` folder

---

## 🤝 Contributing

Found an issue with the Streamlit app?
1. Check the [GitHub Issues](https://github.com/iampreetdave-max/Git-Helper/issues)
2. Create a new issue if not reported
3. Submit a pull request with improvements

---

## 📞 Support

- **Documentation**: Check README.md for general Git-Helper docs
- **Issues**: Report problems on GitHub
- **Discussions**: Ask questions in GitHub Discussions

---

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

Made with ❤️ by the Git-Helper team
