# ExoQuery
ExoQuery is an AI agent designed to interface with NASA's Exoplanet Archive data to quickly answer any questions surrounding this complex dataset.

## Live Demo
In the future, you will be able to interact with the ExoQuery chatbot on [exoquery.lmiller.io](exoquery.lmiller.io) hosted by Streamlit, but since this is a working project, this is not yet implemented! Come back later to see this in action!

## Components
### 1. API Data Fetch
Uses Python requests to query a JSON string which gets stored into an sqlite database.
### 2. Additional Views
Build on top of the mostly-raw data to create additional, more structured tables. This also means that the agent never needs to interact directly with the API to get data.