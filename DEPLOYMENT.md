# Deployment Guide

## Backend Deployment (Railway)

### Prerequisites
- Railway account (https://railway.app)
- Neon PostgreSQL database
- OpenAI API key

### Steps

1. **Create New Project on Railway**
   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account and select this repository

2. **Configure Environment Variables**
   Add these variables in Railway dashboard:
   ```
   DATABASE_URL=your_neon_postgres_connection_string
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-3.5-turbo
   APP_NAME=Todo AI Agent
   VERSION=0.1.0
   DEBUG=false
   API_PREFIX=/api
   ALLOWED_ORIGINS=["https://your-frontend-url.vercel.app"]
   PORT=8000
   ```

3. **Set Root Directory**
   - In Railway settings, set root directory to: `backend`
   - Railway will automatically detect the Dockerfile

4. **Deploy**
   - Railway will automatically build and deploy
   - Note your deployment URL (e.g., `https://your-app.railway.app`)

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (https://vercel.com)
- Backend deployed on Railway

### Steps

1. **Import Project to Vercel**
   - Go to Vercel dashboard
   - Click "Add New Project"
   - Import your GitHub repository

2. **Configure Project Settings**
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. **Configure Environment Variables**
   Add these variables in Vercel dashboard:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   NEXT_PUBLIC_AUTH_URL=https://your-backend-url.railway.app/api/auth
   ```

4. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your frontend

## Post-Deployment

### Update CORS Settings
After deployment, update the `ALLOWED_ORIGINS` in Railway to include your Vercel URL:
```
ALLOWED_ORIGINS=["https://your-frontend-url.vercel.app"]
```

### Test the Application
1. Visit your Vercel URL
2. Register a new user
3. Test the chat interface
4. Verify task operations work correctly

## Troubleshooting

### Backend Issues
- Check Railway logs for errors
- Verify DATABASE_URL is correct
- Ensure OPENAI_API_KEY is valid
- Check that PORT environment variable is set

### Frontend Issues
- Verify NEXT_PUBLIC_API_URL points to Railway backend
- Check browser console for CORS errors
- Ensure backend ALLOWED_ORIGINS includes Vercel URL

### Database Issues
- Verify Neon database is active
- Check connection string format
- Ensure SSL mode is enabled

## Local Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python main.py
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your backend URL
npm run dev
```

## Environment Variables Reference

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key
- `OPENAI_MODEL`: Model to use (gpt-3.5-turbo or gpt-4)
- `ALLOWED_ORIGINS`: CORS allowed origins
- `PORT`: Server port (Railway sets this automatically)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_AUTH_URL`: Authentication endpoint URL
