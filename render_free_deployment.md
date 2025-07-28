# Render FREE Deployment Guide - Step by Step

## ✅ COMPLETELY FREE - No Credit Cards Required

### Step 1: Prepare GitHub Repository
1. Create GitHub account (if you don't have one)
2. Create new repository: "edufeedback-system"
3. Push your code to GitHub:

```bash
cd "c:\Users\HP\Downloads\Projects\Feedback\feedback_system"
git remote add origin https://github.com/YOUR_USERNAME/edufeedback-system.git
git branch -M main
git push -u origin main
```

### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (free)
3. Verify your email

### Step 3: Create PostgreSQL Database (FREE)
1. Click "New" → "PostgreSQL"
2. Name: edufeedback-db
3. Database: edufeedback
4. User: admin
5. Region: Choose closest to you
6. Plan: FREE
7. Click "Create Database"
8. **Copy the External Database URL** (you'll need this)

### Step 4: Create Web Service (FREE)
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Select "edufeedback-system" repository
4. Configure:
   - **Name**: edufeedback-system
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn feedback_system.wsgi:application`
   - **Plan**: FREE

### Step 5: Set Environment Variables
In the Environment section, add:
- `SECRET_KEY` = `typaagmqynzp!v*7+52n6z6&dr*ey+osr3$0c3jnda9y!l0tz2`
- `DEBUG` = `False`
- `DATABASE_URL` = `[paste the PostgreSQL URL from Step 3]`
- `ALLOWED_HOSTS` = `edufeedback-system.onrender.com`
- `CSRF_TRUSTED_ORIGINS` = `https://edufeedback-system.onrender.com`

### Step 6: Deploy
1. Click "Create Web Service"
2. Wait for build (5-10 minutes)
3. Your app will be live at: https://edufeedback-system.onrender.com

### Step 7: Run Database Setup
1. Go to your web service dashboard
2. Click "Shell" tab
3. Run these commands:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 🎉 That's it! Your app is live and 100% FREE!

## ⚠️ Free Tier Limitations:
- App "sleeps" after 15 minutes of inactivity (takes 30 seconds to wake up)
- 750 hours/month (enough for full-time hosting)
- Limited database storage (sufficient for your app)

## 💡 Benefits:
- ✅ Completely free forever
- ✅ Custom domain support
- ✅ Automatic HTTPS
- ✅ GitHub auto-deploy
- ✅ Great for portfolio projects
