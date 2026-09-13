# AI Career Skill Gap & Course Recommendation System

An AI-powered career guidance application that analyzes a user's resume against a selected target job role, identifies missing skills, and recommends relevant learning resources to help bridge the skill gap.

The project combines **Natural Language Processing (NLP), semantic similarity, machine learning techniques, and a modern web application stack** to provide personalized career-development insights.

---

## Overview

Choosing the right skills to learn for a particular career can be difficult, especially when users are unsure about the gap between their current skills and the requirements of a target role.

This project addresses that problem by allowing users to:

1. Upload their resume in **PDF or DOCX format**
2. Select a target career role
3. Automatically extract technical skills from the resume
4. Compare existing skills with the requirements of the selected role
5. Calculate a career match percentage
6. Identify skills that need to be developed
7. Receive relevant course and learning-resource recommendations
8. Explore learning resources based on specific skills or topics

The system is designed to eventually support a broader course discovery experience where users can search for courses even without uploading a resume.

---

## Key Features

### Resume Analysis

Users can upload a resume directly through the web application.

Supported formats:

* PDF
* DOCX

The backend extracts the resume text and processes it using NLP techniques.

### Skill Extraction

The system identifies technical skills mentioned in the resume using a predefined skill taxonomy and normalization system.

Examples include:

* Python
* Java
* JavaScript
* SQL
* React
* Machine Learning
* Git
* Docker
* MongoDB
* Data Structures and Algorithms
* DBMS
* Operating Systems

Skill aliases are also normalized.

For example:

```text
ML → Machine Learning
JS → JavaScript
DSA → Data Structures and Algorithms
Mongo → MongoDB
```

### Target Job Roles

Users can select a target role from the available job-role dataset.

Currently supported roles include:

* Data Scientist
* Machine Learning Engineer
* Backend Developer
* Full Stack Developer
* Software Developer

Each role has a defined set of expected skills.

### Skill Gap Analysis

The system compares the skills extracted from the user's resume with the skills required for the selected role.

The results include:

* Total required skills
* Matched skills
* Missing skills
* Career match percentage

For example:

```text
Target Role: Data Scientist

Required Skills: 7
Matched Skills: 4
Missing Skills: 3

Career Match: 57.14%
```

### AI / Semantic Skill Matching

In addition to traditional keyword-based extraction, the project uses **sentence embeddings** to perform semantic similarity matching.

The current embedding model is:

```text
all-MiniLM-L6-v2
```

This allows the system to measure how semantically related resume content is to a particular skill.

The project therefore combines:

**Rule-based NLP + Semantic Similarity**

rather than relying only on exact keyword matching.

### Course Recommendation

After identifying missing skills, the system searches its course/resource dataset and ranks learning resources based on their relevance to the missing skill.

The recommendation system currently uses a hybrid score:

```text
Final Score =
0.7 × Explicit Skill Match
+
0.3 × Semantic Similarity
```

The weighting is currently a heuristic and is intended to be evaluated and improved as the project develops.

Recommendations are separated into:

* **Direct Matches** — resources that explicitly teach the missing skill
* **Related Resources** — resources that are semantically related to the missing skill

### Course Explorer

The planned Course Explorer allows users to search for learning resources without uploading a resume.

For example, a user could search for:

```text
Machine Learning
Python
SQL
React
Data Science
Statistics
```

The same semantic-ranking approach can then be used to rank relevant courses.

The course ecosystem is intended to include resources from platforms such as **Coursera and Udemy**, alongside other legitimate learning resources.

---

## Machine Learning / NLP Components

Machine learning is an important part of this project rather than simply an added chatbot feature.

### 1. Skill Extraction

The first layer uses:

* Skill taxonomy
* Skill aliases
* Text normalization
* Pattern matching

This provides reliable extraction of explicitly mentioned skills.

### 2. Sentence Embeddings

The project uses the `all-MiniLM-L6-v2` sentence-transformer model to convert text and skills into numerical embeddings.

These embeddings are compared using cosine similarity.

Conceptually:

```text
Resume Text
     ↓
Text Embedding
     ↓
Skill Embedding
     ↓
Cosine Similarity
     ↓
Semantic Relevance
```

### 3. Hybrid Course Ranking

Course recommendations combine:

* Explicit skill matching
* Semantic similarity

This allows the system to prioritize resources that directly teach a required skill while still finding useful related resources.

### 4. Future ML Evaluation

The recommendation and semantic-matching components can be evaluated using metrics such as:

* Precision
* Recall
* F1-score
* Precision@K
* Recall@K
* NDCG@K

Different weighting strategies can also be compared to determine which ranking approach provides the most relevant recommendations.

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │      React UI       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      Resume Parser      Skill Extraction    Job Roles
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                     ┌──────────────────┐
                     │   Skill Gap      │
                     │    Analysis      │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Course Ranking    │
                     │  Semantic +      │
                     │ Explicit Match   │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Recommendations  │
                     └──────────────────┘
