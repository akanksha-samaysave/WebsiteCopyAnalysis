# 📊 Landing Page Intelligence & CRO Analyzer

A complete production-ready full-stack application for analyzing landing pages using advanced UX principles, copywriting psychology, conversion rate optimization (CRO), and trust signal detection.

## 🚀 Features

### Core Analysis Engines

- **Web Scraper Service** - Playwright-based page scraping with JS rendering
- **Section Detection** - Automatic detection of page sections (Hero, Problem, Solution, Benefits, Features, Testimonials, Pricing, FAQ, CTA)
- **Copywriting Analysis** - Scoring for:
  - Headline strength
  - Emotional triggers (pain, desire, urgency)
  - Value proposition clarity
  - Features vs benefits ratio
  - CTA strength
  
- **UX Analysis** - Evaluation of:
  - Readability
  - Visual hierarchy
  - Mobile responsiveness
  - Information density
  - Conversion friction
  
- **Trust Engine** - Detection of:
  - Social proof signals
  - Authority indicators
  - Security & privacy signals
  - Credibility guarantees
  
- **Scoring & Ranking** - Weighted scoring system:
  - Design (15%)
  - Messaging (25%)
  - Trust (20%)
  - Clarity (15%)
  - Conversion (15%)
  - UX (10%)

- **Recommendation Engine** - Generates 5-10 actionable CRO improvements
- **PDF Report Generation** - Comprehensive analysis reports
- **Comparison Dashboard** - Side-by-side website comparison

### Frontend Features

- **Modern React UI** - Built with React 18 + Vite
- **Real-time Analysis** - Live progress tracking
- **Interactive Dashboards** - Score cards, radar charts, comparison charts
- **Dark Mode Design** - Professional SaaS-style interface
- **Responsive Layout** - Mobile-friendly design
- **Multiple Pages**:
  - Home/Analysis page
  - Individual dashboard per website
  - Comparison view across multiple sites

## 📁 Project Structure

```
landing-page-intelligence/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app
│   │   ├── database.py             # SQLAlchemy setup
│   │   ├── models/                 # Database models
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   ├── routers/                # API routes
│   │   │   ├── __init__.py
│   │   │   └── analysis.py
│   │   ├── services/               # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── web_scraper_service.py
│   │   │   ├── section_detector_service.py
│   │   │   ├── copywriting_analyzer_service.py
│   │   │   ├── ux_analyzer_service.py
│   │   │   ├── trust_analyzer_service.py
│   │   │   ├── scoring_service.py
│   │   │   ├── recommendation_service.py
│   │   │   └── pdf_report_service.py
│   │   └── utils/                  # Helper functions
│   │       ├── __init__.py
│   │       └── helpers.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── pages/                  # React pages
│   │   │   ├── HomePage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── ComparisonPage.jsx
│   │   │   └── index.js
│   │   ├── components/             # React components
│   │   │   ├── Cards.jsx
│   │   │   ├── Charts.jsx
│   │   │   ├── Layout.jsx
│   │   │   ├── URLInput.jsx
│   │   │   └── index.js
│   │   ├── services/               # API services
│   │   │   └── api.js
│   │   ├── hooks/                  # Custom hooks
│   │   │   └── useAnalysis.js
│   │   ├── App.jsx                 # Main component
│   │   ├── main.jsx                # Entry point
│   │   └── index.css               # Tailwind styles
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── index.html
├── .gitignore
└── README.md
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **SQLAlchemy** - ORM for database
- **SQLite** - Database (easily swappable)
- **Playwright** - Browser automation for scraping
- **BeautifulSoup4** - HTML parsing
- **Pandas & NumPy** - Data manipulation
- **spaCy** - NLP
- **TextBlob** - Sentiment analysis
- **VaderSentiment** - Sentiment scoring
- **scikit-learn** - Machine learning utilities
- **ReportLab** - PDF generation

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **Lucide React** - Icons
- **React Router** - Client-side routing

### DevOps
- **Docker** - Containerization
- **docker-compose** - Multi-container orchestration

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose (recommended)
- OR Python 3.11+ & Node.js 18+

### Quick Start with Docker

1. **Clone the repository**
```bash
cd landing-page-intelligence
```

2. **Copy environment variables**
```bash
cp .env.example .env
```

3. **Build and run all services**
```bash
docker-compose up --build
```

4. **Open the app**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

5. **Stop the app**
```bash
docker-compose down
```

### Manual Setup

#### Backend Setup

1. **Create Python virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers**
```bash
playwright install chromium
```

4. **Download spaCy model**
```bash
python -m spacy download en_core_web_sm
```

5. **Run the backend**
```bash
python run.py
```

Backend will run on http://localhost:8000

#### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Start development server**
```bash
npm run dev
```

Frontend will run on http://localhost:3000

## 📝 API Documentation

### Endpoints

#### 1. Start Analysis
```
POST /api/analyze
Content-Type: application/json

