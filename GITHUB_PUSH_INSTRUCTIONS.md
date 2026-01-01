# GitHub Push Instructions

## IMPORTANT: Complete Git Installation First

Your Git installation is incomplete. Please follow ONE of these options:

### Option 1: Portable Git (Recommended - No Admin Required)
1. Download Git for Windows from: https://github.com/git-for-windows/git/releases
2. Look for `Git-2.x.x-64-bit.portable.zip` (latest version)
3. Extract to `C:\Git` or similar location
4. Run this in PowerShell to test:
   ```powershell
   C:\Git\cmd\git.exe --version
   ```

### Option 2: Standard Installer (Requires Admin)
1. Download from: https://git-scm.com/download/win
2. Run the installer as Administrator
3. Follow the wizard, selecting "Use Git from the Windows Command Prompt"
4. Restart PowerShell after installation
5. Test: `git --version`

---

## Once Git is Installed, Run These Commands:

### Step 1: Initialize Local Repository
```powershell
cd "C:\Users\Sai Mukesh\Downloads\aleph_distillation_simplified_v2"
git init
git config user.name "Your Name"
git config user.email "your-email@example.com"
```

### Step 2: Stage and Commit All Files
```powershell
git add .
git commit -m "Initial commit: Aleph distillation simulation project"
```

### Step 3: Create GitHub Repository
1. Go to: https://github.com/new
2. Create repository: `aleph_distillation_simplified_v2`
3. Choose Public or Private
4. **Do NOT** check "Initialize with README, gitignore, or license"
5. Click "Create repository"

### Step 4: Add Remote and Push
After creating the GitHub repo, copy the repository URL and run:

**For HTTPS (easier, requires password/token):**
```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aleph_distillation_simplified_v2.git
git push -u origin main
```

**For SSH (recommended, requires key setup):**
```powershell
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/aleph_distillation_simplified_v2.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 5: Verify
```powershell
git remote -v
git log --oneline
```

---

## Need SSH Setup?

Run these commands:
```powershell
ssh-keygen -t ed25519 -C "your-email@example.com"
```
- Press Enter for default location
- Set a passphrase (optional but recommended)
- Open file: `C:\Users\Sai Mukesh\.ssh\id_ed25519.pub`
- Copy the entire content
- Go to: https://github.com/settings/keys
- Click "New SSH key"
- Paste the key and save

---

## Troubleshooting

### "git: command not found"
- Git is not installed or not in PATH
- Follow Option 1 (Portable) or Option 2 (Installer) above

### "fatal: not a git repository"
- Ensure you're in the correct directory:
  ```powershell
  cd "C:\Users\Sai Mukesh\Downloads\aleph_distillation_simplified_v2"
  ```
- Check if `.git` folder exists: `ls -la`

### "Authentication failed"
- For HTTPS: Create Personal Access Token at https://github.com/settings/tokens
  - Use as password when prompted
- For SSH: Make sure SSH key is added to GitHub (see SSH Setup above)

---

**Let me know once Git is installed and I can complete the push automatically!**
