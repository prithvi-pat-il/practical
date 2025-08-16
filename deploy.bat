@echo off
echo ====================================
echo  College Practical Helper Deployment
echo ====================================
echo.
echo Your project is ready for deployment!
echo.
echo Files ready:
echo - Flask app: app.py ✓
echo - Templates: %cd%\templates ✓
echo - Static files: %cd%\static ✓
echo - Configuration: wsgi.py, requirements.txt ✓
echo - Documentation: README.md, DEPLOYMENT.md ✓
echo.
echo ====================================
echo  NEXT STEPS FOR YOUR OWN URL:
echo ====================================
echo.
echo 1. Go to: https://www.pythonanywhere.com/
echo 2. Create a FREE account (choose a good username!)
echo 3. Your URL will be: https://USERNAME.pythonanywhere.com
echo.
echo 4. Upload this entire folder to PythonAnywhere
echo 5. Follow the DEPLOYMENT_CHECKLIST.md file
echo.
echo ====================================
echo  CURRENT STATUS:
echo ====================================
echo - Local URL: http://localhost:5000
echo - Admin Login: admin / admin123
echo - Ready for production: YES ✓
echo.
echo Press any key to open deployment checklist...
pause >nul
start DEPLOYMENT_CHECKLIST.md
echo.
echo Press any key to open PythonAnywhere website...
pause >nul
start https://www.pythonanywhere.com/
echo.
echo Happy deploying! 🚀
pause
