# The Ballot Journey 🗳️

**The Ballot Journey** is an interactive, civic education web application designed to help users understand election processes, test their civic knowledge, and answer complex governance questions using advanced AI.

Powered by Google's **Gemini 2.5 Flash**, the application provides dynamic questions and functions as an intelligent "Civic Guide" chatbot. 

## Features 🚀

- **Civic Quiz Generator:** Generates dynamic, AI-powered questions focusing on election processes and civic duties to test your knowledge.
- **The Civic Guide (Chatbot):** A conversational AI assistant natively integrated to answer any questions regarding voting procedures, political systems, and the Constitution.
- **Document Scanner:** Interactive flow designed to emulate voting verification tasks.
- **Sleek Aesthetic:** Beautiful, responsive UI specifically themed around civic responsibility and smooth UX.

## Tech Stack 🛠️

- **Frontend:** Pure HTML5, Vanilla JavaScript, and CSS (Single File Architecture)
- **Backend (Local Dev):** Python 3 HTTP Server (`http.server` with dynamic environment variable injection)
- **AI Integration:** Google Gemini API (`generativelanguage.googleapis.com`)
- **Deployment:** Docker & Nginx deployed onto Google Cloud Run

## Getting Started ⚙️

### Prerequisites
- Python 3.x installed
- A Google Gemini API Key

### Local Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/Praveen23-kk/PromtWars_2_Elections.git
   cd PromtWars_2_Elections
   ```
2. Create a `.env` file in the root directory and add your API key:
   ```text
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. Run the local development server:
   ```bash
   python server.py
   ```
   *The local server automatically reads the `.env` file and securely injects the API key into the frontend.*
4. Open your browser and navigate to `http://localhost:8001`.

## Deployment ☁️

This application is configured for deployment on **Google Cloud Run** using a custom Dockerfile with an Nginx reverse proxy. 

1. Ensure the Google Cloud SDK is initialized and you are authenticated.
2. Ensure the `generativelanguage.googleapis.com` API is enabled on your target GCP project.
3. Deploy directly using the Cloud Run CLI:
   ```bash
   gcloud run deploy ballot-journey --source . --port 8080 --set-env-vars="GEMINI_API_KEY=your_gemini_api_key_here" --region us-central1 --allow-unauthenticated
   ```

## Repository Structure 📂

- `index.html`: The core frontend rendering the ballot experiences, UI, and interactions.
- `server.py`: A local python server that acts as a secure intermediary to inject the API key during local development.
- `Dockerfile`: Multi-stage build instructions to serve the HTML via Nginx in production.
- `nginx.conf`: Routing instructions for Nginx.
- `cloudbuild.yaml`: Pre-configured CI/CD pipeline script for GCP.
