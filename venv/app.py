# --debug = att man slipper starta om programmet efter ändringar

from flask import Flask, request, render_template, redirect, url_for, jsonify
import json

app = Flask(__name__)


@app.errorhandler(404)
def route_not_found(e):
    return "Route not found. Check if you spelled it correctly"


def read_tasks():
    try:
        with open("tasks.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        with open("tasks.json", "w") as f:
            json.dump({"tasks": []}, f)
        return json.dumps({"Message": "File not found. Created a new tasks file."})
    except json.JSONDecodeError:
        return {"error": "Invalid JSON data in tasks file"}


@app.route("/")
def index():
    task_list = read_tasks()
    return render_template("web.html", tasks=task_list)


@app.route("/submit", methods=["POST"])
def submit_task_from_html():
    tasks = read_tasks()
    new_task = {
        "id": len(tasks["tasks"]) + 1,
        "description": request.form.get("description"),
        "category": request.form.get("category"),
        "status": "pending"
    }
    tasks["tasks"].append(new_task)

    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)

    return redirect(url_for("index"))


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = read_tasks()
    return tasks


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task_id(task_id):
    task_to_get = []

    tasks = read_tasks()
    task_list = tasks.get("tasks", [])

    for task in task_list:
        if task["id"] == task_id:
            task_to_get = task
            break

    if task_to_get:
        return {f"Task {task_id}": task_to_get}
    else:
        return json.dumps({"message": f"Found no task with id: {task_id}"})


@app.route("/tasks", methods=["POST"])
def post_tasks():

    data = read_tasks()
    request_json = request.get_json()
    allowed_keys = ["description", "category"]

    for key in request_json.keys():
        if key not in allowed_keys:
            response = jsonify(
                {"error": f"Invalid key {key} in JSON data. Only 'description' and 'category' keys are allowed."})
            return response

    new_task = {
        "id": len(data["tasks"]) + 1,
        "description": request_json.get("description"),
        "category": request_json.get("category"),
        "status": "pending"
    }
    data["tasks"].append(new_task)

    with open("tasks.json", "w") as f:
        json.dump(data, f, indent=2)
    return {"msg": "Task added successfully!"}


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    tasks = read_tasks()
    task_list = tasks.get("tasks", [])

    for task in task_list:
        if task["id"] == task_id:
            task_list.remove(task)
            with open("tasks.json", "w") as f:
                json.dump(tasks, f, indent=2)
            return json.dumps({"message": "Task deleted"})

    return json.dumps({"message": f"Found no task with id: {task_id}"})



@app.route("/tasks/<int:task_id>", methods=["PUT"])
def put_task(task_id):

    data = read_tasks()
    task_list = data.get("tasks", [])
    for task in task_list:
        if task["id"] == task_id:
            task["description"] = request.json.get("description", task["description"])
            task["category"] = request.json.get("category", task["category"])


            with open("tasks.json", "w") as f:
                json.dump(data, f, indent=2)
            return {"message": "Task updated successfully!"}

    return {"message": f"Found no task with id: {task_id}"}



@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def task_complete(task_id):

    data = read_tasks()
    task_list = data.get("tasks", [])

    for task in task_list:
        if task["id"] == task_id:
            task["status"] = "complete"
            with open("tasks.json", "w") as f:
                json.dump(data, f, indent=2)
            return {"message": "Task is now complete!"}

    return {'message': f"Found no task with id: {task_id}"}



@app.route("/tasks/categories", methods=["GET"])
def categories():

    category_set = set()
    data = read_tasks()
    task_list = data.get("tasks", [])
    for task in task_list:
        category_set.add(task["category"])

    unique_categories = list(category_set)
    return {"categories": unique_categories}



@app.route("/tasks/categories/<category_name>", methods=["GET"])
def get_tasks_by_category(category_name):
    data = read_tasks()
    task_list = data.get("tasks", [])
    tasks_in_category = []
    category_found = False

    for task in task_list:
        if task.get("category") == category_name:
            tasks_in_category.append(task)
            category_found = True

    if not category_found:
        return json.dumps({"message": f"Found no category with the name: {category_name}"})

    return {f"tasks_in_category - {category_name}": tasks_in_category}



@app.route("/tasks/completedornot", methods=["GET"])
def completed_or_not():
    data = read_tasks()
    task_list = data.get("tasks", [])
    completed_tasks = []
    not_completed_tasks = []

    for task in task_list:
        if task.get("status") == "complete":
            completed_tasks.append(task)
        elif task.get("status") == "pending":
            not_completed_tasks.append(task)
    return {"completed tasks": completed_tasks, "Unfinished tasks": not_completed_tasks}



if __name__ == '__main__':
   app.run()

