# Deployment Guide — TeacherManager

Deploy TeacherManager to Render (or similar platforms).

---

## Prerequisites

- GitHub account with TeacherManager repository
- Render account (https://render.com)
- PostgreSQL database (Render provides one)
- (Optional) Sentry account for error tracking

---

## Step 1: Prepare Repository

Ensure these files are in the repo root:

```
Dockerfile              # Container definition
docker-compose.yml      # (Optional, for local Docker testing)
requirements.txt        # Python dependencies
.env.example            # Environment template
PROGRESS.md             # Deployment checklist
```

Make sure all code is committed and pushed to GitHub:

```bash
git add -A
git commit -m "Deploy: ready for production"
git push origin main
```

---

## Step 2: Set Up PostgreSQL on Render

1. **Log in to Render Dashboard:** https://dashboard.render.com
2. **Create new PostgreSQL database:**
   - Name: `teachermanager-db`
   - Plan: Free or Starter (depending on scale)
   - Region: Closest to your users
3. **Note the connection string** (looks like `postgresql://user:pass@host/dbname`)

---

## Step 3: Create Web Service on Render

1. **Create Web Service:**
   - Name: `teachermanager-api`
   - Environment: Docker
   - Repository: Your GitHub repo
   - Branch: `main`
   - Dockerfile path: `./Dockerfile`

2. **Set Environment Variables:**

```env
APP_NAME=TeacherManager
APP_ENV=production
DEBUG=false
LOG_LEVEL=info

# Database (from PostgreSQL service)
DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname
DATABASE_URL_SYNC=postgresql://user:pass@host/dbname

# Redis (optional, use for caching)
REDIS_URL=redis://...

# JWT
SECRET_KEY=<generate-secure-random-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Sentry (optional)
SENTRY_DSN=<your-sentry-dsn>
SENTRY_TRACES_SAMPLE_RATE=0.2

# CORS
ALLOWED_ORIGINS=https://teachermanager.render.com,https://yourdomain.com

# Seed credentials (set only if needed, then remove after first run)
INITIAL_ADMIN_PASSWORD=<secure-password>
INITIAL_USER_PASSWORD=<secure-password>
FORCE_SEED_IN_PROD=false
```

3. **Build Settings:**
   - Build command: `pip install -r requirements.txt && alembic upgrade head`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

4. **Create Service** and wait for deployment

---

## Step 4: Run Initial Migrations

After first deployment, run migrations:

```bash
# Via Render shell or local connection
alembic upgrade head

# Seed initial data (if defined)
python scripts/seed_db.py  # (Create this if needed)
```

---

## Step 5: Set Up Monitoring (Optional)

### Sentry Integration

1. **Create Sentry project** (https://sentry.io)
2. **Get DSN** from project settings
3. **Set `SENTRY_DSN`** in Render env vars
4. Errors will automatically be sent to Sentry

### Health Checks

Enable health checks on Render:
- Health check path: `/health`
- Interval: 10 seconds
- Timeout: 5 seconds

---

## Step 6: Verify Deployment

Check that the app is running:

```bash
curl https://teachermanager.render.com/health
# Expected response:
# {"status":"ok","app":"TeacherManager","environment":"production"}

curl https://teachermanager.render.com/docs
# Swagger UI should be accessible
```

---

## Step 7: Connect Custom Domain (Optional)

1. **Add custom domain in Render:**
   - Domain: `yourdomain.com`
   - Render will provide DNS records

2. **Update DNS provider** with Render's CNAME records

3. **Update `ALLOWED_ORIGINS`** in environment to include custom domain

---

## Production Checklist

- [ ] Database backups configured
- [ ] Sentry monitoring active
- [ ] HTTPS enabled (Render provides automatic SSL)
- [ ] Health checks passing
- [ ] Error logging working
- [ ] Audit logs stored in database
- [ ] Rate limiting configured (if needed)
- [ ] CORS origins restricted to known domains
- [ ] SECRET_KEY is strong and unique
- [ ] Database migrations executed successfully
- [ ] Admin user created (if applicable)
- [ ] Email notifications configured (if applicable)

---

## Scaling Considerations

### Increase Instances

For higher load, increase the number of Render instances:

1. Go to Render Web Service settings
2. Scale up number of instances
3. Render will auto-balance traffic

### External Redis

For session/cache scaling, use external Redis:

1. Provision Redis on Render or AWS ElastiCache
2. Update `REDIS_URL` env var
3. Redeploy

### Database Scaling

If PostgreSQL hits limits:

1. Upgrade database plan on Render
2. Or migrate to managed PostgreSQL on AWS, GCP, Azure

---

## Troubleshooting

### Deployment fails

Check build logs in Render dashboard:
- Python version mismatch (should be 3.12)
- Dependency install errors
- Missing environment variables

### App crashes after deploy

Check logs via Render shell or streaming logs:
- Migration failures: `alembic upgrade head` might need manual fix
- Missing env vars: Check all required vars are set
- Database connection refused: Verify `DATABASE_URL`

### Health checks failing

- Service may not be ready (wait 30-60s after deploy)
- Check app logs for startup errors
- Verify `SECRET_KEY` is set

---

## Rollback Strategy

If deployment fails in production:

1. **Revert code:**
   ```bash
   git revert <commit-hash>
   git push origin main
   ```

2. **Render automatically redeploys** (if "Auto-deploy" is enabled)

3. **Manual rollback:** In Render, deploy a previous commit

4. **Database rollback (if migration broke data):**
   ```bash
   alembic downgrade -1
   ```

---

## Monitoring Post-Deployment

### Key Metrics to Monitor

- **Response time:** Target < 200ms p95
- **Error rate:** Target < 0.1%
- **Database connection pool:** Monitor active connections
- **CPU usage:** Render alerts if > 80%
- **Memory usage:** Render alerts if > 80%

### Set Up Alerts

In Render dashboard:
- Enable email alerts for deployment failures
- Enable alerts for out-of-memory conditions
- Configure Sentry to email on critical errors

---

## Next Steps

1. **Monitor logs** for first 24 hours post-deploy
2. **Test all critical user flows** in production
3. **Collect metrics** to inform scaling decisions
4. **Plan regular backups** and disaster recovery
5. **Document any customizations** for future deployments

---

For questions or issues, refer to:
- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Alembic Docs: https://alembic.sqlalchemy.org
