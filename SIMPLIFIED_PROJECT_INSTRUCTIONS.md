---
markdown-version: v1
tool-type: ai-classroom
---

::page{title="Final Project: CodeCraftHub Learning Management System - Building a Personalized Learning Platform"}

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-CC0100EN-SkillsNetwork/images/IDSN-logo.png" width="200/">

<br>
<br>
**Estimated time**: 1.5 hours
<br>
<br>
Welcome to this final project lab. Your organization is creating CodeCraftHub, a personalized learning platform crafted for developers! Your assignment is to design the server-side architecture for this learning platform and develop the learning platform using Python. You will create the server-side components for CodeCraftHub using Generative AI.

In this project, you'll leverage the power of Generative AI to transform your vision into a reality.


## Learning objectives

After completing this lab, you will be able to perform the following tasks:

- Design and develop software applications using Generative AI
- Create documentation for the code with Generative AI
- Create test cases with Generative AI
- Deploy the application designed and developed entirely with Generative AI


## Prerequisites

- You must be familiar with at least one programming language.
- You must have a GitHub account.
- You must be comfortable using the IDE.
- You must be familiar with using Postman or Curl.

## Setting up the AI classroom

As part of this work, you will need to set up the Gen AI classroom
In case you need help with this task here&apos;s a link to instructions to [Get Familiar with GenAI Classroom](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-AI0274EN-SkillsNetwork/labs/Module1/Get_familiar_with_GenAI_Classroom.md.html "<Lab Link>")
	

::page{title="Gathering requirements for the learning platform development"}

When using GenAI to gather your requirements for developing the server-side learning platform keeping in mind the following considerations:

- The effectiveness of the responses depends on the prompts provided.
- The prompts provided here are suggestions. Use your discretion to adapt the prompts to your needs.
- Apply your subject matter expertise and judgment as a developer.
- You are responsible for validating the correctness of the responses.

>**Note:** In the Gen AI interface, select your preferred LLM.

Type the following prompt to give the LLM context and the objective:


	I want to create a simple personalized learning platform called CodeCraftHub where developers can 
	track courses they want to learn. This is for beginners, so keep it simple.
	
	Requirements:
	- Use Python with Flask framework
	- Store course data in a simple JSON text file (NO database needed)
	- No authentication or user management needed
	- Focus on learning REST API basics
	
	Each course should track:
	- Course name
	- Description
	- Target completion date
	- Current status (Not Started, In Progress, Completed)
	
	Please recommend:
	1. A simple project structure for beginners
	2. The REST API endpoints I should create
	3. How to store and retrieve data from a JSON file

<details style="background-color: rgba(16,119,187,255); color: white; padding-top: .3cm; padding-bottom:.1cm; border-radius: 5px;padding-left:.1cm;padding-right:.1cm"><summary style="cursor: pointer;font-size:larger; margin-left:.5cm">Click here to view the sample response generated</summary>
<div style="background-color: rgba(38,38,38,255); color: white;padding:.3cm">
Creating a simple personalized learning platform like CodeCraftHub is a great beginner project! Here's a straightforward approach:

### 1. Simple Project Structure

