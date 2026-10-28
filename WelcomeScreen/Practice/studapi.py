from flask import Flask, request, jsonify

app = Flask(__name__)

students = [
    {"id": 1, "name": "Riya", "age": 16}
]

# GET: Read all students
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)

# POST: Create a student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    new_student = {
        "id": len(students) + 1,
        "name": data["name"],
        "age": data["age"]
    }

    students.append(new_student)

    return jsonify(new_student), 201

# DELETE: Delete one student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    global students

    students = [
        student for student in students
        if student["id"] != student_id
    ]

    return "", 204

if __name__ == "__main__":
    app.run(debug=True)