# MongoDB Setup Instructions

## Current Issue
The registration page is not working because MongoDB is not accessible. The backend shows this error:
```
No connection could be made because the target machine actively refused it
```

## Solution Options

### Option 1: Use Docker Desktop (Current Setup)

**Steps:**
1. **Start Docker Desktop**
   - Open Docker Desktop application on Windows
   - Wait for it to fully start (Docker icon in system tray should be green)

2. **Run the MongoDB container**
   - Double-click `start_mongodb.bat` file in the project root
   - OR run this command in terminal:
     ```bash
     docker run -d --name lms_db -p 27017:27017 mongo:latest
     ```

3. **Verify MongoDB is running**
   ```bash
   docker ps
   ```
   You should see `lms_db` container running

4. **The backend will automatically reconnect** (it has auto-reload enabled)

5. **Test registration** at http://localhost:5173

---

### Option 2: Use MongoDB Atlas (Cloud - No Docker Required)

**Steps:**
1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create a free account
3. Create a free cluster (M0 tier)
4. Click "Connect" → "Connect your application"
5. Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
6. Update `.env` file:
   ```env
   MONGO_URI=mongodb+srv://your-username:your-password@your-cluster.mongodb.net/ai_tutorial?retryWrites=true&w=majority
   ```
7. Restart the backend server

---

### Option 3: Install MongoDB Locally (No Docker)

**Steps:**
1. Download MongoDB Community Server from https://www.mongodb.com/try/download/community
2. Install MongoDB on Windows
3. Start MongoDB service:
   ```bash
   net start MongoDB
   ```
4. The current `.env` configuration will work automatically
5. Restart the backend server

---

## Verifying the Fix

After setting up MongoDB using any option above:

1. **Check backend logs** - Should see:
   ```
   Connected to MongoDB: ai_tutorial
   ```

2. **Test registration**:
   - Go to http://localhost:5173
   - Fill in the registration form
   - Click "Create Student Account"
   - Should see success message and redirect to login

3. **Check database** (optional):
   - For Docker: `docker exec -it lms_db mongosh`
   - Run: `use ai_tutorial` then `db.users.find()`
   - Should see your registered user

---

## Current Project Status

- ✅ Frontend running on http://localhost:5173
- ✅ Backend running on http://localhost:8000
- ❌ MongoDB not accessible (needs Docker Desktop running)

Once MongoDB is accessible, registration will work immediately!
