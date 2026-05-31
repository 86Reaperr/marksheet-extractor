# Marksheet Extractor API

AI-powered marksheet extraction API built using FastAPI and Gemini LLM.

## Features

* PDF and Image support
* Gemini LLM-based extraction
* Structured JSON output
* Confidence scores for extracted fields
* JWT Authentication
* File validation and error handling
* FastAPI Swagger documentation

## Tech Stack

* Python
* FastAPI
* Gemini 2.5 Flash
* PyMuPDF
* Pillow
* JWT Authentication
* Render

## API Endpoints

### GET /

Returns API status.

### GET /health

Health check endpoint.

### GET /test-gemini

Tests Gemini connectivity.

### POST /token

Returns JWT access token.

### POST /extract

Uploads a marksheet and returns extracted JSON.

## Deployment

API URL:

https://marksheet-extractor-ogzj.onrender.com

Swagger Documentation:

https://marksheet-extractor-ogzj.onrender.com/docs

## Installation

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables

```env
GEMINI_API_KEY=your_api_key
JWT_SECRET_KEY=your_secret_key
```

## Confidence Scoring

Confidence scores range from 0.0 to 1.0 and are generated based on:

* Document clarity
* Field visibility
* Context consistency
* Gemini extraction certainty

## Author

Pranav Sharma
