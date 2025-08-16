# College Practical Helper - Deployment Guide

This guide will walk you through deploying the College Practical Helper web application to PythonAnywhere for free hosting.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [PythonAnywhere Setup](#pythonanywhere-setup)
- [File Upload](#file-upload)
- [Database Setup](#database-setup)
- [Web App Configuration](#web-app-configuration)
- [Domain Configuration](#domain-configuration)
- [Post-Deployment Setup](#post-deployment-setup)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)

## 🔧 Prerequisites

1. **PythonAnywhere Account**: Create a free account at [pythonanywhere.com](https://www.pythonanywhere.com/)
2. **Project Files**: Have all project files ready (created by following this guide)
3. **Admin Credentials**: Note down the default admin credentials (admin/admin123)

## 🚀 PythonAnywhere Setup

### Step 1: Create Account and Login
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com/)
2. Click "Pricing & signup" → "Create a Beginner account"
3. Fill in your details and verify your email
4. Login to your dashboard

### Step 2: Access Console
1. In your PythonAnywhere dashboard, click on "Tasks" → "Consoles"
2. Click "New console: Bash"
3. You now have a terminal interface

## 📁 File Upload

### Option A: Using Git (Recommended)
If you have your code in a Git repository:

```bash
# In the PythonAnywhere Bash console
cd ~
git clone https://github.com/yourusername/college_practical_helper.git
```

### Option B: Manual Upload
1. In PythonAnywhere dashboard, go to "Files"
2. Navigate to your home directory (`/home/yourusername/`)
3. Create a new folder: `college_practical_helper`
4. Upload each file individually:
   - `app.py`
   - `wsgi.py`
   - `requirements.txt`
   - `config.py`
   - Upload the entire `templates/` folder
   - Upload the entire `static/` folder

### Option C: Using the Files Tab
1. Click "Files" in your dashboard
2. Navigate to `/home/yourusername/`
3. Click "Upload a file" and select your project files
4. Alternatively, use "Open Bash console here" and use command line tools

## 🗄️ Database Setup

### Step 1: Create Database Directory
```bash
# In your Bash console
cd ~/college_practical_helper
mkdir -p instance
```

### Step 2: Initialize Database
```bash
# Run the app once to create the database
python3.9 app.py
# Press Ctrl+C to stop after it says "Running on http://127.0.0.1:5000"
```

The database will be created automatically with sample data when you first run the app.

## 🌐 Web App Configuration

### Step 1: Create Web App
1. In your dashboard, click on "Web" tab
2. Click "Add a new web app"
3. Click "Next" for your domain (yourusername.pythonanywhere.com)
4. Select "Manual configuration"
5. Choose "Python 3.9"
6. Click "Next"

### Step 2: Configure WSGI File
1. In the Web tab, scroll down to "Code" section
2. Click on "WSGI configuration file" link
3. Delete all existing content and replace with:

```python
#!/usr/bin/python3.9

import sys
import os

# Add your project directory to Python path
sys.path.insert(0, '/home/yourusername/college_practical_helper')

from app import app as application

if __name__ == "__main__":
    application.run()
```

**Important**: Replace `yourusername` with your actual PythonAnywhere username!

### Step 3: Set Virtual Environment (Optional but Recommended)
1. In the Web tab, find "Virtualenv" section
2. Enter: `/home/yourusername/.virtualenvs/mysite-virtualenv`
3. Create the virtual environment in your Bash console:

```bash
cd ~
python3.9 -m venv .virtualenvs/mysite-virtualenv
source .virtualenvs/mysite-virtualenv/bin/activate
cd college_practical_helper
pip install -r requirements.txt
```

### Step 4: Configure Static Files
1. In the Web tab, scroll to "Static files" section
2. Add a new static file mapping:
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/college_practical_helper/static/`

### Step 5: Reload Web App
1. Scroll to the top of the Web tab
2. Click the big green "Reload yourusername.pythonanywhere.com" button
3. Wait for the reload to complete

## 🔗 Domain Configuration

### Free Subdomain
Your app will be available at: `https://yourusername.pythonanywhere.com`

### Custom Domain (Paid Plans Only)
If you have a paid plan and want to use a custom domain:
1. In the Web tab, click "Add a new web app"
2. Enter your custom domain
3. Follow the same configuration steps above
4. Update your domain's DNS settings as instructed

## ⚙️ Post-Deployment Setup

### Step 1: Test the Application
1. Visit your website: `https://yourusername.pythonanywhere.com`
2. You should see the homepage with default subjects
3. Test the debug helper functionality
4. Try admin login with default credentials

### Step 2: Admin Setup
1. Go to `https://yourusername.pythonanywhere.com/admin`
2. Login with default credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
3. **IMPORTANT**: Change the admin password immediately for security

### Step 3: Add Sample Content
1. In the admin dashboard, add your first subject
2. Add sample questions to test functionality
3. Verify everything works correctly

### Step 4: Security Configuration
1. In your Bash console, edit the app.py file:
```bash
nano ~/college_practical_helper/app.py
```
2. Change the secret key to something secure:
```python
app.secret_key = 'your-very-secure-secret-key-here'
```
3. Save the file (Ctrl+X, then Y, then Enter)
4. Reload your web app

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. "Something went wrong" Error Page
- Check the error logs in the Web tab → "Error log"
- Ensure all file paths in wsgi.py are correct
- Verify Python version is set to 3.9

#### 2. Static Files Not Loading
- Check static files mapping in Web tab
- Ensure path is: `/home/yourusername/college_practical_helper/static/`
- Verify files exist in the static directory

#### 3. Database Issues
- Ensure the instance directory exists
- Check database file permissions
- Try recreating the database:
```bash
cd ~/college_practical_helper
rm -f instance/database.db
python3.9 app.py
```

#### 4. Import Errors
- Check that all files are uploaded correctly
- Verify requirements.txt dependencies are installed
- Use virtual environment if packages conflict

#### 5. 404 Errors
- Ensure WSGI configuration is correct
- Check that app.py is in the right location
- Verify all routes are properly defined

### Debug Mode
To enable debug mode for troubleshooting (disable in production):
```python
# In app.py, change the last line to:
app.run(debug=True)
```

## 🔧 Maintenance

### Regular Tasks

#### 1. Backup Database
```bash
# Download a copy of your database
cp ~/college_practical_helper/instance/database.db ~/backup_$(date +%Y%m%d).db
```

#### 2. Update Application
If you make changes to your code:
1. Upload the changed files
2. Reload the web app from the Web tab

#### 3. Monitor Usage
- Check the Web tab for reload statistics
- Monitor error logs regularly
- Keep track of storage usage

#### 4. Security Updates
- Regularly update dependencies:
```bash
cd ~/college_practical_helper
pip install --upgrade -r requirements.txt
```
- Change admin passwords periodically
- Monitor for suspicious admin login attempts

### Performance Optimization

#### 1. Free Tier Limitations
- PythonAnywhere free tier sleeps after 3 months of inactivity
- Limited CPU seconds per day
- One web app per account

#### 2. Optimization Tips
- Optimize database queries
- Minimize large file uploads
- Use caching for frequently accessed data
- Keep static files optimized

## 📧 Support

### Getting Help
1. **PythonAnywhere Help**: Check their [help pages](https://help.pythonanywhere.com/)
2. **Forums**: Post questions on PythonAnywhere forums
3. **Documentation**: Reference Flask and Python documentation

### Useful Resources
- [PythonAnywhere Flask Tutorial](https://help.pythonanywhere.com/pages/Flask/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://sqlite.org/docs.html)

## 🎉 Congratulations!

Your College Practical Helper website should now be live and accessible to students worldwide! 

**Website URL**: `https://yourusername.pythonanywhere.com`

### What Students Can Do:
- ✅ Browse subjects without login
- ✅ View practical questions and solutions
- ✅ Use the AI debug helper
- ✅ Access from any device
- ✅ Share question links with classmates

### What You Can Do as Admin:
- ✅ Add new subjects and questions
- ✅ Edit existing content
- ✅ Manage the website completely
- ✅ Monitor usage and performance

---

**Next Steps**: Start adding your actual course subjects and questions to make the website useful for your students. Don't forget to share the URL with them!

**Pro Tip**: Consider upgrading to a paid PythonAnywhere plan if you need:
- Custom domain name
- More CPU seconds
- Always-on tasks
- Multiple web apps
