# Feedback Exploration Tool

A full-stack application for exploring and summarizing customer feedback using AI. Built with Python FastAPI, PostgreSQL, React, TypeScript, and Google Gemini API.

## Features

- **Feedback Exploration**: Browse, search, and filter customer feedback by source, sentiment, and date range
- **AI Summarization**: Generate intelligent summaries of feedback using Google Gemini 2.5 Flash
- **Sentiment Analysis**: Automatic sentiment classification (positive, negative, neutral)
- **Statistics Dashboard**: View feedback counts by sentiment and source
- **Real-time Search**: Quick text search across all feedback

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Pydantic
- **Frontend**: React, TypeScript, Vite
- **AI**: Google Gemini 2.5 Flash API
- **Database**: PostgreSQL (local installation)

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL (local installation via Homebrew or direct install)
- Google Gemini API key

## Setup Instructions

### 1. Clone and Navigate

```bash
cd kevin-test-project
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```
# Database Configuration (use your local PostgreSQL username)
DATABASE_URL=postgresql://<YOUR-USERNAME>@localhost:5432/feedback_db

# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Application Settings
DEBUG=false
APP_NAME=Feedback Exploration API
```

### 3. Set Up Local PostgreSQL

#### Install PostgreSQL (if not already installed)

**Using Homebrew:**
```bash
brew install postgresql@18
brew services start postgresql@18
```

**Or download from:** https://www.postgresql.org/download/macosx/

#### Create Database

```bash
# Connect to PostgreSQL (replace 'your_username' with your PostgreSQL username)
psql -U your_username -d postgres

# Create the database
CREATE DATABASE feedback_db;

# Exit psql
\q
```

**Note:** If you don't have a PostgreSQL user set up, you can use your macOS username. Homebrew installations typically use your system username by default.

### 4. Set Up Backend

```bash
cd backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed the database with sample data
python seed_data.py

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs` (when DEBUG=true)

### 5. Set Up Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. **View Feedback**: The main page displays all feedback items with pagination
2. **Search**: Use the search bar to find specific feedback
3. **Filter**: Use the filters panel to narrow down by source, sentiment, or date range
4. **Generate Summary**: Click "Generate Summary" to get an AI-powered summary of the filtered feedback
5. **View Statistics**: Statistics are displayed in the filters panel

## Project Structure

```
kevin-test-project/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/          # Core utilities (constants, exceptions, logging, middleware)
│   │   ├── services/      # Business logic and AI service
│   │   ├── models.py      # Database models
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── database.py    # Database configuration
│   │   ├── config.py      # Application settings
│   │   └── main.py        # FastAPI app
│   ├── requirements.txt
│   └── seed_data.py       # Seed script
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API client
│   │   ├── types/          # TypeScript types
│   │   ├── utils/          # Utility functions
│   │   ├── constants/      # Application constants
│   │   └── App.tsx
│   └── package.json
├── .env.example
├── .gitignore
└── README.md
```

## API Endpoints

- `GET /api/feedback` - List feedback with filters
- `GET /api/feedback/{id}` - Get single feedback item
- `POST /api/feedback` - Create new feedback
- `POST /api/feedback/summarize` - Generate AI summary
- `GET /api/feedback/stats` - Get statistics
- `GET /health` - Health check

## Development

### Backend

- The backend uses FastAPI with automatic API documentation at `/docs` (when DEBUG=true)
- Database models are defined in `app/models.py`
- AI service uses Google Gemini 2.5 Flash API for sentiment analysis and summarization
- Logging is configured in `app/core/logging_config.py` (logs saved to `backend/logs/app.log`)

### Frontend

- Built with Vite for fast development
- TypeScript for type safety
- Responsive design with modern CSS
- Custom hooks for data fetching (`useFeedback`, `useStats`)

## Troubleshooting

- **Database connection errors**: 
  - Ensure PostgreSQL is running: `brew services list | grep postgresql`
  - Verify your username in the DATABASE_URL matches your PostgreSQL user
  - Check that the database exists: `psql -U your_username -d feedback_db -c "\dt"`
  
- **API key errors**: Verify your Gemini API key is set correctly in `.env`

- **CORS errors**: Check that `CORS_ORIGINS` in `.env` includes your frontend URL

- **Port already in use**: 
  - Backend: Change port in uvicorn command or kill existing process
  - Frontend: Vite will automatically use next available port

## Notes

- The seed script creates 32 sample feedback items with varied dates and sentiments
- Sentiment analysis runs automatically when creating new feedback
- The AI summary can handle up to 50 feedback items at once
- Logs are written to `backend/logs/app.log` for debugging

## Architecture Highlights

- **Clean Architecture**: Separation of concerns with core, services, and API layers
- **Error Handling**: Custom exceptions and global error handlers
- **Logging**: Structured logging with file and console output
- **Type Safety**: Full TypeScript coverage in frontend, type hints in backend
- **Database Pooling**: Connection pooling for optimal performance
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