```
codecrafthub/
├── app.py              # Main Flask application
├── courses.json        # JSON file for data storage (auto-created)
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

### 2. REST API Endpoints

You should create these basic endpoints:

**Course Management:**
- `POST /api/courses` - Add a new course
- `GET /api/courses` - Get all courses
- `GET /api/courses/<id>` - Get a specific course
- `PUT /api/courses/<id>` - Update a course
- `DELETE /api/courses/<id>` - Delete a course

**Optional Bonus Endpoints:**
- `GET /api/courses/stats` - Get statistics about courses
- `GET /api/courses/search?q=term` - Search courses

### 3. Data Storage with JSON

**Course Data Structure:**
```json
{
  "id": 1,
  "name": "Python Basics",
  "description": "Learn Python fundamentals",
  "target_date": "2025-12-31",
  "status": "Not Started",
  "created_at": "2025-11-04 10:30:00"
}
```

**How to Store/Retrieve:**
- Use Python's `json` module to read/write
- Load all courses at the start of each request
- Save back to file after any changes
- The file will be created automatically if it doesn't exist

### 4. Next Steps

Start by creating `app.py` with these helper functions:
- `load_courses()` - Read from JSON file
- `save_courses(courses)` - Write to JSON file
- `get_next_id(courses)` - Generate new course IDs

Then implement each API endpoint one at a time, testing as you go!
</div></details>

>Disclaimer: The response you receive from your LLM might vary from the response provided here.


::page{title="Creating the application structure"}

For the following exercise, a simple single-file Flask application is the recommended approach.

Enter the following in the prompt to create the main application file:


	Now create the complete Python Flask code for app.py with these requirements:
	
	1. Create a Flask REST API with all CRUD operations for courses
	2. Store data in a JSON file called "courses.json"
	3. Include these endpoints:
	   - POST /api/courses - Add a new course
	   - GET /api/courses - Get all courses
	   - GET /api/courses/<id> - Get a specific course
	   - PUT /api/courses/<id> - Update a course
	   - DELETE /api/courses/<id> - Delete a course
	
	4. Each course must have:
	   - id (auto-generated, starting from 1)
	   - name (required)
	   - description (required)
	   - target_date (required, format YYYY-MM-DD)
	   - status (required, must be: "Not Started", "In Progress", or "Completed")
	   - created_at (auto-generated timestamp)
	
	5. Include proper error handling for:
	   - Missing required fields
	   - Course not found
	   - Invalid status values
	   - File read/write errors
	
	6. Add helpful comments throughout the code for beginners
	7. Make sure the app creates courses.json automatically if it doesn't exist

The response will include the complete Flask application code.

<details style="background-color: rgba(16,119,187,255); color: white; padding-top: .3cm; padding-bottom:.1cm; border-radius: 5px;padding-left:.1cm;padding-right:.1cm"><summary style="cursor: pointer;font-size:larger; margin-left:.5cm">Click here to view the sample response generated</summary>
<div style="background-color: rgba(38,38,38,255); color: white;padding:.3cm">

Here's the complete Flask application code with all the requirements:

```python
from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
DATA_FILE = 'courses.json'

# Helper function to load courses from JSON file
def load_courses():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
        return []
    
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

# Helper function to save courses to JSON file
def save_courses(courses):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(courses, f, indent=2)
        return True
    except Exception as e:
        return False

# Get next available ID
def get_next_id(courses):
    if not courses:
        return 1
    return max(course['id'] for course in courses) + 1

# GET all courses
@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    courses = load_courses()
    return jsonify({
        'success': True,
        'count': len(courses),
        'courses': courses
    }), 200

# GET specific course
@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    courses = load_courses()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course:
        return jsonify({'success': True, 'course': course}), 200
    return jsonify({'success': False, 'error': 'Course not found'}), 404

# POST new course
@app.route('/api/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'description', 'target_date', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Missing required field: {field}'
            }), 400
    
    # Validate status
    valid_statuses = ['Not Started', 'In Progress', 'Completed']
    if data['status'] not in valid_statuses:
        return jsonify({
            'success': False,
            'error': f'Status must be one of: {", ".join(valid_statuses)}'
        }), 400
    
    courses = load_courses()
    
    new_course = {
        'id': get_next_id(courses),
        'name': data['name'],
        'description': data['description'],
        'target_date': data['target_date'],
        'status': data['status'],
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    courses.append(new_course)
    save_courses(courses)
    
    return jsonify({
        'success': True,
        'message': 'Course added successfully',
        'course': new_course
    }), 201

# PUT update course
@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json()
    courses = load_courses()
    
    course_index = next((i for i, c in enumerate(courses) if c['id'] == course_id), None)
    
    if course_index is None:
        return jsonify({'success': False, 'error': 'Course not found'}), 404
    
    # Update fields if provided
    course = courses[course_index]
    if 'name' in data:
        course['name'] = data['name']
    if 'description' in data:
        course['description'] = data['description']
    if 'target_date' in data:
        course['target_date'] = data['target_date']
    if 'status' in data:
        course['status'] = data['status']
    
    save_courses(courses)
    
    return jsonify({
        'success': True,
        'message': 'Course updated successfully',
        'course': course
    }), 200

# DELETE course
@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    courses = load_courses()
    course_index = next((i for i, c in enumerate(courses) if c['id'] == course_id), None)
    
    if course_index is None:
        return jsonify({'success': False, 'error': 'Course not found'}), 404
    
    deleted_course = courses.pop(course_index)
    save_courses(courses)
    
    return jsonify({
        'success': True,
        'message': 'Course deleted successfully',
        'deleted_course': deleted_course
    }), 200

if __name__ == '__main__':
    print("CodeCraftHub API is starting...")
    print(f"Data will be stored in: {os.path.abspath(DATA_FILE)}")
    print("API will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
```

This code includes all required features with proper error handling and helpful comments!
</div></details>

>Disclaimer: The response you receive from your LLM might vary from the response provided here.


::page{title="Creating test cases for the API"}

You now have a complete Flask application. Next, create test cases to verify all endpoints work correctly.

Enter the following prompt:


	Create comprehensive test cases for the CodeCraftHub API. Provide:
	
	1. Curl commands to test each endpoint
	2. Example JSON payloads for POST and PUT requests
	3. Expected responses for successful operations
	4. Test cases for error scenarios (missing fields, invalid data, course not found)
	
	Make the tests easy to copy and paste for beginners.

The response will provide complete test commands.

<details style="background-color: rgba(16,119,187,255); color: white; padding-top: .3cm; padding-bottom:.1cm; border-radius: 5px;padding-left:.1cm;padding-right:.1cm"><summary style="cursor: pointer;font-size:larger; margin-left:.5cm">Click here to view the sample response generated</summary>
<div style="background-color: rgba(38,38,38,255); color: white;padding:.3cm">

Here are comprehensive test cases for the CodeCraftHub API:

### Test 1: Add a New Course (POST)

```bash
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Basics",
    "description": "Learn Python fundamentals including variables, loops, and functions",
    "target_date": "2025-12-31",
    "status": "Not Started"
  }'
```

**Expected Response (201 Created):**
```json
{
  "success": true,
  "message": "Course added successfully",
  "course": {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals including variables, loops, and functions",
    "target_date": "2025-12-31",
    "status": "Not Started",
    "created_at": "2025-11-04 10:30:00"
  }
}
```

### Test 2: Get All Courses (GET)

```bash
curl http://localhost:5000/api/courses
```

**Expected Response (200 OK):**
```json
{
  "success": true,
  "count": 1,
  "courses": [
    {
      "id": 1,
      "name": "Python Basics",
      "description": "Learn Python fundamentals",
      "target_date": "2025-12-31",
      "status": "Not Started",
      "created_at": "2025-11-04 10:30:00"
    }
  ]
}
```

### Test 3: Get Specific Course (GET)

```bash
curl http://localhost:5000/api/courses/1
```

### Test 4: Update Course (PUT)

```bash
curl -X PUT http://localhost:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "In Progress"
  }'
