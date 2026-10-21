# SUPERSTORM AI

Superstorm AI is a real-time cryptocurrency intelligence and precision signal engine. It connects to Bybit WebSocket feeds to process low-latency order book and trade data, identifying structural and liquidity insights.

## Project Structure
- `backend/`: Python FastAPI service providing market data streaming, order book reconstruction, and signal intelligence.
- `frontend/`: Next.js React application offering a low-latency dashboard for real-time market data visualization.

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+

### Setup using Docker Compose (Recommended)
You can run the entire application using Docker Compose:
```bash
docker-compose up --build
```

### Local Development Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

For more architectural details, see `AGENTS.md`.
