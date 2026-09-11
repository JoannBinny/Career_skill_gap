import { useEffect, useState } from "react";
import {
PieChart,
Pie,
Cell,
Tooltip,
Legend,
ResponsiveContainer,
} from "recharts";

import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
const [resume, setResume] = useState(null);
const [jobRole, setJobRole] = useState("");
const [jobRoles, setJobRoles] = useState([]);
const [loadingRoles, setLoadingRoles] = useState(true);
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");
const [analysisResult, setAnalysisResult] = useState(null);

useEffect(() => {
const fetchJobRoles = async () => {
try {
setLoadingRoles(true);

    const response = await fetch(`${API_BASE_URL}/api/jobs`);

    if (!response.ok) {
      throw new Error("Failed to load job roles.");
    }

    const data = await response.json();
    setJobRoles(data.job_roles || []);
  } catch (fetchError) {
    console.error("Error fetching job roles:", fetchError);
    setError(
      "Unable to load career roles. Make sure the FastAPI backend is running."
    );
  } finally {
    setLoadingRoles(false);
  }
};

fetchJobRoles();


}, []);

const handleResumeChange = (event) => {
const file = event.target.files?.[0];


if (!file) {
  return;
}

const extension = file.name.split(".").pop()?.toLowerCase();

if (!["pdf", "docx"].includes(extension)) {
  setError("Please upload a PDF or DOCX resume.");
  return;
}

setResume(file);
setError("");
setAnalysisResult(null);


};

const handleRemoveResume = () => {
setResume(null);
setAnalysisResult(null);
setError("");
};