```

---

## Technology Stack

### Frontend

* React
* Vite
* JavaScript
* Recharts
* CSS

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

### NLP / Machine Learning

* Sentence Transformers
* `all-MiniLM-L6-v2`
* Scikit-learn
* Cosine similarity
* Rule-based NLP / skill extraction

### Resume Processing

* PyMuPDF
* python-docx

### Development Tools

* Git
* GitHub
* VS Code

### Planned Database Layer

The project contains a database architecture foundation using:

* SQLAlchemy
* Alembic
* PostgreSQL

Database persistence is planned for a later stage of development.

---

## API Endpoints

### Health Check

```http
GET /api/health
```

Checks whether the backend is running.

### Job Roles

```http
GET /api/jobs
```

Returns the available job roles.

```http
GET /api/jobs/{job_role_id}
```

Returns a specific job role.

### Skill Extraction

```http
POST /api/skills/extract
```

Extracts skills from supplied text.

### Skill Gap

```http
POST /api/jobs/skill-gap
```

Calculates the skill gap between a user's skills and a selected job role.

### Courses

```http
GET /api/courses
```

Returns available learning resources.

```http
GET /api/courses/skill/{skill}
```

Returns resources associated with a particular skill.

```http
GET /api/courses/{course_id}
```

Returns a specific course/resource.

### Career Analysis

```http
POST /api/career-analysis
```

Performs career analysis using supplied resume text.

### Resume Upload + Career Analysis

```http
POST /api/career-analysis/upload
```

Accepts a PDF/DOCX resume and performs the complete analysis pipeline.

---

## Application Flow

```text
User Uploads Resume
        ↓
Resume Text Extraction
        ↓
NLP Skill Extraction
        ↓
Skill Normalization
        ↓
Target Job Selection
        ↓
Required vs Existing Skills
        ↓
Skill Gap Calculation
        ↓
Missing Skills Identified
        ↓
Semantic Course Ranking
        ↓
Personalized Recommendations
```

---

## Example

A user selects:

```text
Target Role: Data Scientist
```

and uploads a resume containing:

```text
Python
SQL
Machine Learning
Data Visualization
Git
Java
MongoDB
```

The system compares these skills against the expected Data Scientist skill set.

Example result:

```text
Career Match: 57.14%

Skills You Have:
✓ Python
✓ SQL
✓ Machine Learning
✓ Data Visualization

Skills to Develop:
⚠ Statistics
⚠ Pandas
⚠ NumPy
```

The system then recommends learning resources relevant to the missing skills.

---

## Project Structure

```text
career-skill-gap/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── data/
│   │   ├── ml/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── tests/
│   ├── alembic/
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── ...
│
└── README.md
```

---

## Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/JoannBinny/Career_skill_gap.git
cd Career_skill_gap
```

### 2. Start the Backend

Navigate to the backend:

```bash
cd backend
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### 3. Start the Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## Current Development Status

### Completed

* [x] FastAPI backend setup
* [x] React frontend setup
* [x] Resume PDF parsing
* [x] Resume DOCX parsing
* [x] Skill taxonomy
* [x] Skill normalization
* [x] Baseline NLP skill extraction
* [x] Sentence-transformer semantic matching
* [x] Hybrid skill analysis
* [x] Job-role dataset
* [x] Skill-gap calculation
* [x] Course/resource dataset
* [x] Semantic course ranking
* [x] Hybrid course ranking
* [x] End-to-end career analysis
* [x] Resume upload endpoint
* [x] React job-role selection
* [x] Resume upload interface
* [x] Career analysis results UI
* [x] Skill match visualization
* [x] Course recommendation UI
* [x] Recharts integration

### In Progress / Planned

* [ ] General Course Explorer
* [ ] Expanded real-world course dataset
* [ ] Coursera course integration
* [ ] Udemy course integration
* [ ] Course search and filtering
* [ ] Improved semantic search
* [ ] ML recommendation evaluation
* [ ] PostgreSQL persistence
* [ ] User accounts
* [ ] Learning-progress tracking
* [ ] Improved job-role dataset
* [ ] Production deployment

---

## Future Improvements

Several components can be extended as the project matures.

### Larger Course Dataset

The current development dataset can be expanded to include a much larger collection of real learning resources from platforms such as Coursera and Udemy.

### Improved Job-Skill Data

The current job-role dataset can eventually be replaced or supplemented with standardized occupational and skill datasets such as O*NET or ESCO.

### Personalized Recommendations

Future versions could consider:

* User experience level
* Course difficulty
* Learning preferences
* Course ratings
* Course duration
* Previously completed courses
* Learning progress

### Recommendation Model Evaluation

The ranking system can be evaluated using human relevance judgments and ranking metrics such as Precision@K and NDCG@K.

### Database Integration

A PostgreSQL database can eventually store:

* Users
* Resumes
* Skills
* Job roles
* Courses
* Skill gaps
* Recommendations
* Learning progress

---

## Why This Project?

The project demonstrates how AI and NLP can be applied to a practical career-development problem.

Instead of simply generating generic career advice, the system attempts to create a measurable pipeline:

```text
Current Skills
      ↓
Target Career
      ↓
Skill Gap
      ↓
Learning Recommendations
      ↓
Career Development
```

This makes the project useful as both a **career guidance application** and a demonstration of practical **NLP, semantic similarity, recommendation systems, and full-stack development**.

---

## License

This project is developed for educational and portfolio purposes.