{
  "urls": [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
  ]
}

Response:
{
  "job_id": "abc123",
  "status": "pending",
  "urls_count": 3
}
```

#### 2. Get Analysis Results
```
GET /api/analysis/{job_id}

Response:
{
  "job_id": "abc123",
  "all_completed": true,
  "results": [
    {
      "website_url": "https://example1.com",
      "status": "completed",
      "scores": [
        {
          "category": "design",
          "score": 8.5
        },
        ...
      ],
      "recommendations": [
        {
          "priority": "High",
          "title": "Improve headline strength",
          "description": "...",
          "reasoning": "...",
          "category": "copywriting"
        },
        ...
      ],
      "metadata": {
        "copy_scores": {...},
        "ux_scores": {...},
        "trust_scores": {...},
        "category_scores": {...},
        "overall_score": 75.5,
        "sections": {...}
      }
    }
  ]
}
```

#### 3. Get Comparison
```
GET /api/comparison/{job_id}

Response:
{
  "job_id": "abc123",
  "websites": [
    {
      "url": "https://example1.com",
      "domain": "example1.com",
      "overall_score": 85,
      "scores": {
        "design": 8.5,
        "messaging": 7.5,
        "trust": 9.0,
        ...
      }
    },
    ...
  ],
  "ranking": [...],
  "best_category": {
    "category": "trust",
    "average_score": 8.5
  },
  "worst_category": {
    "category": "ux",
    "average_score": 5.5
  }
}
```

#### 4. Generate Report
```
POST /api/report/{job_id}

Response:
{
  "pdf_path": "/app/reports/abc123.pdf",
  "download_url": "/api/report-download/abc123",
  "generated_at": "2024-01-15T10:30:00"
}
```

#### 5. Download Report
```
GET /api/report-download/{job_id}

Returns: PDF file
```

#### 6. Health Check
```
GET /api/health

Response:
{
  "status": "healthy"
}
```

## 📊 Database Schema

### Website
- `id` (Integer, Primary Key)
- `url` (String, Unique)
- `domain` (String)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Analysis
- `id` (Integer, Primary Key)
- `job_id` (String, Unique, Index)
- `website_id` (Foreign Key)
- `status` (String) - pending, processing, completed, failed
- `raw_html` (Text)
- `visible_text` (Text)
- `sections` (JSON)
- `metadata` (JSON)
- `error_message` (String)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Score
- `id` (Integer, Primary Key)
- `analysis_id` (Foreign Key)
- `category` (String) - design, messaging, trust, clarity, conversion, ux
- `score` (Float, 0-10)
- `details` (JSON)
- `created_at` (DateTime)

### Recommendation
- `id` (Integer, Primary Key)
- `analysis_id` (Foreign Key)
- `priority` (String) - High, Medium, Low
- `title` (String)
- `description` (Text)
- `reasoning` (Text)
- `category` (String)
- `created_at` (DateTime)

### Report
- `id` (Integer, Primary Key)
- `analysis_id` (Foreign Key)
- `pdf_path` (String)
- `csv_path` (String)
- `generated_at` (DateTime)

### Screenshot
- `id` (Integer, Primary Key)
- `website_id` (Foreign Key)
- `file_path` (String)
- `created_at` (DateTime)

## 🔧 Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```env
# Backend
DATABASE_URL=sqlite:///./analytics.db
PYTHONUNBUFFERED=1

