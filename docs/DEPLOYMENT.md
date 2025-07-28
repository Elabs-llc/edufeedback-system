# EduFeedback System - Production Deployment Guide

## 🚀 Deployment Options

### Option 1: Heroku Deployment (Recommended for beginners)

#### Prerequisites
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create a [Heroku account](https://heroku.com)

#### Steps
1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   cd feedback_system
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY="your-super-secret-key-here"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
   ```

4. **Add PostgreSQL Database**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. **Deploy to Heroku**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for deployment"
   git push heroku main
   ```

6. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

7. **Collect Static Files**
   ```bash
   heroku run python manage.py collectstatic --noinput
   ```

### Option 2: DigitalOcean App Platform

1. **Create App on DigitalOcean**
   - Go to DigitalOcean App Platform
   - Connect your GitHub repository
   - Select your repository and branch

2. **Configure Environment Variables**
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com
   DATABASE_URL=postgres://user:pass@host:port/db
   ```

3. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn feedback_system.wsgi:application`

### Option 3: Railway Deployment

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Add Database**
   ```bash
   railway add postgresql
   ```

### Option 4: VPS/Server Deployment

#### Prerequisites
- Ubuntu/CentOS server
- Python 3.8+
- PostgreSQL
- Nginx
- SSL certificate (Let's Encrypt recommended)

#### Server Setup
1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv postgresql nginx
   ```

2. **Setup Database**
   ```bash
   sudo -u postgres createdb edufeedback
   sudo -u postgres createuser --interactive
   ```

3. **Deploy Application**
   ```bash
   git clone your-repository.git
   cd feedback_system
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your production values
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

6. **Setup Gunicorn Service**
   ```bash
   sudo vim /etc/systemd/system/edufeedback.service
   ```
   
   Add content:
   ```ini
   [Unit]
   Description=EduFeedback gunicorn daemon
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/feedback_system
   ExecStart=/path/to/feedback_system/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/path/to/feedback_system/feedback_system.sock feedback_system.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

7. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       location /static/ {
           root /path/to/feedback_system;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/path/to/feedback_system/feedback_system.sock;
       }
   }
   ```

## 🔧 Pre-Deployment Checklist

### Security
- [ ] Change SECRET_KEY to a secure random string
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Set up HTTPS/SSL
- [ ] Configure CSRF_TRUSTED_ORIGINS
- [ ] Set secure cookie settings

### Database
- [ ] Set up PostgreSQL for production
- [ ] Configure DATABASE_URL
- [ ] Run migrations on production
- [ ] Create superuser account

### Static Files
- [ ] Configure STATIC_ROOT
- [ ] Run collectstatic
- [ ] Set up WhiteNoise or CDN

### Monitoring
- [ ] Set up error logging
- [ ] Configure email notifications
- [ ] Set up monitoring (New Relic, Sentry)

## 🌍 Environment Variables Reference

```bash
# Required
SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgres://user:pass@host:port/database

# Security (HTTPS only)
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000

# Optional
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📊 Post-Deployment Tasks

1. **Test all functionality**
   - User registration/login
   - Course enrollment
   - Feedback submission
   - Admin panel access

2. **Set up monitoring**
   - Error tracking
   - Performance monitoring
   - Uptime monitoring

3. **Configure backups**
   - Database backups
   - Media file backups
   - Code repository backups

4. **Set up CI/CD (Optional)**
   - GitHub Actions
   - Automated testing
   - Automated deployment

## 🆘 Troubleshooting

### Common Issues

1. **Static files not loading**
   ```bash
   python manage.py collectstatic --clear
   ```

2. **Database connection errors**
   - Check DATABASE_URL format
   - Verify database credentials
   - Ensure database server is running

3. **CSRF errors**
   - Check CSRF_TRUSTED_ORIGINS
   - Verify HTTPS configuration
   - Check cookie settings

4. **Permission errors**
   - Set correct file permissions
   - Check user/group ownership
   - Verify directory access

## 📞 Support

For deployment support:
- Check Django documentation
- Review platform-specific guides
- Monitor application logs
- Use platform support channels

---

**Your EduFeedback System is now ready for production! 🎉**
