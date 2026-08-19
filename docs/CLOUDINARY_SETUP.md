# Cloudinary Setup for Product Images

## Why Cloudinary?

Heroku uses an ephemeral filesystem, meaning uploaded files are deleted when the app restarts (which happens at least once every 24 hours). Cloudinary provides free cloud storage for your product images.

## Step 1: Create Cloudinary Account

1. Go to https://cloudinary.com
2. Click "Sign Up for Free"
3. Fill in your details or sign up with Google/GitHub
4. Verify your email

## Step 2: Get Your Credentials

After logging in:

1. Go to your Dashboard: https://cloudinary.com/console
2. You'll see your credentials:
   - **Cloud Name**: (e.g., `dxyz123abc`)
   - **API Key**: (e.g., `123456789012345`)
   - **API Secret**: (e.g., `abcdefghijklmnopqrstuvwxyz`)

## Step 3: Set Heroku Environment Variables

Run these commands (replace with your actual credentials):

```bash
heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name
heroku config:set CLOUDINARY_API_KEY=your-api-key
heroku config:set CLOUDINARY_API_SECRET=your-api-secret
```

Example:
```bash
heroku config:set CLOUDINARY_CLOUD_NAME=dxyz123abc
heroku config:set CLOUDINARY_API_KEY=123456789012345
heroku config:set CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz
```

## Step 4: Deploy Updated Code

```bash
git add .
git commit -m "Add Cloudinary for media storage"
git push heroku master
```

## Step 5: Upload Product Images

1. Go to your admin panel: `https://your-app.herokuapp.com/admin/`
2. Login with your credentials
3. Go to Products
4. Edit each product and upload images
5. Images will now be stored on Cloudinary and persist across restarts

## How It Works

- **Development (DEBUG=True)**: Images stored locally in `media/` folder
- **Production (DEBUG=False)**: Images automatically uploaded to Cloudinary
- **Automatic**: No code changes needed, Django handles it automatically

## Cloudinary Free Tier

- **Storage**: 25 GB
- **Bandwidth**: 25 GB/month
- **Transformations**: 25,000/month
- **More than enough for a jewellery store!**

## Verify It's Working

1. Upload a product image through admin
2. View the product on your site
3. Right-click the image and "Open in new tab"
4. URL should look like: `https://res.cloudinary.com/your-cloud-name/...`

## Troubleshooting

### Images Not Showing

Check environment variables are set:
```bash
heroku config
```

You should see:
```
CLOUDINARY_CLOUD_NAME: your-cloud-name
CLOUDINARY_API_KEY: your-api-key
CLOUDINARY_API_SECRET: your-api-secret
```

### Upload Fails

1. Check Cloudinary credentials are correct
2. Check you haven't exceeded free tier limits
3. Check Heroku logs: `heroku logs --tail`

### Old Images Not Working

If you uploaded images before Cloudinary setup:
1. Re-upload all product images through admin
2. Old local images won't transfer automatically

## Alternative: AWS S3

If you prefer AWS S3:

1. Install: `pip install django-storages boto3`
2. Configure in settings.py
3. Set AWS credentials in Heroku config

See Django Storages docs: https://django-storages.readthedocs.io/

## Cloudinary Dashboard

Access your Cloudinary dashboard to:
- View all uploaded images
- See storage usage
- Manage transformations
- Monitor bandwidth

Dashboard: https://cloudinary.com/console

## Benefits

✅ Images persist across Heroku restarts
✅ Fast CDN delivery worldwide
✅ Automatic image optimization
✅ Free tier is generous
✅ Easy to set up
✅ No code changes needed

Your product images will now work perfectly on Heroku! 🎉