```

### Test 5: Delete Course (DELETE)

```bash
curl -X DELETE http://localhost:5000/api/courses/1
```

### Error Test Cases

**Test 6: Missing Required Fields**
```bash
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Incomplete Course"
  }'
```

**Expected Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Missing required field: description"
}
```

**Test 7: Invalid Status Value**
```bash
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Course",
    "description": "Test",
    "target_date": "2025-12-31",
    "status": "Invalid Status"
  }'
```

**Test 8: Course Not Found**
```bash
curl http://localhost:5000/api/courses/999
```

**Expected Response (404 Not Found):**
```json
{
  "success": false,
  "error": "Course not found"
}
```

You can run these tests in sequence to verify all functionality!
</div></details>

>Disclaimer: The response you receive from your LLM might vary from the response provided here.


::page{title="Creating project documentation"}

Now create comprehensive documentation for your project.

Enter the following prompt:


	Create a complete README.md file for the CodeCraftHub project that includes:
	
	1. Project overview and description
	2. Features list
	3. Installation instructions (step by step)
	4. How to run the application
	5. API endpoints documentation with examples
	6. Testing instructions
	7. Troubleshooting common issues
	8. Project structure explanation
	
	Write it for beginners who are learning REST APIs for the first time.

The response will provide a comprehensive README file.

<details style="background-color: rgba(16,119,187,255); color: white; padding-top: .3cm; padding-bottom:.1cm; border-radius: 5px;padding-left:.1cm;padding-right:.1cm"><summary style="cursor: pointer;font-size:larger; margin-left:.5cm">Click here to view the sample response generated</summary>
<div style="background-color: rgba(38,38,38,255); color: white;padding:.3cm">

# CodeCraftHub Learning Management System

A simple personalized learning platform for developers to track courses they want to learn.

## Features

- Add courses with target completion dates
- View all your courses
- Update course information and status
- Delete completed courses
- JSON file-based storage (no database needed)
- RESTful API design
- Proper error handling

## Installation

1. **Clone or download the project**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Flask server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Add a Course
**POST** `/api/courses`

Request body:
```json
{
  "name": "Python Basics",
  "description": "Learn Python fundamentals",
  "target_date": "2025-12-31",
  "status": "Not Started"
}
```

### 2. Get All Courses
**GET** `/api/courses`

### 3. Get Specific Course
**GET** `/api/courses/<id>`

### 4. Update Course
**PUT** `/api/courses/<id>`

Request body (all fields optional):
```json
{
  "status": "In Progress"
}
```

### 5. Delete Course
**DELETE** `/api/courses/<id>`

## Testing

Use the provided curl commands or import the Postman collection to test all endpoints.

## Troubleshooting

