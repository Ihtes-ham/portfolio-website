from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

IHTESHAM_CONTEXT = """You are an AI assistant on Muhammad Ihtesham Ul Haq's portfolio website. Answer questions about Ihtesham based on this info only. Be friendly, professional and concise in 2-3 sentences.

Name: Muhammad Ihtesham Ul Haq
Role: Python/Django Backend Developer
Email: ihteshamm480@gmail.com
GitHub: github.com/Ihtes-ham
LinkedIn: linkedin.com/in/m-ihtesham480
Location: Layyah, Punjab, Pakistan

Education: BS Software Engineering, Islamia University of Bahawalpur (2022-2026), CGPA: 3.50

Experience: Backend Developer Intern at Enigmatix Pvt. Ltd. (Jun 2024 - Jul 2025)
- Built REST APIs, authentication, database-driven CRUD operations
- Shipped: HR Management System, Online Lab Diagnosis Portal, Student Record Management, Blog Application

Skills:
- Languages: Python, SQL, JavaScript, HTML5, CSS3
- Backend: Django, Django REST Framework, JWT, OAuth 2.0
- Databases: PostgreSQL, MySQL, SQLite, Redis
- Async: Celery, Celery Beat
- AI/Data: Google Gemini API, TextBlob, Pandas
- Frontend: Bootstrap, Tailwind CSS, Chart.js
- Tools: Git, GitHub, VS Code, PyCharm, Postman, Swagger/ReDoc

Projects:
1. SocialSync - AI social media management platform (Final Year Project)
   Stack: Django REST, PostgreSQL, Redis, Celery, Google Gemini API
   22+ database models, 60+ REST endpoints, multi-platform management

2. ScholarIntell - Scholarship Recommendation System (Freelance)
   Stack: Python, Django, HTML, CSS, JavaScript
   Large scholarship database with eligibility matching engine

3. HRMS - Human Resource Management System
   Stack: Django, PostgreSQL | github.com/Ihtes-ham/hrms

4. Face Recognition Attendance System
   Stack: Django, OpenCV | github.com/Ihtes-ham/face_attendance_system

5. Social Media Analytics Platform
   Stack: Django | github.com/Ihtes-ham/social-analytics-platform

6. Bugzilla Lite - Bug tracking app
   github.com/Ihtes-ham/bugzilla_lite

Availability: Open to full-time, remote, and freelance opportunities"""


def index(request):
    return render(request, 'core/index.html')


@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            headers = {
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            }

            payload = {
                'model': 'llama-3.3-70b-versatile',
                'messages': [
                    {'role': 'system', 'content': IHTESHAM_CONTEXT},
                    {'role': 'user', 'content': user_message}
                ],
                'max_tokens': 150,
                'temperature': 0.7
            }

            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=10
            )

            result = response.json()
            ai_response = result['choices'][0]['message']['content']

            return JsonResponse({'response': ai_response, 'status': 'success'})

        except Exception as e:
            return JsonResponse({
                'response': 'Sorry, having trouble responding right now. Please contact Ihtesham at ihteshamm480@gmail.com',
                'status': 'error'
            })

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def analyze_cv(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            job_description = data.get('job_description', '')

            if not job_description:
                return JsonResponse({'response': 'Please provide a job description.', 'status': 'error'})

            headers = {
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            }

            prompt = f"""Analyze how well Ihtesham matches this job description:

{job_description}

Provide your analysis in this exact format:
- Match Score: X%
- Matching Skills: (list them)
- Skills to Develop: (list missing ones)
- Recommendation: (1-2 sentences)

Be honest and professional."""

            payload = {
                'model': 'llama-3.3-70b-versatile',
                'messages': [
                    {'role': 'system', 'content': IHTESHAM_CONTEXT},
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': 300,
                'temperature': 0.7
            }

            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=10
            )

            result = response.json()
            ai_response = result['choices'][0]['message']['content']

            return JsonResponse({'response': ai_response, 'status': 'success'})

        except Exception as e:
            return JsonResponse({
                'response': 'Analysis failed. Please try again!',
                'status': 'error'
            })

    return JsonResponse({'error': 'Method not allowed'}, status=405)