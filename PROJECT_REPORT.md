# Project Report: AI Risk Assessment Assistant for a Small Business

## Abstract
Small businesses face cyber, financial, operational, compliance, and people-related risks but may not have a dedicated risk management team. This project presents a lightweight web-based Risk Assessment Assistant built with Python and Streamlit. Users enter a risk, rate its likelihood and impact, and receive a transparent score, severity classification, and practical mitigation suggestions. A dashboard summarizes recorded risks and supports CSV export. The prototype demonstrates how structured assessment and automation can make risk management easier to begin. It is a decision-support tool rather than a certified risk management system.

## 1. Introduction
Risk management is the process of identifying events that may prevent an organization from meeting its objectives, assessing their potential effects, and choosing suitable responses. Small organizations may rely on informal judgment, causing risks to be missed or handled inconsistently. A simple digital register can improve consistency and accountability.

## 2. Problem statement
Small businesses often lack a low-cost, easy-to-use process to document risks, prioritize them, and track suggested actions. A manual spreadsheet may not provide consistent scoring or clear recommendations.

## 3. Objectives
- Provide a simple interface for recording business risks.
- Classify risks into common business categories.
- Calculate a repeatable likelihood-impact score.
- Suggest mitigation actions based on the risk category and severity.
- Display a summary and export a risk register.

## 4. Scope
The prototype supports cybersecurity, financial, operational, compliance, and people-related risks. It is designed for demonstration and early-stage assessment. It does not automatically inspect business systems, verify compliance, predict incidents from historical data, or replace expert review.

## 5. Technology stack
- Python: application logic
- Streamlit: interactive web interface
- Pandas: tabular data and CSV export
- Session state: temporary storage during the current session

## 6. Methodology
The user assigns likelihood and impact from 1 (lowest) to 5 (highest). The application multiplies the values to produce a score from 1 to 25.

- 1–5: Low
- 6–11: Medium
- 12–19: High
- 20–25: Critical

The category determines a set of suggested actions. Higher-severity risks display more initial recommendations. This is a transparent rule-based approach; the term “AI-assisted” describes the intended direction of the project, not a trained predictive model in this version.

## 7. System workflow
1. User enters a business profile.
2. User records a risk title, category, likelihood, impact, details, owner, and status.
3. The application calculates the score and severity.
4. The recommendation engine selects relevant actions.
5. The dashboard displays a risk register and summary.
6. The user downloads the assessment as a CSV file.

## 8. Example test cases

| Test | Likelihood | Impact | Expected score | Expected level |
|---|---:|---:|---:|---|
| Low exposure | 1 | 2 | 2 | Low |
| Moderate concern | 2 | 3 | 6 | Medium |
| Significant concern | 3 | 4 | 12 | High |
| Severe concern | 5 | 4 | 20 | Critical |
| Maximum severity | 5 | 5 | 25 | Critical |

## 9. Expected results
The application should accept valid risk entries, calculate the score consistently, display a severity label, provide category-specific recommendations, summarize the recorded assessments, and export the data to CSV. Users can prioritize high-scoring risks for review.

## 10. Limitations and ethical considerations
- Ratings are subjective and depend on the quality of user input.
- The current version uses predefined rules rather than a machine-learning model or live generative AI.
- Data is not saved permanently after the session ends.
- Recommendations can be incomplete or unsuitable for a particular business.
- Avoid entering confidential information.
- A qualified person should review important decisions and applicable legal requirements.

## 11. Future enhancements
Permanent database storage, secure login, user roles, risk history, visual analytics, mitigation due dates, notifications, an optional language-model API, and mapping to a recognized risk framework can be added. Any AI-generated recommendation should be reviewed by a human and should not be treated as a guarantee.

## 12. Conclusion
The AI Risk Assessment Assistant demonstrates a practical way to structure and prioritize common small-business risks. By combining a simple questionnaire, transparent scoring, recommendations, and report export, it can help a business begin a more consistent risk review process. Future versions can improve persistence, security, and personalization.

## Viva questions
1. What is risk assessment?
2. Why are likelihood and impact scored separately?
3. Why is the score calculated by multiplication?
4. What is the difference between rule-based logic and machine learning?
5. Why is human review still necessary?
6. What are the limitations of session-state storage?
7. How could SQLite improve this project?
8. What safeguards are needed before using a generative AI API?
