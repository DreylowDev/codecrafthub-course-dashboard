"""
CodeCraftHub - Course Tracking REST API

This Flask application provides CRUD operations for courses and stores
course data in a local JSON file named courses.json.

Run with:

    python app.py
"""

from datetime import datetime
from pathlib import Path
from json import JSONDecodeError
import json
import re

from flask import Flask, jsonify, request


# ---------------------------------------------------------
# Flask application setup
# ---------------------------------------------------------

app = Flask(__name__)

# Store courses.json in the same folder as this app.py file.
DATA_FILE = Path(__file__).parent / "courses.json"

# Allowed course status values.
VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed",
}

# Required fields when creating or replacing a course.
REQUIRED_FIELDS = {
    "name",
    "description",
    "target_date",
    "status",
}


# ---------------------------------------------------------
# Custom exception for file storage errors
# ---------------------------------------------------------

class StorageError(Exception):
    """Raised when courses.json cannot be read or written."""


# ---------------------------------------------------------
# JSON file helper functions
# ---------------------------------------------------------

def save_courses(courses):
    """
    Save the course list to courses.json.

    Raises:
        StorageError: If the file cannot be written.
    """
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(courses, file, indent=4)
    except OSError as error:
        raise StorageError(
            f"Unable to write course data: {error}"
        ) from error


def load_courses():
    """
    Load courses from courses.json.

    If courses.json does not exist, it is created automatically
    with an empty list.

    Returns:
        list: A list of course dictionaries.

    Raises:
        StorageError: If the file cannot be read or contains invalid JSON.
    """
    # Create the file automatically if it does not exist.
    if not DATA_FILE.exists():
        try:
            save_courses([])
        except StorageError:
            raise

        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            courses = json.load(file)

    except JSONDecodeError as error:
        raise StorageError(
            "courses.json contains invalid JSON data."
        ) from error

    except OSError as error:
        raise StorageError(
            f"Unable to read course data: {error}"
        ) from error

    # The JSON file should contain a list of courses.
    if not isinstance(courses, list):
        raise StorageError(
            "courses.json must contain a JSON list."
        )

    return courses


# ---------------------------------------------------------
# Validation helper functions
# ---------------------------------------------------------

def validate_date(date_value):
    """
    Check that a date uses the YYYY-MM-DD format.

    Returns:
        str or None: An error message, or None if valid.
    """
    if not isinstance(date_value, str):
        return "target_date must be a string in YYYY-MM-DD format."

    # This ensures the date has exactly the expected structure.
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_value):
        return "target_date must use YYYY-MM-DD format."

    # This ensures the date is an actual calendar date.
    try:
        datetime.strptime(date_value, "%Y-%m-%d")
    except ValueError:
        return "target_date must be a valid calendar date."

    return None


def validate_course_data(data):
    """
    Validate data received from a POST or PUT request.

    Returns:
        str or None: An error message, or None if all data is valid.
    """
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    # Check that all required fields are present.
    missing_fields = REQUIRED_FIELDS - set(data.keys())

    if missing_fields:
        missing_names = ", ".join(sorted(missing_fields))
        return f"Missing required field(s): {missing_names}."

    # Validate name.
    if not isinstance(data["name"], str) or not data["name"].strip():
        return "name is required and must be a non-empty string."

    # Validate description.
    if (
        not isinstance(data["description"], str)
        or not data["description"].strip()
    ):
        return "description is required and must be a non-empty string."

    # Validate target date.
    date_error = validate_date(data["target_date"])
    if date_error:
        return date_error

    # Validate status.
    if data["status"] not in VALID_STATUSES:
        valid_values = ", ".join(sorted(VALID_STATUSES))
        return (
            f"Invalid status. Status must be one of: "
            f"{valid_values}."
        )

    return None


def get_next_course_id(courses):
    """
    Generate the next numeric course ID.

    The first course receives ID 1. If courses have been deleted,
    the next ID is still one greater than the largest existing ID.
    """
    if not courses:
        return 1

    existing_ids = [
        course.get("id", 0)
        for course in courses
        if isinstance(course.get("id"), int)
    ]

    if not existing_ids:
        return 1

    return max(existing_ids) + 1


