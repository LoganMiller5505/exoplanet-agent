# ExoQuery
ExoQuery is an AI agent designed to interface with NASA's Exoplanet Archive data to quickly answer any questions surrounding this complex dataset.

## Live Demo
You can currently talk with the ExoQuery chatbot on [exoquery.lmiller.io](exoquery.lmiller.io). Be patient, as it is using a free model which is subject to rate limiting. Feel free to test its knowledge and discover the kinds of data it can access!

## Components
### 1. API Data Fetch
`ingest/api.py` uses Python requests to pull 11 tables from the archive's TAP service and store them in a Neon Postgres database.
### 2. Views
`transforms/views/` builds structured views on top of the mostly-raw data — planets, systems, name aliases, size and orbit classes, habitable zone boundaries, and unconfirmed candidates. This also means the agent never needs to interact directly with the API to get data.
### 3. Orchestration
GitHub Actions re-runs the ingest daily and re-applies the views whenever their SQL changes.
### 4. Agent with Tooling
Utilizes the Groq API free-tier and four predefined tools which interface with the views to answer user questions regarding exoplanets. The model never writes SQL itself.
### 5. Streamlit App
A helpful chat interface is provided for users to easily ask questions. Run it with `streamlit run agent/app.py`, with `DATABASE_URL` and `GROQ_API_KEY` set in a `.env` file locally, or go to [exoquery.lmiller.io](exoquery.lmiller.io)!
