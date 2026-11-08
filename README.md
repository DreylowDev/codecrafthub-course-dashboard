# MyLearnTracker - Personal Learning Goal Tracker

A simple REST API to track courses you want to learn, built with Python Flask.

## 🎯 What Does This Do?

MyLearnTracker helps you keep track of courses you want to take. You can:
- ✅ Add new courses with target dates
- 📋 View all your courses
- 🔄 Update course information
- ✔️ Mark courses as completed
- 🗑️ Delete courses you're no longer interested in

## 📁 Project Structure

```
mylearn-tracker/
├── app.py              # Main Flask application (API server)
├── courses.json        # Data storage (auto-created)
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── test_api.sh        # Test script (optional)
```

## 🚀 Quick Start

### Step 1: Install Dependencies

Make sure you have Python 3.7+ installed, then run:

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python app.py
```

You should see:
```
============================================================
MyLearnTracker API is starting...
============================================================
Data will be stored in: /path/to/courses.json
API will be available at: http://localhost:5000
============================================================
```

### Step 3: Test It!

Open a new terminal and try:
```bash
curl http://localhost:5000
```

You should see a welcome message with available endpoints.

## 📚 API Endpoints

### 1. Get All Courses
**GET** `/api/courses`

```bash
curl http://localhost:5000/api/courses
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "courses": [
    {
      "id": 1,
      "name": "Python Basics",
      "description": "Learn Python fundamentals",
      "target_date": "2025-12-31",
      "status": "In Progress",
      "created_at": "2025-11-04 10:30:00"
    }
  ]
}
```

### 2. Get a Specific Course
**GET** `/api/courses/<id>`

```bash
curl http://localhost:5000/api/courses/1
```

### 3. Add a New Course
**POST** `/api/courses`

```bash
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2025-12-31",
    "status": "Not Started"
  }'
```

**Required Fields:**
- `name` - Course name (string)
- `description` - Course description (string)
- `target_date` - Target completion date in YYYY-MM-DD format
- `status` - Must be one of: "Not Started", "In Progress", "Completed"

**Response:**
```json
{
  "success": true,
  "message": "Course added successfully",
  "course": {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2025-12-31",
    "status": "Not Started",
    "created_at": "2025-11-04 10:30:00"
  }
}
```

### 4. Update a Course
**PUT** `/api/courses/<id>`

```bash
curl -X PUT http://localhost:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "In Progress"
  }'
```

You can update any of these fields:
- `name`
- `description`
- `target_date`
- `status`

### 5. Delete a Course
**DELETE** `/api/courses/<id>`

```bash
curl -X DELETE http://localhost:5000/api/courses/1
```

## 🎁 Bonus Features

### Get Statistics
**GET** `/api/courses/stats`

```bash
curl http://localhost:5000/api/courses/stats
```

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_courses": 5,
    "not_started": 2,
    "in_progress": 2,
    "completed": 1
  }
}
```

### Search Courses
**GET** `/api/courses/search?q=<search_term>`

```bash
curl "http://localhost:5000/api/courses/search?q=python"
```

## 🧪 Testing with Postman

1. Open Postman
2. Create a new request
3. Set the method (GET, POST, PUT, DELETE)
4. Enter the URL (e.g., `http://localhost:5000/api/courses`)
5. For POST/PUT, add JSON body in the "Body" tab (select "raw" and "JSON")
6. Click "Send"

### Example Test Sequence:

1. **Add 3 courses:**
   - POST `/api/courses` (do this 3 times with different data)

2. **View all courses:**
   - GET `/api/courses`

3. **Update one course:**
   - PUT `/api/courses/1` (change status to "In Progress")

4. **Get statistics:**
   - GET `/api/courses/stats`

5. **Delete a course:**
   - DELETE `/api/courses/2`

6. **Verify deletion:**
   - GET `/api/courses`

## 📖 Understanding the Code

### How Data is Stored

Data is stored in `courses.json` as a simple JSON array:

```json
[
  {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2025-12-31",
    "status": "Not Started",
    "created_at": "2025-11-04 10:30:00"
  }
]
```

### How the API Works

1. **When you start the app:** Flask creates a web server on port 5000
2. **When you make a request:** Flask routes it to the right function
3. **The function:** 
   - Reads `courses.json`
   - Does the operation (add, update, delete)
   - Saves back to `courses.json`
   - Returns a JSON response

### Key Code Sections

- **Helper Functions** (lines 20-90): Load/save data, validate input
- **API Endpoints** (lines 95-350): Handle HTTP requests
- **Error Handlers** (lines 355-370): Handle errors gracefully

## 🐛 Troubleshooting

### Problem: "Module not found: flask"
**Solution:** Run `pip install -r requirements.txt`

### Problem: "Address already in use"
**Solution:** Another app is using port 5000. Stop it or change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Problem: "courses.json not found"
**Solution:** The app creates it automatically. Make sure you have write permissions in the folder.

### Problem: "Invalid JSON"
**Solution:** Check your JSON syntax. Common issues:
- Missing quotes around strings
- Extra commas
- Missing braces

## 🎓 Learning Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **REST API Tutorial:** https://restfulapi.net/
- **JSON Tutorial:** https://www.json.org/

## 🚀 Next Steps (Phase 2 Ideas)

Once you master this, you can add:
1. Frontend web interface
2. User accounts and authentication
3. Course categories and tags
4. Progress tracking (percentage complete)
5. Email reminders for target dates
6. Export to PDF feature

## 📝 Assignment Checklist

- [ ] Application runs without errors
- [ ] Can add a course
- [ ] Can view all courses
- [ ] Can update a course
- [ ] Can delete a course
- [ ] Data persists in courses.json
- [ ] Tested all endpoints
- [ ] Code has comments
- [ ] README is complete

## 💡 Tips

1. **Test one endpoint at a time** - Don't try to build everything at once
2. **Check the terminal** - Error messages appear there
3. **Use print statements** - Add `print(variable)` to debug
4. **Save your work often** - Use Git to commit changes
5. **Ask for help** - Use your GenAI tool if you get stuck!

## 🏆 Success!

If you can successfully:
- Start the server
- Add 3 different courses
- Update one course status
- Delete one course
- View all remaining courses

**Congratulations! You've built a working REST API!** 🎉

## 📧 Questions?

If you have questions:
1. Check the error message in the terminal
2. Review the relevant section of app.py
3. Ask your instructor
4. Use GenAI: "I'm getting error X when doing Y, what does it mean?"

---

**Built with ❤️ for learning Python and APIs**