# Frontend
REACT_APP_API_URL=http://localhost:8000
VITE_API_URL=http://localhost:8000
```

## 📈 Scoring Methodology

### Category Weights
- **Design** (15%) - Visual hierarchy + Mobile responsiveness
- **Messaging** (25%) - Headline + Value proposition + Features vs Benefits + CTA
- **Trust** (20%) - Social proof + Authority + Security + Credibility
- **Clarity** (15%) - Readability + Information density
- **Conversion** (15%) - CTA strength + Conversion friction + Emotional triggers
- **UX** (10%) - Average of all UX metrics

### Overall Score Calculation
```
Overall Score = Sum(Category Score × Category Weight)
Overall % = Overall Score × 10 (Scale to 0-100)
```

## 🎯 Example Use Cases

1. **Website Owner** - Analyze own landing page to improve conversions
2. **Marketer** - Compare competitor pages
3. **SaaS Founder** - Track landing page improvements over time
4. **Conversion Specialist** - Get data-driven CRO recommendations
5. **Agency** - Analyze client landing pages

## 🔐 Security Considerations

- CORS enabled for localhost (configure for production)
- Input validation on all endpoints
- SQL injection protection via SQLAlchemy ORM
- File path sanitization for reports
- Environment variables for sensitive config

## 📝 Testing the Application

### Test URLs (Public landing pages)
```
https://www.uber.com
https://www.airbnb.com
https://www.stripe.com
https://www.figma.com
https://www.slack.com
```

### Expected Behavior
1. Submit URLs from home page
2. See real-time analysis progress
3. View detailed dashboard with scores
4. Compare multiple sites
5. Download PDF report

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use**
```bash
# Change port in docker-compose.yml or run.py
```

**Database errors**
```bash
# Remove database file and restart
rm analytics.db
```

**Playwright browser issues**
```bash
playwright install chromium
```

### Frontend Issues

**Port 3000 already in use**
```bash
# Change port in vite.config.js
```

**API connection errors**
```bash
# Check backend is running: curl http://localhost:8000/health
# Update API_BASE_URL in services/api.js if needed
```

## 📚 Documentation

- **API Docs** - http://localhost:8000/docs (Swagger UI)
- **OpenAPI Schema** - http://localhost:8000/openapi.json

## 🚀 Production Deployment

### Using Docker in Production

1. **Build images**
```bash
docker-compose build
```

2. **Run containers**
```bash
docker-compose up -d
```

3. **Setup reverse proxy** (nginx)
```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:3000;
}

server {
    listen 80;
    server_name example.com;

    location /api {
        proxy_pass http://backend;
    }

    location / {
        proxy_pass http://frontend;
    }
}
```

4. **Use PostgreSQL instead of SQLite**
```python
# In database.py
DATABASE_URL = "postgresql://user:password@db:5432/analytics"
```

5. **Setup SSL with Let's Encrypt**
```bash
certbot certonly --standalone -d example.com
```

## 📊 Performance Optimization

- Async web scraping for parallel analysis
- Database indexing on frequently queried fields
- PDF generation as background task
- Frontend code splitting and lazy loading
- Caching of analysis results

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes

## 🙏 Acknowledgments

- Playwright for browser automation
- ReportLab for PDF generation
- Recharts for beautiful charts
- TailwindCSS for styling

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Open an issue on GitHub

---

**Built with ❤️ for conversion optimization professionals**
