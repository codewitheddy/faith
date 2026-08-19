# Sentry Error Tracking Setup Guide

## What is Sentry?

Sentry is a real-time error tracking and monitoring platform that helps you:
- Track and fix errors in production
- Monitor application performance
- Get alerts when errors occur
- See detailed error context (stack traces, user info, request data)
- Track error trends and patterns

---

## Setup Instructions

### Step 1: Create a Sentry Account

1. Go to [https://sentry.io](https://sentry.io)
2. Sign up for a free account (Free tier includes 5,000 errors/month)
3. Verify your email address

### Step 2: Create a New Project

1. Click "Create Project" in your Sentry dashboard
2. Select **Django** as the platform
3. Set alert frequency (recommended: "Alert me on every new issue")
4. Name your project (e.g., "popshop-production")
5. Click "Create Project"

### Step 3: Get Your DSN

After creating the project, Sentry will show you a DSN (Data Source Name). It looks like:
```
https://abc123def456@o123456.ingest.sentry.io/7890123
```

**Copy this DSN** - you'll need it for the next step.

### Step 4: Configure Heroku

Add the Sentry DSN to your Heroku environment variables:

```bash
heroku config:set SENTRY_DSN="https://abc123def456@o123456.ingest.sentry.io/7890123"
```

Or add it via the Heroku Dashboard:
1. Go to your app's Settings
2. Click "Reveal Config Vars"
3. Add a new variable:
   - Key: `SENTRY_DSN`
   - Value: Your DSN from Sentry

### Step 5: Install Dependencies

The sentry-sdk package has already been added to requirements.txt. Install it locally:

```bash
pip install -r requirements.txt
```

### Step 6: Deploy to Heroku

```bash
git add .
git commit -m "Add Sentry error tracking"
git push heroku main
```

### Step 7: Test Sentry Integration

Create a test error to verify Sentry is working:

1. Add a test view in `shop/views.py`:
```python
def sentry_test(request):
    division_by_zero = 1 / 0  # This will trigger an error
```

2. Add URL in `shop/urls.py`:
```python
path('sentry-test/', views.sentry_test, name='sentry_test'),
```

3. Visit: `https://your-app.herokuapp.com/sentry-test/`

4. Check your Sentry dashboard - you should see the error appear within seconds!

5. **Remove the test view and URL after testing**

---

## What Sentry Tracks

### Automatic Error Tracking
- Python exceptions and errors
- Database query errors
- Template rendering errors
- Middleware errors
- 404 and 500 errors

### Performance Monitoring
- Slow database queries
- Slow HTTP requests
- Transaction traces
- Database query performance

### Context Information
For each error, Sentry captures:
- **Stack trace**: Exact line of code that caused the error
- **Request data**: URL, method, headers, query params
- **User info**: Username, IP address (if authenticated)
- **Environment**: Python version, Django version, OS
- **Breadcrumbs**: Events leading up to the error
- **Local variables**: Variable values at the time of error

---

## Sentry Dashboard Features

### Issues
- View all errors grouped by type
- See error frequency and trends
- Mark issues as resolved
- Assign issues to team members
- Add comments and notes

### Performance
- View slow transactions
- Identify performance bottlenecks
- Track database query performance
- Monitor API response times

### Releases
- Track errors by deployment version
- See which release introduced an error
- Monitor error rates after deployments

### Alerts
- Email notifications for new errors
- Slack/Discord integrations
- Custom alert rules
- Spike detection

---

## Configuration Details

### Current Settings (in settings.py)

```python
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration()],
    
    # Performance monitoring
    traces_sample_rate=0.1,  # 10% of transactions in production
    profiles_sample_rate=0.1,  # 10% profiling in production
    
    # Send user info with errors
    send_default_pii=True,
    
    # Environment tracking
    environment='production' if not DEBUG else 'development',
    
    # Release tracking (uses Heroku commit hash)
    release=config('HEROKU_SLUG_COMMIT', default='unknown'),
)
```

### Adjusting Sample Rates

**traces_sample_rate**: Controls performance monitoring
- `1.0` = Monitor 100% of requests (high overhead)
- `0.1` = Monitor 10% of requests (recommended for production)
- `0.01` = Monitor 1% of requests (for high-traffic sites)

**profiles_sample_rate**: Controls profiling
- Same as traces_sample_rate
- Profiling adds more overhead, so keep it low in production

### Filtering Sensitive Data

Sentry automatically filters common sensitive fields:
- Passwords
- Credit card numbers
- API keys
- Session tokens

To filter additional fields, add to settings.py:
```python
sentry_sdk.init(
    # ... other settings
    before_send=lambda event, hint: filter_sensitive_data(event, hint),
)

def filter_sensitive_data(event, hint):
    # Remove specific fields
    if 'request' in event:
        if 'data' in event['request']:
            event['request']['data'].pop('secret_field', None)
    return event
```

---

## Best Practices

### 1. Set Up Alerts
Configure alerts for:
- New issues (immediate notification)
- Issue spikes (10x increase in errors)
- Performance degradation

### 2. Use Releases
Tag each deployment with a release version:
```bash
# In your deployment script
export SENTRY_RELEASE=$(git rev-parse HEAD)
heroku config:set HEROKU_SLUG_COMMIT=$SENTRY_RELEASE
```

### 3. Add Context to Errors
Add custom context in your code:
```python
from sentry_sdk import set_context, set_tag, set_user

# Add user context
set_user({"id": user.id, "email": user.email})

# Add custom tags
set_tag("payment_method", "mpesa")

# Add custom context
set_context("order", {
    "order_id": order.id,
    "total": order.total_amount,
})
```

### 4. Handle Expected Errors
Don't send expected errors to Sentry:
```python
from sentry_sdk import capture_exception

try:
    # Some operation
    process_payment()
except PaymentDeclined as e:
    # Expected error - log locally but don't send to Sentry
    logger.warning(f"Payment declined: {e}")
except Exception as e:
    # Unexpected error - send to Sentry
    capture_exception(e)
    raise
```

### 5. Monitor Performance
Use Sentry's performance monitoring to find:
- Slow database queries
- N+1 query problems
- Slow API calls
- Memory leaks

---

## Troubleshooting

### Sentry Not Receiving Errors

1. **Check DSN is set**:
```bash
heroku config:get SENTRY_DSN
```

2. **Check Sentry is initialized**:
```python
# In Django shell
import sentry_sdk
print(sentry_sdk.Hub.current.client)
# Should show Sentry client info
```

3. **Test with manual error**:
```python
from sentry_sdk import capture_message
capture_message("Test message from Django")
```

4. **Check Heroku logs**:
```bash
heroku logs --tail
# Look for Sentry-related errors
```

### Too Many Errors

If you're hitting rate limits:

1. **Increase sample rate** (reduce monitoring):
```python
traces_sample_rate=0.01  # Monitor only 1%
```

2. **Filter noisy errors**:
```python
def before_send(event, hint):
    # Ignore specific errors
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if isinstance(exc_value, SomeNoisyException):
            return None
    return event

sentry_sdk.init(
    # ... other settings
    before_send=before_send,
)
```

3. **Upgrade Sentry plan** if needed

---

## Cost & Limits

### Free Tier
- 5,000 errors per month
- 10,000 performance units per month
- 30-day error retention
- 1 project
- Email alerts

### Team Plan ($26/month)
- 50,000 errors per month
- 100,000 performance units per month
- 90-day error retention
- Unlimited projects
- Slack/Discord integrations

### Business Plan ($80/month)
- 100,000 errors per month
- 500,000 performance units per month
- 90-day error retention
- Advanced features (custom alerts, SSO)

**Recommendation**: Start with Free tier, upgrade if needed.

---

## Next Steps

1. ✅ Install sentry-sdk (already done)
2. ✅ Configure settings.py (already done)
3. ⏳ Create Sentry account
4. ⏳ Get DSN and add to Heroku
5. ⏳ Deploy and test
6. ⏳ Set up alerts
7. ⏳ Monitor dashboard regularly

---

## Support

- Sentry Documentation: https://docs.sentry.io/platforms/python/guides/django/
- Sentry Support: https://sentry.io/support/
- Community Forum: https://forum.sentry.io/

---

## Summary

Sentry is now configured and ready to use. Once you add the SENTRY_DSN to Heroku and deploy, all errors will be automatically tracked and reported to your Sentry dashboard. This will help you quickly identify and fix issues in production.
