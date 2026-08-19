# Quick Cloudinary Setup

## 1. Sign up at Cloudinary
Visit: https://cloudinary.com/users/register_free

## 2. Get your credentials from dashboard
Visit: https://cloudinary.com/console

## 3. Run these commands (replace with your credentials):

```bash
heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name
heroku config:set CLOUDINARY_API_KEY=your-api-key  
heroku config:set CLOUDINARY_API_SECRET=your-api-secret
```

## 4. Deploy the changes:

```bash
git push heroku master
```

## 5. Upload product images through admin

That's it! Your images will now persist on Heroku.

For detailed instructions, see CLOUDINARY_SETUP.md
