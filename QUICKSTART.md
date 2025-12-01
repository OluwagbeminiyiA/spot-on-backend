# SpotOn Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install django-cors-headers
```

## Step 2: Start Django Backend

```bash
cd "c:\Users\DELL 5320\PycharmProjects\SpotOn"
python manage.py runserver
```

The backend will run on `http://localhost:8000`

## Step 3: Open Frontend

**Option A: Using Live Server (Recommended)**
1. Install "Live Server" extension in VS Code
2. Right-click on `spoton_frontend/index.html`
3. Select "Open with Live Server"
4. Your browser will open to `http://localhost:5500` or similar

**Option B: Using Python HTTP Server**
```bash
cd spoton_frontend
python -m http.server 8080
```
Then open `http://localhost:8080` in your browser

**Option C: Direct File (May have CORS issues)**
- Double-click `spoton_frontend/index.html`

## Step 4: Create Your Account

To use protected features (add spots, write reviews, report status), you need an account:

```bash
python manage.py createsuperuser
```

Follow the prompts to create your username and password.

## Step 5: Login When Needed

### Two Ways to Login:

**Option 1: Proactive Login**
- Click the "Login" button in the navigation bar
- Login at `http://localhost:8000/api-auth/login/`
- Automatically redirected back to the frontend

**Option 2: Reactive Login**
- Try to use a protected feature (Add Spot, Write Review, Report Status)
- You'll see: "Please login to [action]"
- Automatically redirected to login page
- After login, you're back in the app!

## Features You Can Test

### Without Login:
✅ **Browse Spots** - View all approved study spots
✅ **Search & Filter** - Search by name/location, filter by capacity or features
✅ **View Details** - Click any spot to see full details, reviews, and status

### With Login:
✅ **Add Spot** - Click "Add Spot" button to submit new study locations
✅ **Write Review** - Open a spot detail and click "Write Review"
✅ **Report Status** - Update occupancy status

## Troubleshooting

**Problem: "CORS error" in browser console**
- Solution: Make sure django-cors-headers is installed and Django settings are updated

**Problem: "No spots found"**
- Solution: Create and approve some spots in Django admin (`http://localhost:8000/admin/`)

**Problem: Redirected to login when trying to add spot/review**
- Solution: This is normal! Login with your superuser credentials, then you'll be redirected back

**Problem: Frontend can't connect to API**
- Solution: Ensure Django server is running on port 8000

**Problem: Login not persisting**
- Solution: Make sure cookies are enabled and you're not in incognito/private mode

## Next Steps

1. Create your superuser account
2. Login via the "Login" button or by trying a protected action
3. Add some study spots to the platform
4. Browse and review existing spots
5. Report real-time status updates

Enjoy using SpotOn! 🎯
