# Web Doctor - Quick Start Guide

Get up and running with Web Doctor in 5 minutes!

## ⚡ Quick Setup

### 1. Prerequisites Check
```bash
# Check Python version (need 3.8+)
python --version

# Check Node.js version (need 16+)
node --version

# Check npm version
npm --version
```

### 2. Install Backend
```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running at: **http://localhost:8000**

### 3. Install Frontend (New Terminal)
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

✅ Frontend running at: **http://localhost:5173**

## 🎯 First Steps

### 1. Open the App
Go to: **http://localhost:5173**

### 2. Try Symptom Checker (No Login Required)
1. Click "Get Started"
2. Enter: "fever and headache"
3. Click "Analyze Symptoms"
4. View AI diagnosis!

### 3. Create Patient Account
1. Click "Create Account"
2. Fill in:
   - Name: Your Name
   - Phone: 9876543210
   - Email: patient@test.com
   - Password: test123
   - Role: Patient
3. Click "Create Account"
4. Login with same credentials

### 4. Book an Appointment
1. Go to Dashboard
2. Scroll to "Available Doctors"
3. Click "Book Appointment" on any doctor
4. Check notification bell (top right) - you'll see "1"!

### 5. Login as Doctor
1. Logout
2. Login with:
   - Email: dr.sharma@apollo.com
   - Password: doctor123
3. Check notification bell - you'll see the appointment!
4. View appointment in dashboard

### 6. View Hospital Appointments
1. Click "Hospitals" in navbar
2. Click on "Apollo Multispecialty Hospital"
3. Scroll down to see "Recent Appointments"
4. Your booking is visible!

## 🏥 Test Accounts

### Doctors (All password: doctor123)
```
dr.sharma@apollo.com       - Cardiologist
dr.priya@apollo.com        - Pediatrician
dr.singh@fortis.com        - General Medicine
dr.reddy@fortis.com        - Dermatologist
dr.gupta@maxhealthcare.com - Neurologist
dr.iyer@manipal.com        - OB/GYN
```

## 🔧 Troubleshooting

### Backend won't start?
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Try different port
uvicorn main:app --reload --port 8001
```

### Frontend won't start?
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Database issues?
```bash
# Delete and recreate database
# Stop backend server
# Delete backend/webdoctor.db
# Restart backend (auto-creates fresh DB)
```

### Can't login?
- Make sure backend is running
- Check browser console for errors
- Try registering a new account
- Clear browser cache/localStorage

## 📱 Features to Try

### ✅ Patient Features
- [ ] AI Symptom Analysis (English & Hindi)
- [ ] Browse 11 specialist doctors
- [ ] Book appointments
- [ ] View appointment history
- [ ] Check notifications
- [ ] View hospital information

### ✅ Doctor Features
- [ ] View appointments
- [ ] Review AI analyses
- [ ] Check notifications
- [ ] See hospital info

### ✅ Hospital Features
- [ ] Browse 4 hospitals
- [ ] View doctors per hospital
- [ ] See recent appointments
- [ ] Check contact details

## 🎨 UI Features

- **Glassmorphism Design**: Modern translucent cards
- **Gradient Backgrounds**: Eye-catching colors
- **Notification Bell**: Real-time updates
- **Responsive Layout**: Works on mobile
- **Smooth Animations**: Hover effects

## 📊 API Documentation

Visit: **http://localhost:8000/docs**

Interactive Swagger UI with all endpoints!

## 🚨 Important Notes

### Medical Disclaimer
⚠️ This is a **demo project** for educational purposes
- Not for actual medical use
- AI guidance is not professional medical advice
- For emergencies, call 108 (India)

### Security Notes
🔒 For production:
- Change SECRET_KEY in backend/main.py
- Use HTTPS
- Add rate limiting
- Use environment variables

## 📞 Need Help?

1. Check README.md for detailed docs
2. Check backend logs in terminal
3. Check browser console (F12)
4. Review API docs at /docs

## 🎉 You're All Set!

Enjoy exploring Web Doctor! 

**Next Steps:**
- Try all features
- Test with different symptoms
- Book multiple appointments
- Check notifications
- Explore hospital pages

---

**Happy Coding! 🚀**
