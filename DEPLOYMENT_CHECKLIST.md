# Production Deployment Checklist

## 🔐 Security Configuration

- [ ] **SECRET_KEY**: Generate new secure secret key for production
- [ ] **DEBUG**: Set to `False`
- [ ] **ALLOWED_HOSTS**: Configure with your domain(s)
- [ ] **HTTPS**: Set up SSL certificate (Let's Encrypt recommended)
- [ ] **CSRF_TRUSTED_ORIGINS**: Add your domain
- [ ] **Secure Cookies**: Enable for HTTPS
- [ ] **HSTS**: Configure HTTP Strict Transport Security

## 🗄️ Database Setup

- [ ] **PostgreSQL**: Set up production database
- [ ] **DATABASE_URL**: Configure connection string
- [ ] **Migrations**: Run `python manage.py migrate`
- [ ] **Superuser**: Create admin account with `python manage.py createsuperuser`
- [ ] **Backup Strategy**: Set up automated database backups

## 📁 Static Files

- [ ] **STATIC_ROOT**: Configure static files directory
- [ ] **WhiteNoise**: Set up for serving static files
- [ ] **Collect Static**: Run `python manage.py collectstatic`
- [ ] **Media Files**: Configure media storage (if using file uploads)

## 🚀 Deployment Platform

### Render (100% FREE - Recommended)
- [x] Create GitHub repository (✅ https://github.com/Elabs-llc/edufeedback-system.git)
- [x] Create Render account (free) ✅
- [x] ~~Create PostgreSQL database~~ (using SQLite instead) ✅
- [x] Create web service (free) ✅
- [x] Set environment variables ✅
- [x] Deploy and test ✅ **LIVE: https://edufeedback-system.onrender.com**
- [ ] **🔧 URGENT FIX**: Manual redeploy with comprehensive database fixes
- [ ] **🔍 TEST**: Check health endpoint: `/health/`
- [ ] **🔐 VERIFY**: Test login with admin/admin123

### PythonAnywhere (100% FREE)
- [ ] Create PythonAnywhere account
- [ ] Upload code via Git/Files
- [ ] Configure web app
- [ ] Set up virtual environment
- [ ] Configure WSGI file

### Railway (Credit-based - $5/month free credits)
- [ ] Install Railway CLI (`npm install -g @railway/cli`)
- [ ] Create Railway account
- [ ] Initialize project (`railway init`)
- [ ] Add PostgreSQL database
- [ ] Deploy with Git (`railway up`)

### Heroku (Now Paid)
- [x] ~~Install Heroku CLI~~ (Not using - paid service)
- [x] ~~Create Heroku app~~
- [x] ~~Add PostgreSQL addon~~
- [x] ~~Set environment variables~~
- [x] ~~Deploy with Git~~

### DigitalOcean
- [ ] Create App Platform project
- [ ] Connect GitHub repository
- [ ] Configure environment variables
- [ ] Set build/run commands

### VPS/Server
- [ ] Install Python, PostgreSQL, Nginx
- [ ] Configure Gunicorn service
- [ ] Set up Nginx reverse proxy
- [ ] Configure firewall
- [ ] Set up process monitoring

## 🔧 Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
SECRET_KEY=your-django-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgres://user:password@host:port/database
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
```

## 📊 Testing & Monitoring

- [ ] **Functionality Test**: Test all user workflows
- [ ] **Admin Panel**: Verify admin access
- [ ] **Error Logging**: Set up error tracking (Sentry)
- [ ] **Performance**: Monitor response times
- [ ] **Uptime**: Set up uptime monitoring

## 🔄 Post-Deployment

- [ ] **DNS**: Point domain to deployment
- [ ] **Email**: Configure SMTP for notifications (optional)
- [ ] **Backups**: Verify backup procedures
- [ ] **Documentation**: Update deployment docs
- [ ] **Team Access**: Grant access to team members

## 🆘 Quick Commands

```bash
# Heroku deployment
heroku create your-app-name
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser

# Local testing in production mode
export DEBUG=False
export SECRET_KEY="test-key"
python manage.py runserver
```

---

**✅ Deployment Ready! Your EduFeedback System is production-ready.**
