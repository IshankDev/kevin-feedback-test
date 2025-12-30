# Feedback Exploration Tool

A full-stack application for exploring and summarizing customer feedback using AI. Built with Python FastAPI, PostgreSQL, React, TypeScript, and Google Gemini API.

## Features

- **Feedback Exploration**: Browse, search, and filter customer feedback by source, sentiment, and date range
- **AI Summarization**: Generate intelligent summaries of feedback using Google Gemini
- **Sentiment Analysis**: Automatic sentiment classification (positive, negative, neutral)
- **Statistics Dashboard**: View feedback counts by sentiment and source
- **Real-time Search**: Quick text search across all feedback

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Alembic
- **Frontend**: React, TypeScript, Vite
- **AI**: Google Gemini API
- **Database**: PostgreSQL (via Docker Compose)

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker and Docker Compose
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

Edit `.env` and add your Google Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Start PostgreSQL Database

```bash
docker-compose up -d
```

This will start a PostgreSQL container on port 5432.

### 4. Set Up Backend

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations (tables will be created automatically on first run)
# The app will create tables automatically, but you can also use Alembic if needed

# Seed the database with sample data
python seed_data.py

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

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
│   │   ├── services/      # Business logic and AI service
│   │   ├── models.py      # Database models
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── database.py    # Database configuration
│   │   ├── config.py      # Application settings
│   │   └── main.py        # FastAPI app
│   ├── alembic/           # Database migrations
│   ├── requirements.txt
│   └── seed_data.py       # Seed script
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   ├── types/         # TypeScript types
│   │   └── App.tsx
│   └── package.json
├── docker-compose.yml     # PostgreSQL setup
├── .env.example
└── README.md
```

## API Endpoints

- `GET /api/feedback` - List feedback with filters
- `GET /api/feedback/{id}` - Get single feedback item
- `POST /api/feedback` - Create new feedback
- `POST /api/feedback/summarize` - Generate AI summary
- `GET /api/feedback/stats` - Get statistics

## Development

### Backend

- The backend uses FastAPI with automatic API documentation at `/docs`
- Database models are defined in `app/models.py`
- AI service uses Google Gemini API for sentiment analysis and summarization

### Frontend

- Built with Vite for fast development
- TypeScript for type safety
- Responsive design with modern CSS

## Troubleshooting

- **Database connection errors**: Ensure Docker Compose is running and PostgreSQL is up
- **API key errors**: Verify your Gemini API key is set correctly in `.env`
- **CORS errors**: Check that `CORS_ORIGINS` in `.env` includes your frontend URL

## Notes

- The seed script creates 32 sample feedback items with varied dates and sentiments
- Sentiment analysis runs automatically when creating new feedback
- The AI summary can handle up to 50 feedback items at once

