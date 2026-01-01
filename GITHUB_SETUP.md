# GitHub Integration Setup Guide

## Prerequisites
1. **Install Git**: Download and install from https://git-scm.com/download/win
   - During installation, choose "Use Git from the Windows Command Prompt"
   - Complete the installation and restart your terminal/VS Code

2. **Create GitHub Account**: If you don't have one, create it at https://github.com

3. **Set up SSH Key (Recommended)**:
   ```bash
   ssh-keygen -t ed25519 -C "your-email@example.com"
   ```
   - Save the key in the default location
   - Add the public key (`~/.ssh/id_ed25519.pub`) to GitHub Settings > SSH Keys

## Step 1: Initialize Git Repository
After installing Git, run:
```bash
cd c:\Users\Sai Mukesh\Downloads\aleph_distillation_simplified_v2
git init
```

## Step 2: Configure Git
```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

## Step 3: Add Files and Create Initial Commit
```bash
git add .
git commit -m "Initial commit: Aleph distillation simulation project"
```

## Step 4: Create Repository on GitHub
1. Go to https://github.com/new
2. Create a new repository named `aleph_distillation_simplified_v2`
3. Choose Public or Private based on your preference
4. Do NOT initialize with README, .gitignore, or license (we already have these)

## Step 5: Add Remote Repository
After creating the GitHub repository, run:
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aleph_distillation_simplified_v2.git
git push -u origin main
```

Or if using SSH:
```bash
git remote add origin git@github.com:YOUR_USERNAME/aleph_distillation_simplified_v2.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 6: Verify Integration
```bash
git remote -v
```

Should show:
```
origin  https://github.com/YOUR_USERNAME/aleph_distillation_simplified_v2.git (fetch)
origin  https://github.com/YOUR_USERNAME/aleph_USERNAME_aleph_distillation_simplified_v2.git (push)
```

## Future Commits
```bash
git add .
git commit -m "Your commit message"
git push
```

## Notes
- The `.gitignore` file has been created to exclude:
  - Python cache files (`__pycache__`, `.pyc`)
  - Virtual environments
  - IDE settings
  - Output files (CSV, JSON)
  - Jupyter notebooks checkpoints
  
This prevents these files from being tracked in version control.
