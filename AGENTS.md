# SUPERSTORM AI Architecture & Developer Guide

## Architecture Overview
Superstorm AI is a real-time crypto intelligence and precision signal engine. The platform consists of two main parts:
- **Backend**: Python 3.10+ application built with FastAPI. It handles WebSocket ingestion of real-time market data from Bybit, maintains an in-memory order book, runs real-time order flow and execution calculations, and serves data to the frontend via WebSockets.
- **Frontend**: A React application built with Next.js and Tailwind CSS. It connects to the backend WebSocket streams to display live market conditions.

## Development Setup

### Backend (Python)
1. Navigate to the `backend` directory.
2. Create a virtual environment and activate it: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the backend locally: `uvicorn main:app --reload`

### Frontend (Next.js)
1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

### Tests
Run backend tests with `pytest` from the `backend` directory: `pytest tests/`

## Project Principles
- Real-time event-driven processing using WebSockets.
- No historical data polling for live signals; processing must react to live exchange events.
- Rigorous risk management and robust state validation.