def find_course(courses, course_id):
    """
    Find a course by its integer ID.

    Returns:
        dict or None: The matching course, if found.
    """
    for course in courses:
        if course.get("id") == course_id:
            return course

    return None


# ---------------------------------------------------------
# API endpoints
# ---------------------------------------------------------

@app.route("/api/courses", methods=["POST"])
def create_course():
    """
    Add a new course.

    Endpoint:
        POST /api/courses
    """
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    try:
        courses = load_courses()

        new_course = {
            "id": get_next_course_id(courses),
            "name": data["name"].strip(),
            "description": data["description"].strip(),
            "target_date": data["target_date"],
            "status": data["status"],
            "created_at": datetime.now().astimezone().isoformat(),
        }

        courses.append(new_course)
        save_courses(courses)

    except StorageError as error:
        return jsonify({
            "error": str(error)
        }), 500

    return jsonify(new_course), 201


@app.route("/api/courses", methods=["GET"])
@app.route("/api/courses/", methods=["GET"])
def get_all_courses():
    """
    Get all courses.

    Endpoints:
        GET /api/courses
        GET /api/courses/
    """
    try:
        courses = load_courses()
    except StorageError as error:
        return jsonify({
            "error": str(error)
        }), 500

    return jsonify(courses), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course(course_id):
    """
    Get one course by ID.

    Endpoints:
        GET /api/courses/<course_id>
        GET /api/courses/<course_id>/
    """
    try:
        courses = load_courses()
    except StorageError as error:
        return jsonify({
            "error": str(error)
        }), 500

    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
@app.route("/api/courses/<int:course_id>/", methods=["PUT"])
def update_course(course_id):
    """
    Replace all editable fields for an existing course.

    The ID and created_at timestamp are preserved.

    Endpoints:
        PUT /api/courses/<course_id>
        PUT /api/courses/<course_id>/
    """
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    try:
        courses = load_courses()
        course = find_course(courses, course_id)

        if course is None:
            return jsonify({
                "error": f"Course with ID {course_id} was not found."
            }), 404

        # Update only fields supplied by the API.
        course["name"] = data["name"].strip()
        course["description"] = data["description"].strip()
        course["target_date"] = data["target_date"]
        course["status"] = data["status"]

        save_courses(courses)

    except StorageError as error:
        return jsonify({
            "error": str(error)
        }), 500

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    """
    Delete a course by ID.

    Endpoints:
        DELETE /api/courses/<course_id>
        DELETE /api/courses/<course_id>/
    """
    try:
        courses = load_courses()
        course = find_course(courses, course_id)

        if course is None:
            return jsonify({
                "error": f"Course with ID {course_id} was not found."
            }), 404

        # Keep every course except the one being deleted.
        remaining_courses = [
            existing_course
            for existing_course in courses
            if existing_course.get("id") != course_id
        ]

        save_courses(remaining_courses)

    except StorageError as error:
        return jsonify({
            "error": str(error)
        }), 500

    return jsonify({
        "message": f"Course with ID {course_id} was deleted successfully."
    }), 200


# ---------------------------------------------------------
# General error handlers
# ---------------------------------------------------------

@app.errorhandler(404)
def handle_not_found(error):
    """Return JSON instead of Flask's default HTML 404 response."""
    return jsonify({
        "error": "The requested endpoint was not found."
    }), 404


@app.errorhandler(405)
def handle_method_not_allowed(error):
    """Return JSON when an HTTP method is not supported."""
    return jsonify({
        "error": "The HTTP method is not allowed for this endpoint."
    }), 405


@app.errorhandler(500)
def handle_internal_server_error(error):
    """Return JSON for unexpected server errors."""
    return jsonify({
        "error": "An unexpected internal server error occurred."
    }), 500


# ---------------------------------------------------------
# Start the development server
# ---------------------------------------------------------

if __name__ == "__main__":
    # load_courses() creates courses.json automatically if needed.
    try:
        load_courses()
    except StorageError as error:
        print(f"Could not initialize course storage: {error}")
        raise SystemExit(1)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )