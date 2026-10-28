# Web Doctor - Frontend

Modern React-based frontend for the Web Doctor healthcare platform.

## 🛠️ Technology Stack

- **React 18**: Modern React with hooks
- **Vite**: Lightning-fast build tool with HMR
- **React Router v7**: Client-side routing
- **Axios**: HTTP client for API calls
- **Lucide React**: Beautiful icon library
- **Vanilla CSS**: Custom styling with Glassmorphism design

## 📦 Dependencies

### Core Dependencies
```json
{
  "react": "^19.2.5",
  "react-dom": "^19.2.5",
  "react-router-dom": "^7.14.2",
  "axios": "^1.15.2",
  "lucide-react": "^0.479.0"
}
```

### Dev Dependencies
```json
{
  "@vitejs/plugin-react": "^6.0.1",
  "vite": "^8.0.10",
  "eslint": "^10.2.1"
}
```

## 🚀 Getting Started

### Installation
```bash
npm install
```

### Development Server
```bash
npm run dev
```
Runs on: **http://localhost:5173**

### Build for Production
```bash
npm run build
```
Output: `dist/` directory

### Preview Production Build
```bash
npm run preview
```

### Linting
```bash
npm run lint
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── main.jsx              # Application entry point
│   ├── App.jsx               # Main app component with routing
│   ├── App.css               # Global styles
│   ├── index.css             # Base CSS variables
│   │
│   ├── components/
│   │   └── Navbar.jsx        # Navigation with notifications
│   │
│   ├── pages/
│   │   ├── LandingPage.jsx   # Home page
│   │   ├── Auth.jsx          # Login/Register
│   │   ├── PatientDashboard.jsx
│   │   ├── DoctorDashboard.jsx
│   │   └── Hospitals.jsx     # Hospital directory
│   │
│   └── assets/
│       ├── hero.png
│       └── icons.svg
│
├── public/
│   ├── favicon.svg
│   └── icons.svg
│
├── index.html
├── vite.config.js
├── package.json
└── eslint.config.js
```

## 🎨 Key Features

### Pages

#### 1. Landing Page (`/`)
- Hero section with call-to-action
- Feature highlights
- Doctor showcase
- Responsive design

#### 2. Authentication (`/login`, `/register`)
- Login form with JWT authentication
- Registration with role selection (Patient/Doctor)
- Phone number field
- Error handling and validation
- Loading states

#### 3. Patient Dashboard (`/dashboard`)
- AI Symptom Checker with multi-language support
- Doctor browsing and appointment booking
- Appointment history
- Health analysis records
- Quick stats cards
- Real-time notifications

#### 4. Doctor Dashboard (`/dashboard`)
- Appointment management
- AI review queue
- Patient consultation details
- Hospital information
- Notification system

#### 5. Hospitals Page (`/hospitals`)
- Hospital directory with 4 locations
- Expandable hospital cards
- Doctor listings per hospital
- Recent appointments view
- Contact information

### Components

#### Navbar
- Responsive navigation
- User authentication state
- Notification bell with badge
- Dropdown notification panel
- Auto-refresh notifications (30s interval)
- Logout functionality

## 🔌 API Integration

### Base URL
```javascript
const API_URL = 'http://localhost:8000';
```

### Authentication Headers
```javascript
const authHeaders = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};
```

### Key API Calls

#### Authentication
```javascript
// Login
axios.post('/token', formData);

// Register
axios.post('/register', userData);

// Get current user
axios.get('/me', { headers: authHeaders() });
```

#### Appointments
```javascript
// Book appointment
axios.post('/appointments', appointmentData, { headers: authHeaders() });

// Get appointments
axios.get('/appointments', { headers: authHeaders() });

// Get hospital appointments
axios.get(`/hospitals/${hospitalId}/appointments`);
```

#### Notifications
```javascript
// Get notifications
axios.get('/notifications', { headers: authHeaders() });

// Get unread count
axios.get('/notifications/unread/count', { headers: authHeaders() });

// Mark as read
axios.put(`/notifications/${id}/read`, {}, { headers: authHeaders() });
```

#### AI Analysis
```javascript
// Analyze symptoms
axios.post('/ai/analyze', { symptoms, language }, { headers: authHeaders() });

// Get model info
axios.get('/ai/model-info');
```

## 🎨 Styling

### CSS Variables
```css
:root {
  --brand: #6366f1;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --text: #1f2937;
  --text-muted: #6b7280;
  --surface: #ffffff;
  --surface-muted: #f3f4f6;
  --border: #e5e7eb;
}
```

### Design System
- **Glassmorphism**: Translucent cards with backdrop blur
- **Gradients**: Linear gradients for headers and buttons
- **Shadows**: Subtle box-shadows for depth
- **Transitions**: Smooth hover and focus states
- **Responsive**: Mobile-first approach

## 🔐 Authentication Flow

1. User submits login/register form
2. Frontend sends credentials to backend
3. Backend returns JWT token
4. Token stored in localStorage
5. Token included in subsequent API requests
6. Protected routes check for valid token
7. Redirect to login if token invalid/missing

## 📱 Responsive Design

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Grid Layouts
```css
.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.layout-2-1 { grid-template-columns: 2fr 1fr; }
```

## 🚨 Error Handling

### Network Errors
```javascript
try {
  const res = await axios.get('/api/endpoint');
  // Handle success
} catch (err) {
  if (err.response) {
    // Server responded with error
    setError(err.response.data.detail);
  } else if (err.message === 'Network Error') {
    // Network issue
    setError('Cannot connect to server');
  } else {
    // Other errors
    setError('An error occurred');
  }
}
```

### Loading States
```javascript
const [loading, setLoading] = useState(false);

const handleSubmit = async () => {
  setLoading(true);
  try {
    await apiCall();
  } finally {
    setLoading(false);
  }
};
```

## 🔄 State Management

### Local State (useState)
- Form inputs
- Loading states
- Error messages
- UI toggles

### Props
- User data passed from App.jsx
- Callback functions for state updates

### localStorage
- JWT token storage
- Persistent authentication

## 🎯 Best Practices

1. **Component Organization**: One component per file
2. **Naming Conventions**: PascalCase for components
3. **Props Validation**: Use PropTypes or TypeScript
4. **Error Boundaries**: Catch and handle errors gracefully
5. **Code Splitting**: Lazy load routes if needed
6. **Accessibility**: ARIA labels and semantic HTML
7. **Performance**: Memoization for expensive operations

## 🧪 Testing

### Manual Testing Checklist
- [ ] Login/Register flows
- [ ] Protected route access
- [ ] Symptom analysis
- [ ] Appointment booking
- [ ] Notification system
- [ ] Hospital browsing
- [ ] Responsive design
- [ ] Error handling

## 🚀 Deployment

### Build
```bash
npm run build
```

### Deploy to Vercel/Netlify
1. Connect repository
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Add environment variables if needed

### Environment Variables
```
VITE_API_URL=https://your-api-domain.com
```

## 📝 Development Tips

### Hot Module Replacement (HMR)
Vite provides instant HMR - changes reflect immediately without full page reload.

### React DevTools
Install React DevTools browser extension for debugging.

### Network Tab
Use browser DevTools Network tab to monitor API calls.

### Console Logging
Use `console.log()` for debugging, remove before production.

## 🤝 Contributing

1. Follow existing code style
2. Test changes thoroughly
3. Update documentation
4. Create meaningful commit messages

## 📄 License

Part of Web Doctor BCA Final Year Project

---

**Built with React + Vite for optimal developer experience**

