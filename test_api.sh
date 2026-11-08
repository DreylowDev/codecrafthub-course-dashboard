#!/bin/bash

# MyLearnTracker API Test Script
# This script tests all API endpoints

echo "=================================="
echo "MyLearnTracker API Test Suite"
echo "=================================="
echo ""

BASE_URL="http://localhost:5000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASS=0
FAIL=0

# Function to print test results
print_test() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $2"
        ((PASS++))
    else
        echo -e "${RED}✗ FAIL${NC}: $2"
        ((FAIL++))
    fi
}

echo -e "${YELLOW}Test 1: Check if server is running${NC}"
response=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL)
if [ $response -eq 200 ]; then
    print_test 0 "Server is running"
else
    print_test 1 "Server is not responding (make sure app.py is running)"
    exit 1
fi
echo ""

echo -e "${YELLOW}Test 2: Add a new course - Python Basics${NC}"
response=$(curl -s -X POST $BASE_URL/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2025-12-31",
    "status": "Not Started"
  }')
echo "Response: $response"
if [[ $response == *"success\":true"* ]]; then
    print_test 0 "Course added successfully"
else
    print_test 1 "Failed to add course"
fi
echo ""

echo -e "${YELLOW}Test 3: Add another course - Web Development${NC}"
response=$(curl -s -X POST $BASE_URL/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Web Development",
    "description": "HTML, CSS, JavaScript basics",
    "target_date": "2026-03-15",
    "status": "Not Started"
  }')
echo "Response: $response"
if [[ $response == *"success\":true"* ]]; then
    print_test 0 "Course added successfully"
else
    print_test 1 "Failed to add course"
fi
echo ""

echo -e "${YELLOW}Test 4: Add a third course - Data Science${NC}"
response=$(curl -s -X POST $BASE_URL/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Data Science Fundamentals",
    "description": "Introduction to data analysis and machine learning",
    "target_date": "2026-06-30",
    "status": "Not Started"
  }')
echo "Response: $response"
if [[ $response == *"success\":true"* ]]; then
    print_test 0 "Course added successfully"
else
    print_test 1 "Failed to add course"
fi
echo ""

echo -e "${YELLOW}Test 5: Get all courses${NC}"
response=$(curl -s $BASE_URL/api/courses)
echo "Response: $response"
if [[ $response == *"success\":true"* ]] && [[ $response == *"courses"* ]]; then
    print_test 0 "Retrieved all courses"
else
    print_test 1 "Failed to retrieve courses"
fi
echo ""

echo -e "${YELLOW}Test 6: Get specific course (ID: 1)${NC}"
response=$(curl -s $BASE_URL/api/courses/1)
echo "Response: $response"
if [[ $response == *"success\":true"* ]]; then
    print_test 0 "Retrieved specific course"
else
    print_test 1 "Failed to retrieve specific course"
fi
echo ""

echo -e "${YELLOW}Test 7: Update course status (ID: 1)${NC}"
response=$(curl -s -X PUT $BASE_URL/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "In Progress"
  }')
echo "Response: $response"
if [[ $response == *"success\":true"* ]]; then
    print_test 0 "Course updated successfully"
else
    print_test 1 "Failed to update course"
fi
echo ""

echo -e "${YELLOW}Test 8: Get statistics${NC}"
response=$(curl -s $BASE_URL/api/courses/stats)
echo "Response: $response"
if [[ $response == *"success\":true"* ]] && [[ $response == *"statistics"* ]]; then
    print_test 0 "Retrieved statistics"
else
    print_test 1 "Failed to retrieve statistics"
fi
echo ""

echo -e "${YELLOW}Test 9: Search for 'Python' courses${NC}"
response=$(curl -s "$BASE_URL/api/courses/search?q=python")
echo "Response: $response"
if [[ $response == *"success\":true"* ]]; then
    print_test 0 "Search completed"
else
    print_test 1 "Search failed"
fi
echo ""

echo -e "${YELLOW}Test 10: Delete a course (ID: 2)${NC}"
response=$(curl -s -X DELETE $BASE_URL/api/courses/2)
echo "Response: $response"
if [[ $response == *"success\":true"* ]]; then
    print_test 0 "Course deleted successfully"
else
    print_test 1 "Failed to delete course"
fi
echo ""

echo -e "${YELLOW}Test 11: Verify course was deleted${NC}"
response=$(curl -s $BASE_URL/api/courses/2)
echo "Response: $response"
if [[ $response == *"404"* ]] || [[ $response == *"not found"* ]]; then
    print_test 0 "Course correctly returns not found"
else
    print_test 1 "Course should not exist"
fi
echo ""

echo -e "${YELLOW}Test 12: Try to add invalid course (missing fields)${NC}"
response=$(curl -s -X POST $BASE_URL/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Incomplete Course"
  }')
echo "Response: $response"
if [[ $response == *"success\":false"* ]]; then
    print_test 0 "Error handling works correctly"
else
    print_test 1 "Should reject invalid data"
fi
echo ""

echo "=================================="
echo "Test Summary"
echo "=================================="
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
echo "=================================="

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}All tests passed! 🎉${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Check the errors above.${NC}"
    exit 1
fi