**Problem:** "Module not found: flask"  
**Solution:** Run `pip install -r requirements.txt`

**Problem:** "Port already in use"  
**Solution:** Stop other applications using port 5000 or change the port in app.py

## Project Structure

```
codecrafthub/
├── app.py           # Main Flask application
├── courses.json     # Data storage (auto-created)
└── requirements.txt # Dependencies
```
</div></details>

>Disclaimer: The response you receive from your LLM might vary from the response provided here.


::page{title="Running and testing your application"}

## Step 1: Set up your development environment

1. Create a new project directory:
```bash
mkdir codecrafthub
cd codecrafthub
```

2. Create `requirements.txt`:
```
Flask==3.0.0
```

3. Create your `app.py` file with the code generated by GenAI

## Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Run the application

```bash
python app.py
```

You should see:
```
CodeCraftHub API is starting...
Data will be stored in: /path/to/courses.json
API will be available at: http://localhost:5000
```

## Step 4: Test the API endpoints

In a new terminal window, test each endpoint using the curl commands generated by GenAI:

1. Add a course (POST)
2. Get all courses (GET)
3. Get specific course (GET)
4. Update a course (PUT)
5. Delete a course (DELETE)

Verify that:
- All endpoints return appropriate responses
- Data persists in `courses.json`
- Error handling works correctly


::page{title="Optional enhancements"}

If you complete the basic requirements early, consider adding these bonus features using GenAI:

### Enhancement 1: Statistics Endpoint

Prompt:
```
Add a new endpoint GET /api/courses/stats that returns statistics about courses:
- Total number of courses
- Number of courses by status (Not Started, In Progress, Completed)
```

### Enhancement 2: Search Functionality

Prompt:
```
Add a search endpoint GET /api/courses/search?q=term that searches courses by name or description
```

### Enhancement 3: Date Validation

Prompt:
```
Add validation to ensure target_date is in the future and in correct format (YYYY-MM-DD)
```


::page{title="Pushing your work to GitHub"}

Remember, any modifications you make in the lab environment won&#39;t be saved. If you plan to step away, use the following steps to make sure your changes are pushed to GitHub:

Verify that you are currently inside the project directory.

1. Navigate to the project directory by performing `cd codecrafthub`.

2. Set up your Git configuration:
   - Run: `git config --global user.email "yourgithub@email.com"`
   - Run: `git config --global user.name "name"`

3. Initialize the repository (if not already done):
   - Run: `git init`

4. Add your changes to the staging area:
   - Run: `git add .`

5. Commit your changes with a descriptive message:
   - Run: `git commit -m "Complete CodeCraftHub learning platform"`

6. The first step is to generate an access token from GitHub.com. Follow the lab named [Generate GitHub personal access token](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-CD0131EN-SkillsNetwork/labs/create-personal-token/instructions.md.html "Generate GitHub personal access token") and copy the access token as a password in the upcoming exercises.

7. Create a new repository on GitHub.com and copy the repository URL.

8. Link your local repository to GitHub:
   - Run: `git remote add origin <your-github-repo-url>`

9. Push your changes to the Git repository:
   - Run: `git push -u origin main`

10. A prompt in the terminal will prompt you to enter your GitHub username and password (your previously created Personal Access Token from Step 6).

These steps verify that you safely stored in GitHub, allowing you to continue when you return to the lab environment.


::page{title="Reviewing your checklist"}

At this stage, you have completed the following tasks:
- You now have a running application that offers REST API functionality for the CodeCraftHub learning platform.
- You created a simple, file-based storage system using JSON.
- The application includes proper error handling and validation.
- You have documented your code and created test cases.
- [Optional] You pushed all the code to your GitHub repository.


## Summary

You&#39;ve now achieved the following accomplishments:  

- You successfully gathered requirements for a simple learning platform using Generative AI.
- You created a complete Flask REST API with CRUD operations.
- You implemented file-based data storage using JSON.
- You created comprehensive test cases and documentation.
- You validated your application works correctly.
	
**Congratulations! You have successfully leveraged Generative AI to build the CodeCraftHub Learning Management System using Python, Flask, and JSON file storage.**


## Author(s)

- [Ramanujam Srinivasan](https://www.linkedin.com/in/ramanujamrs/)

### &#169; IBM Corporation. All rights reserved.

<!--
## Changelog
| Date | Version | Changed by | Change Description |
|------|--------|--------|---------|
| 2025-10-25 | 0.1 | Ramanujam | Initial version created |
| 2025-11-04 | 0.2 | P.Kravitz | ID edits. With questions back to the SME |
| 2025-11-05 | 1.0 | Simplified | Simplified for beginners |
-->