const handleAnalyze = async () => {
if (!resume || !jobRole) {
return;
}

setLoading(true);
setError("");
setAnalysisResult(null);

const formData = new FormData();

formData.append("resume", resume);
formData.append("job_role_id", jobRole);
formData.append("courses_per_skill", "3");

try {
  const response = await fetch(
    `${API_BASE_URL}/api/career-analysis/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Career analysis failed.");
  }

  setAnalysisResult(data);

  setTimeout(() => {
    document
      .getElementById("results")
      ?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 100);
} catch (analysisError) {
  console.error("Career analysis error:", analysisError);
  setError(
    analysisError.message ||
      "Something went wrong while analyzing your resume."
  );
} finally {
  setLoading(false);
}


};

const getMatchLabel = (percentage) => {
if (percentage >= 80) {
return "Strong match";
}


if (percentage >= 60) {
  return "Good foundation";
}

if (percentage >= 40) {
  return "Promising start";
}

return "Needs development";


};

const getCourseTypeLabel = (course) => {
return course.explicit_match ? "DIRECT MATCH" : "RELATED RESOURCE";
};

const chartData = analysisResult
? [
{
name: "Matched Skills",
value: analysisResult.matched_skills.length,
},
{
name: "Missing Skills",
value: analysisResult.missing_skills.length,
},
]
: [];

return ( <div className="app"> <header className="navbar"> <a href="#dashboard" className="logo"> <span className="logo-mark">CG</span> <span>CareerGap AI</span> </a>


    <nav className="navbar-links">
      <a href="#dashboard">Dashboard</a>
      <a href="#how-it-works">How It Works</a>
      <a href="#features">Features</a>
    </nav>

    <a href="#dashboard" className="navbar-cta">
      Start Analysis
      <span>→</span>
    </a>
  </header>

  <main>
    <section className="dashboard-section" id="dashboard">
      <div className="dashboard-heading">
        <div className="heading-content">
          <span className="badge">AI CAREER ANALYSIS</span>

          <h1>
            Find the skills you need
            <span> to reach your next role.</span>
          </h1>

          <p>
            Upload your resume and select a target career. CareerGap AI
            analyzes your current skills, identifies gaps, and recommends
            learning resources to help you move forward.
          </p>
        </div>

        <div className="heading-stat">
          <strong>01</strong>
          <span>Resume → Skills → Gap → Learning</span>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="analysis-panel">
          <div className="panel-header">
            <div className="panel-title">
              <span className="panel-number">01</span>

              <div>
                <h2>Upload your resume</h2>
                <p>We'll extract relevant skills from your document.</p>
              </div>
            </div>

            <span className="file-type">PDF / DOCX</span>
          </div>

          <label className="upload-area">
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleResumeChange}
            />

            <div className="upload-icon">
              <span>↑</span>
            </div>

            <strong>
              {resume ? resume.name : "Choose your resume"}
            </strong>

            <span>
              {resume
                ? `${(resume.size / 1024 / 1024).toFixed(2)} MB`
                : "Click to browse or drag your file here"}
            </span>
          </label>

          {resume && (
            <div className="selected-file">
              <div className="selected-file-icon">✓</div>

              <div className="selected-file-info">
                <strong>Resume selected</strong>
                <span>{resume.name}</span>
              </div>

              <button
                type="button"
                onClick={handleRemoveResume}
                className="remove-button"
              >
                Remove
              </button>
            </div>
          )}

          <div className="role-section">
            <div className="panel-header">
              <div className="panel-title">
                <span className="panel-number">02</span>

                <div>
                  <h2>Choose your target role</h2>
                  <p>We'll compare your skills against this career.</p>
                </div>
              </div>
            </div>

            <label className="select-wrapper">
              <span>Target career</span>

              <select
                value={jobRole}
                onChange={(event) => {
                  setJobRole(event.target.value);
                  setAnalysisResult(null);
                  setError("");
                }}
                disabled={loadingRoles || loading}
              >
                <option value="">
                  {loadingRoles
                    ? "Loading career roles..."
                    : "Select a career"}
                </option>

                {jobRoles.map((role) => (
                  <option key={role.id} value={role.id}>
                    {role.title}
                  </option>
                ))}
              </select>
            </label>
          </div>

          {error && (
            <div className="error-message">
              <span>!</span>
              <p>{error}</p>
            </div>
          )}

          <button
            type="button"
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={!resume || !jobRole || loading}
          >
            <span>
              {loading ? "Analyzing your resume..." : "Analyze My Resume"}
            </span>

            <span className="button-arrow">
              {loading ? "•••" : "→"}
            </span>
          </button>

          <div className="privacy-note">
            <span>✓</span>
            <p>Your resume is processed only for this analysis.</p>
          </div>
        </div>

        <aside className="preview-panel">
          {analysisResult ? (
            <>
              <div className="preview-top">
                <span className="panel-number">ANALYSIS</span>
                <span className="preview-status complete">COMPLETE</span>
              </div>

              <div className="preview-complete">
                <div className="preview-score">
                  <strong>{analysisResult.match_percentage}%</strong>
                  <span>career match</span>
                </div>

                <span className="preview-role">
                  {analysisResult.job_role.title}
                </span>

                <h2>{getMatchLabel(analysisResult.match_percentage)}</h2>

                <p>
                  Your resume currently matches{" "}
                  {analysisResult.matched_skills.length} of{" "}
                  {analysisResult.matched_skills.length +
                  analysisResult.missing_skills.length} required skills
                  for this role.
                </p>
              </div>

              <div className="preview-items">
                <div>
                  <span>01</span>
                  <strong>
                    {analysisResult.extracted_skills.length} detected
                  </strong>
                  <small>Skills found in resume</small>
                </div>

                <div>
                  <span>02</span>
                  <strong>
                    {analysisResult.missing_skills.length} to develop
                  </strong>
                  <small>Skills missing for role</small>
                </div>

                <div>
                  <span>03</span>
                  <strong>
                    {analysisResult.recommendations.length} skill areas
                  </strong>
                  <small>Learning recommendations</small>
                </div>
              </div>
            </>
          ) : (
            <>
              <div className="preview-top">
                <span className="panel-number">PREVIEW</span>
                <span className="preview-status">READY</span>
              </div>

              <div className="preview-empty">
                <div className="preview-orb">
                  <span>✦</span>
                </div>

                <h2>Your analysis will appear here.</h2>

                <p>
                  Once your resume is analyzed, you'll see your current
                  skills, target-role requirements, skill gaps, and
                  recommended learning resources.
                </p>
              </div>

              <div className="preview-items">
                <div>
                  <span>01</span>
                  <strong>Skills detected</strong>
                  <small>NLP-based extraction</small>
                </div>

                <div>
                  <span>02</span>
                  <strong>Skill gap</strong>
                  <small>Target role comparison</small>
                </div>

                <div>
                  <span>03</span>
                  <strong>Learning path</strong>
                  <small>ML-ranked resources</small>
                </div>
              </div>
            </>
          )}
        </aside>
      </div>
    </section>

    {analysisResult && (
      <section className="results-section" id="results">
        <div className="section-heading results-heading">
          <span className="badge">YOUR RESULTS</span>

          <h2>Your career gap analysis.</h2>

          <p>
            Here's how your current resume compares with the requirements
            for{" "}
            <strong>{analysisResult.job_role.title}</strong>.
          </p>
        </div>

        <div className="results-preview">
          <div className="result-header">
            <div>
              <span className="result-label">TARGET ROLE</span>
              <h2>{analysisResult.job_role.title}</h2>
            </div>

            <span className="badge success-badge">
              Analysis Complete
            </span>
          </div>

          <div className="match-score">
            <div className="match-score-info">
              <span>Career Match</span>

              <p>
                How closely your current skills match this role's
                requirements.
              </p>

              <div className="match-progress">
                <div
                  style={{
                    width: `${Math.min(
                      analysisResult.match_percentage,
                      100
                    )}%`,
                  }}
                />
              </div>
            </div>

            <div className="match-score-value">
              <strong>{analysisResult.match_percentage}%</strong>
              <span>{getMatchLabel(analysisResult.match_percentage)}</span>
            </div>
          </div>

          <div className="skill-summary">
            <div className="summary-card">
              <span>Total Required</span>
              <strong>{analysisResult.matched_skills.length +
analysisResult.missing_skills.length}</strong>
              <small>Skills for this role</small>
            </div>

            <div className="summary-card matched-summary">
              <span>Matched</span>
              <strong>{analysisResult.matched_skills.length}</strong>
              <small>Skills you already have</small>
            </div>

            <div className="summary-card missing-summary">
              <span>Missing</span>
              <strong>{analysisResult.missing_skills.length}</strong>
              <small>Skills to develop</small>
            </div>
          </div>

          <div className="chart-section">
            <div className="chart-heading">
              <div>
                <span className="result-label">SKILL BREAKDOWN</span>
                <h3>Skill Gap Overview</h3>
              </div>

              <span className="chart-total">
                {analysisResult.matched_skills.length +
analysisResult.missing_skills.length} required
              </span>
            </div>

            <div className="chart-container">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={chartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={72}
                    outerRadius={105}
                    paddingAngle={4}
                    dataKey="value"
                    labelLine={false}
                    label={({ percent }) =>
                      `${Math.round(percent * 100)}%`
                    }
                  >
                    <Cell fill="#5964d9" />
                    <Cell fill="#f59e0b" />
                  </Pie>

                  <Tooltip
                    formatter={(value) => [`${value} skills`, "Count"]}
                  />

                  <Legend
                    verticalAlign="bottom"
                    height={30}
                    iconType="circle"
                  />
                </PieChart>
              </ResponsiveContainer>

              <div className="chart-center">
                <strong>{analysisResult.match_percentage}%</strong>
                <span>matched</span>
              </div>
            </div>
          </div>

          <div className="result-section">
            <div className="result-section-header">
              <div>
                <span className="result-label">RESUME ANALYSIS</span>
                <h3>Skills Detected</h3>
              </div>

              <span className="count-pill">
                {analysisResult.extracted_skills.length}
              </span>
            </div>

            <p className="section-description">
              Technical skills identified from your resume.
            </p>

            <div className="skill-list">
              {analysisResult.extracted_skills.map((skill) => (
                <span key={skill} className="skill-tag">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div className="result-section">
            <div className="result-section-header">
              <div>
                <span className="result-label">STRENGTHS</span>
                <h3>Skills You Already Have</h3>
              </div>

              <span className="count-pill matched-pill">
                {analysisResult.matched_skills.length}
              </span>
            </div>

            <p className="section-description">
              These skills directly match the requirements of your target
              role.
            </p>

            <div className="skill-list">
              {analysisResult.matched_skills.map((skill) => (
                <span key={skill} className="skill-tag matched">
                  <span>✓</span>
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div className="result-section">
            <div className="result-section-header">
              <div>
                <span className="result-label">OPPORTUNITIES</span>
                <h3>Skills to Develop</h3>
              </div>

              <span className="count-pill missing-pill">
                {analysisResult.missing_skills.length}
              </span>
            </div>

            <p className="section-description">
              Developing these skills will improve your match for the
              selected role.
            </p>

            <div className="skill-list">
              {analysisResult.missing_skills.map((skill) => (
                <span key={skill} className="skill-tag missing">
                  <span>!</span>
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div className="recommendations-section">
            <div className="recommendations-heading">
              <div>
                <span className="result-label">PERSONALIZED LEARNING</span>
                <h3>Recommended Learning</h3>
                <p>
                  Resources ranked according to your missing skills using
                  semantic similarity and hybrid recommendation scores.
                </p>
              </div>
            </div>

            <div className="recommendations-list">
              {analysisResult.recommendations.map((recommendation) => (
                <div
                  key={recommendation.missing_skill}
                  className="recommendation-group"
                >
                  <div className="recommendation-skill">
                    <span>Focus area</span>
                    <h4>{recommendation.missing_skill}</h4>
                  </div>

                  {recommendation.direct_recommendations.map((course) => (
                    <div key={course.id} className="course-card">
                      <div className="course-card-top">
                        <span className="course-type direct">
                          {getCourseTypeLabel(course)}
                        </span>

                        <span className="course-score">
                          {course.final_score.toFixed(2)} score
                        </span>
                      </div>

                      <div className="course-card-content">
                        <h5>{course.title}</h5>

                        <p className="course-provider">
                          {course.provider}
                        </p>

                        <p className="course-explanation">
                          {course.explanation}
                        </p>

                        <div className="course-metrics">
                          <span>
                            Semantic{" "}
                            <strong>
                              {course.similarity.toFixed(4)}
                            </strong>
                          </span>

                          <span>
                            Hybrid{" "}
                            <strong>
                              {course.final_score.toFixed(4)}
                            </strong>
                          </span>
                        </div>
                      </div>

                      <a
                        href={course.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="course-link"
                      >
                        <span>Open Resource</span>
                        <span>↗</span>
                      </a>
                    </div>
                  ))}

                  {recommendation.related_recommendations.map(
                    (course) => (
                      <div
                        key={course.id}
                        className="course-card related"
                      >
                        <div className="course-card-top">
                          <span className="course-type related-type">
                            {getCourseTypeLabel(course)}
                          </span>

                          <span className="course-score">
                            {course.similarity.toFixed(2)} similarity
                          </span>
                        </div>

                        <div className="course-card-content">
                          <h5>{course.title}</h5>

                          <p className="course-provider">
                            {course.provider}
                          </p>

                          <p className="course-explanation">
                            {course.explanation}
                          </p>

                          <div className="course-metrics">
                            <span>
                              Semantic{" "}
                              <strong>
                                {course.similarity.toFixed(4)}
                              </strong>
                            </span>
                          </div>
                        </div>

                        <a
                          href={course.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="course-link"
                        >
                          <span>Open Resource</span>
                          <span>↗</span>
                        </a>
                      </div>
                    )
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    )}

    <section className="features" id="features">
      <div className="section-heading">
        <span className="badge">WHAT YOU GET</span>

        <h2>Turn your resume into a learning roadmap.</h2>

        <p>
          CareerGap AI combines NLP, skill matching, and semantic
          recommendation techniques to turn your resume into actionable
          career insights.
        </p>
      </div>

      <div className="feature-grid">
        <div className="feature-card">
          <div className="feature-card-top">
            <div className="feature-icon">01</div>
            <span>01</span>
          </div>

          <h3>Resume Skill Extraction</h3>

          <p>
            NLP analyzes your resume and identifies relevant technical
            skills from your experience, projects, and education.
          </p>

          <div className="feature-line" />
        </div>

        <div className="feature-card">
          <div className="feature-card-top">
            <div className="feature-icon">02</div>
            <span>02</span>
          </div>

          <h3>Skill Gap Analysis</h3>

          <p>
            Compare your current skills against the requirements of your
            chosen target career and see exactly what you need to develop.
          </p>

          <div className="feature-line" />
        </div>

        <div className="feature-card">
          <div className="feature-card-top">
            <div className="feature-icon">03</div>
            <span>03</span>
          </div>

          <h3>Course Recommendations</h3>

          <p>
            Learning resources are ranked using semantic similarity and
            explainable hybrid recommendation scores.
          </p>

          <div className="feature-line" />
        </div>
      </div>
    </section>

    <section className="how-it-works" id="how-it-works">
      <div className="section-heading">
        <span className="badge">SIMPLE PROCESS</span>

        <h2>How it works.</h2>

        <p>
          Four simple steps take you from a resume to a focused learning
          roadmap.
        </p>
      </div>

      <div className="steps">
        <div className="step">
          <span>01</span>
          <div>
            <h3>Upload Resume</h3>
            <p>Provide your PDF or DOCX resume.</p>
          </div>
        </div>

        <div className="step">
          <span>02</span>
          <div>
            <h3>Choose Career</h3>
            <p>Select the job role you want to target.</p>
          </div>
        </div>

        <div className="step">
          <span>03</span>
          <div>
            <h3>Analyze</h3>
            <p>Our NLP and ML pipeline identifies your skill gaps.</p>
          </div>
        </div>

        <div className="step">
          <span>04</span>
          <div>
            <h3>Start Learning</h3>
            <p>Use the recommended resources to close your gaps.</p>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div className="footer-content">
      <div>
        <a href="#dashboard" className="logo footer-logo">
          <span className="logo-mark">CG</span>
          <span>CareerGap AI</span>
        </a>

        <p>
          AI Career Skill Gap & Course Recommendation System
        </p>
      </div>

      <span>Built with React + FastAPI + NLP + ML</span>
    </div>
  </footer>
</div>


);
}

export default App;
