# 🚀 Quick Deployment Checklist for Your Own URL

## ✅ Pre-Deployment Checklist

### 1. Account Setup
- [ ] Create free PythonAnywhere account at: https://www.pythonanywhere.com/
- [ ] Choose a username (this will be part of your URL: `yourusername.pythonanywhere.com`)
- [ ] Verify your email address
- [ ] Login to your dashboard

### 2. File Preparation
Your files are ready! Here's what you have:
- [x] `app.py` - Main Flask application
- [x] `wsgi.py` - Web server configuration
- [x] `requirements.txt` - Python dependencies
- [x] `templates/` folder - All HTML templates
- [x] `static/` folder - CSS, JS, and assets
- [x] Database will be created automatically

### 3. Security Setup
- [ ] Change admin password from default (admin123) to something secure
- [ ] Update secret key in app.py for production

## 🌐 Deployment Steps

### Step 1: Upload Files
Choose one option:

**Option A: ZIP Upload (Easiest)**
1. Create a ZIP file of your `college_practical_helper` folder
2. In PythonAnywhere, go to "Files" tab
3. Upload the ZIP file
4. Extract it to your home directory

**Option B: Manual Upload**
1. In PythonAnywhere, go to "Files" tab
2. Create folder: `college_practical_helper`
3. Upload each file individually

### Step 2: Create Web App
1. Go to "Web" tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose your domain: `yourusername.pythonanywhere.com`
4. Select "Manual configuration"
5. Choose "Python 3.9"

### Step 3: Configure WSGI
1. Click on WSGI configuration file link
2. Replace all content with:

```python
#!/usr/bin/python3.9

import sys
import os

# Add your project directory to Python path
sys.path.insert(0, '/home/YOURUSERNAME/college_practical_helper')

from app import app as application

if __name__ == "__main__":
    application.run()
```
**IMPORTANT**: Replace `YOURUSERNAME` with your actual PythonAnywhere username!

### Step 4: Set Up Static Files
1. In Web tab, find "Static files" section
2. Add new mapping:
   - URL: `/static/`
   - Directory: `/home/YOURUSERNAME/college_practical_helper/static/`

### Step 5: Install Dependencies
1. Open a Bash console from "Tasks" → "Consoles"
2. Run these commands:
```bash
cd ~/college_practical_helper
pip3.9 install --user flask
python3.9 app.py
```
3. Press Ctrl+C to stop after database is created

### Step 6: Launch Your Website
1. Go back to Web tab
2. Click the big green "Reload" button
3. Visit your URL: `https://yourusername.pythonanywhere.com`

## 🎉 Your Website URLs

After deployment, you'll have:
- **Student Access**: `https://yourusername.pythonanywhere.com`
- **Admin Panel**: `https://yourusername.pythonanywhere.com/admin`
- **Debug Helper**: `https://yourusername.pythonanywhere.com/debug-helper`

## 🔧 Post-Deployment Tasks

### Immediate Security Tasks
1. Visit `https://yourusername.pythonanywhere.com/admin`
2. Login with: admin / admin123
3. **IMMEDIATELY change the admin password!**

### Content Setup
1. Delete sample subjects you don't need
2. Add your actual course subjects
3. Add real practical questions and solutions
4. Test all functionality

### Share with Students
1. Share the main URL: `https://yourusername.pythonanywhere.com`
2. Tell them: "No login needed - just browse and learn!"
3. Show them the AI Debug Helper feature

## 🆘 Troubleshooting

### Common Issues:
1. **"Something went wrong" error**
   - Check error logs in Web tab
   - Verify WSGI file paths are correct

2. **CSS/JS not loading**
   - Check static files mapping
   - Ensure path includes your username

3. **Database errors**
   - Run `python3.9 app.py` in console to create database
   - Check file permissions

### Need Help?
- Check the detailed `DEPLOYMENT.md` file
- PythonAnywhere help: https://help.pythonanywhere.com/
- Forums: https://www.pythonanywhere.com/forums/

## 🎯 Success Indicators

Your deployment is successful when:
- [x] Main website loads at your URL
- [x] Subject cards are visible and clickable
- [x] Admin panel works with login
- [x] Debug helper responds to queries
- [x] Mobile version looks good
- [x] All animations work smoothly

**Estimated deployment time: 15-30 minutes**

---

**🎓 Once deployed, your students will have 24/7 access to practical exam help at your custom URL!**
