# 🐰 CodeRabbit Integration Guide

This guide helps you set up **CodeRabbit**, an AI-powered code reviewer that automatically reviews your pull requests.

## 🎯 What is CodeRabbit?

CodeRabbit is an intelligent code review bot that:
- 🤖 Reviews pull requests automatically using AI
- ✅ Catches bugs, security issues, and code quality problems
- 💬 Leaves detailed comments on code changes
- 🚀 Helps maintain code quality without manual effort
- 🔒 Runs entirely on GitHub (no external access to code)

## ⚡ 5-Minute Setup

### Step 1: Install CodeRabbit
1. Go to [CodeRabbit.ai](https://coderabbit.ai)
2. Click "Start with GitHub"
3. Authorize CodeRabbit to access your repositories
4. Select repositories where you want code reviews

### Step 2: Enable on Your Repository
```bash
# Files are already in your repo:
# ✅ .coderabbit.yaml - Configuration file
# ✅ .github/workflows/coderabbit-review.yml - GitHub Actions workflow
```

### Step 3: Create API Key
1. Go to your CodeRabbit dashboard
2. Create an API key
3. Add it to your repository secrets:
   - Go to `Settings → Secrets and variables → Actions`
   - Click "New repository secret"
   - Name: `CODERABBIT_API_KEY`
   - Value: (paste your CodeRabbit API key)

### Step 4: Test It!
1. Create a test pull request
2. CodeRabbit will automatically review your code
3. Check the review comments on your PR

**Done!** 🎉

---

## 📋 Configuration Guide

### .coderabbit.yaml Options

The `.coderabbit.yaml` file controls how CodeRabbit reviews your code:

#### Review Settings
```yaml
review:
  auto_review: true              # Always review PRs
  prioritize:
    - ".github/scripts/"          # Files to focus on
    - "streamlit_app.py"
  skip_files:
    - "*.md"                      # Files to skip
    - "*.json"
```

#### What to Check
```yaml
checks:
  code_quality: true              # Check code quality
  complexity: true                # Check complexity
  security: true                  # Check security issues
  documentation: true             # Check docs
  imports: true                   # Check import statements
  unused_variables: true          # Flag unused vars
  type_hints: true                # Check type annotations
```

#### Review Depth
```yaml
ai:
  model: "gpt-4"                  # AI model to use
  depth: "detailed"               # Review depth
  instructions: |                 # Custom instructions
    Focus on:
    1. Security issues
    2. Code quality
    3. Performance
```

#### File Limits
```yaml
workflow:
  max_files: 20                   # Max files per review
  timeout: 300                    # Review timeout (seconds)
  review_draft: false             # Review draft PRs?
```

---

## 🎨 Customization Examples

### Example 1: Strict Security Review
```yaml
review:
  auto_review: true

checks:
  security: true
  code_quality: true
  imports: true

ai:
  depth: "detailed"
  instructions: |
    CRITICAL: Focus on security vulnerabilities
    Check for: SQL injection, XSS, unsafe dependencies
    Severity: Report all issues, even minor ones
```

### Example 2: Lightweight Performance Review
```yaml
review:
  auto_review: true
  skip_files:
    - "*.md"
    - "*.json"
    - "tests/*"

checks:
  code_quality: true
  performance: true

workflow:
  max_files: 10
  timeout: 120
```

### Example 3: Documentation Focus
```yaml
review:
  auto_review: true

checks:
  documentation: true
  code_quality: true
  type_hints: true

ai:
  instructions: |
    Focus on:
    1. Missing docstrings
    2. Poor documentation
    3. Missing type hints
```

---

## 🔧 GitHub Actions Integration

The `.github/workflows/coderabbit-review.yml` file automates CodeRabbit reviews:

### How It Works
1. PR is opened/updated → Workflow triggers
2. Code is checked out → Files are ready
3. CodeRabbit reviews → AI analyzes code
4. Comments are posted → Feedback on PR

### Customizing the Workflow
```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]
    # Add paths to review only certain files:
    paths:
      - '.github/scripts/**'
      - 'streamlit_app.py'
      - 'requirements.txt'
```

### Running on Schedule (Optional)
```yaml
on:
  schedule:
    # Review all PRs daily
    - cron: '0 0 * * *'
  pull_request:
    types: [opened, synchronize, reopened]
```

---

## 📊 Review Quality

### What CodeRabbit Checks
| Category | Examples |
|----------|----------|
| **Security** | Vulnerabilities, unsafe patterns, secret exposure |
| **Performance** | Inefficient code, memory leaks, slow operations |
| **Quality** | Code smell, complexity, maintainability |
| **Style** | Naming conventions, formatting, structure |
| **Documentation** | Missing docs, unclear comments, type hints |
| **Testing** | Missing tests, edge cases, error handling |

### Feedback Quality
CodeRabbit provides:
- 🎯 Specific line numbers and exact issues
- 💡 Suggestions for improvement
- 📚 Links to relevant documentation
- 🔗 Examples of better patterns

---

## 🚀 Advanced Setup

### Ignore Specific Files
```yaml
review:
  skip_files:
    - "migrations/*"
    - "generated/*"
    - "vendor/*"
    - "*.min.js"
    - "*.min.css"
```

### Custom Review Rules
```yaml
ai:
  instructions: |
    For Python files:
    - Use PEP 8 style guide
    - Require docstrings for all functions
    - Suggest type hints where missing

    For test files:
    - Ensure adequate test coverage
    - Check for edge cases
    - Verify assertions are meaningful
```

### Set Severity Thresholds
```yaml
severity:
  critical:
    - security_vulnerabilities
    - data_loss_risks
    - runtime_errors

  high:
    - code_quality_issues
    - performance_problems

  medium:
    - documentation_gaps
    - style_issues
```

---

## 🐛 Troubleshooting

### CodeRabbit Not Reviewing
1. Check if bot is installed: Go to GitHub Settings → Applications
2. Verify API key: Check `Settings → Secrets → CODERABBIT_API_KEY`
3. Check workflow: `Actions` tab should show successful runs
4. Verify configuration: `.coderabbit.yaml` should exist

### Review Takes Too Long
- Reduce `max_files` in `.coderabbit.yaml`
- Set `review_draft: false` to skip draft reviews
- Increase `timeout` value if needed

### Too Many Comments
- Adjust `depth` to "normal" instead of "detailed"
- Add more files to `skip_files`
- Set custom severity thresholds

### Unwanted Insights on Certain Files
```yaml
review:
  skip_files:
    - "path/to/skip/*"
    - "specific_file.py"
```

---

## 🔐 Security Notes

### API Key Safety
- ✅ Store API key in GitHub Secrets (not in `.coderabbit.yaml`)
- ✅ Rotate keys periodically
- ❌ Never commit API keys to repository
- ❌ Never share API keys in issues/PRs

### Code Privacy
- CodeRabbit runs on GitHub infrastructure
- Code is not stored externally
- Only reviewed during PR analysis
- Deleted after review is complete

---

## 📈 Monitoring Reviews

### Check Review Status
1. Go to your PR
2. Scroll to "Conversation" tab
3. Look for CodeRabbit comments
4. Each comment is actionable

### View Workflow Logs
1. Go to `Actions` tab
2. Click `🐰 CodeRabbit Code Review` workflow
3. Click the most recent run
4. Check logs for details

### Track Issues Found
- Create labels: `coderabbit-suggested`, `coderabbit-security`, etc.
- Use GitHub Issues to track recommended changes
- Link PRs to issues for better tracking

---

## 🎓 Best Practices

### For Teams
- ✅ Use same `.coderabbit.yaml` across all repos
- ✅ Disable reviews on draft PRs to save AI credits
- ✅ Review CodeRabbit feedback weekly
- ✅ Update configuration based on team feedback

### For Individual Developers
- ✅ Fix critical and high-severity issues
- ✅ Discuss medium/low issues in team meetings
- ✅ Add custom instructions for your coding standards
- ✅ Customize for your project's specific needs

### For Projects
- ✅ Enable security reviews by default
- ✅ Focus on code quality and performance
- ✅ Require fixes for security issues
- ✅ Use as learning tool for new developers

---

## 🔗 Integration with Git-Helper

CodeRabbit works alongside Git-Helper:

| Tool | Purpose | When It Runs |
|------|---------|--------------|
| **Git-Helper** | Repository health analysis | Daily (scheduled) |
| **CodeRabbit** | PR code review | On every PR |
| **Both Together** | Complete code quality | Always monitoring |

---

## 📞 Support

### CodeRabbit Issues
- Visit [CodeRabbit Docs](https://coderabbit.ai/docs)
- Check [CodeRabbit GitHub](https://github.com/coderabbit)

### Git-Helper Issues
- Check [Git-Helper README](./README.md)
- Report issues on [GitHub Issues](https://github.com/iampreetdave-max/Git-Helper/issues)

---

## 💡 Tips

1. **Start Simple**: Use default configuration first
2. **Iterate**: Adjust based on your team's feedback
3. **Focus**: Prioritize security and critical issues
4. **Learn**: Use CodeRabbit feedback to improve coding
5. **Share**: Discuss findings with your team

---

Made with ❤️ by the Git-Helper team
