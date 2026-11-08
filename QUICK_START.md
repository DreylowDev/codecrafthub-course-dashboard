# 🚀 Quick Start Guide - MyLearnTracker

## Get Running in 5 Minutes!

### Step 1: Download the Files (1 minute)
Download all these files to a folder on your computer:
- `app.py`
- `requirements.txt`
- `README.md`
- `test_api.sh` (optional)
- `MyLearnTracker_Postman_Collection.json` (optional)

### Step 2: Install Dependencies (1 minute)
Open your terminal/command prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 3: Start the Server (30 seconds)
```bash
python app.py
```

You should see:
```
============================================================
MyLearnTracker API is starting...
============================================================
API will be available at: http://localhost:5000
============================================================
```

### Step 4: Test It! (2.5 minutes)

#### Option A: Use the Test Script (Easiest)
```bash
# On Mac/Linux
chmod +x test_api.sh
./test_api.sh

# On Windows
# Use Git Bash or test manually with curl commands below
```

#### Option B: Test Manually with curl
```bash
# 1. Add your first course
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"name":"Python Basics","description":"Learn Python","target_date":"2025-12-31","status":"Not Started"}'

# 2. View all courses
curl http://localhost:5000/api/courses

# 3. Update course status
curl -X PUT http://localhost:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"In Progress"}'

# 4. Get statistics
curl http://localhost:5000/api/courses/stats
```

#### Option C: Use Postman (Most User-Friendly)
1. Open Postman
2. Click "Import"
3. Select `MyLearnTracker_Postman_Collection.json`
4. Run the requests in order (1-12)

## ✅ Success Checklist

You're ready to submit when:
- [ ] Server starts without errors
- [ ] You can add a course
- [ ] You can view courses
- [ ] You can update a course
- [ ] You can delete a course
- [ ] `courses.json` file exists with your data

## 🎯 What to Submit

1. **Your complete project folder** with all files
2. **Screenshot** showing successful API tests
3. **Your courses.json** with at least 3 courses

## 💡 Pro Tips

1. **Keep the terminal open** - You'll see helpful debug messages
2. **Test one thing at a time** - Don't try everything at once
3. **Check courses.json** - Open it to see your data being saved
4. **Use Postman** - It's easier than curl for beginners
5. **Read error messages** - They tell you exactly what's wrong

## 🆘 Common Issues

**"pip not found"**
- Install Python from python.org
- Make sure "Add to PATH" was checked during installation

**"Port 5000 already in use"**
- Another app is using that port
- Change to port 5001 in app.py (line at the bottom)

**"No module named 'flask'"**
- Run: `pip install -r requirements.txt`
- Try: `pip3 install -r requirements.txt` if pip doesn't work

## 🎓 Next Steps

After you complete this:
1. Read through `app.py` to understand how it works
2. Try adding the bonus features from the README
3. Customize it to track other things (books, movies, etc.)
4. Show it to your instructor!

## 🎉 You've Got This!

This is a real, working API that you built. You're now an API developer! 

Keep this project - you can use it as a reference for future projects.

---

**Need help?** Check the detailed README.md file or ask your instructor.
