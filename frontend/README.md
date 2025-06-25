# Patient Reported Outcomes Multi-Agent System - Frontend Application

This directory contains the frontend web application for the PROPER platform, built with [React](https://reactjs.org/) and `create-react-app`.

## Features

-   User-friendly interface for patient login.
-   Interactive chat-like experience for agent communication.
-   Responsive design for use on various devices.

## Prerequisites

-   Node.js (v18.x or later)
-   `npm` or `yarn`

## Local Development Setup

### 1. Navigate to the Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
```

### 3. Configure Environment Variables

Create a `.env` file in this directory by copying `.env.local.example`. Edit the file and set `REACT_APP_API_URL` to point to your running backend instance. `create-react-app` requires environment variables to be prefixed with `REACT_APP_`.

**Example `.env`:**
`REACT_APP_API_URL=http://localhost:8000`

### 4. Run the Development Server

```bash
npm run dev
# or
yarn start
```

Open http://localhost:3000 with your browser to see the result.
