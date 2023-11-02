# --debug = att man slipper starta om programmet efter ändringar

from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)


def read_tasks():
    try:
        with open("tasks.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        with open("tasks.json", "w") as f:
            json.dump({}, f)
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
    try:
        tasks = read_tasks()
        task_list = tasks.get("tasks", [])

        for task in task_list:
            if task["id"] == task_id:
                task_to_get = task
                break


    except FileNotFoundError:
        return json.dumps({'message': 'File not found'})

    if task_to_get:
        return json.dumps(task_to_get, indent=2)
    else:
        return json.dumps({'message': 'Task not found'})


@app.route("/tasks", methods=["POST"])
def post_tasks():
    try:
        try:
            data = read_tasks()
        except json.JSONDecodeError: # om filen är tom eller i fel format
            data = {"tasks": []}

        if "tasks" not in data:
            data["tasks"] = []

        new_task = {"id": len(data["tasks"]) + 1,
                    "description": request.json.get("description"),
                    "category": request.json.get("category"),
                    "status": "pending"
                    }
        data["tasks"].append(new_task)

        with open("tasks.json", "w") as f:
            json.dump(data, f, indent=2)
        return {"msg": "Task added successfully!"}

    except FileNotFoundError:
        return {"msg": "File not found"}


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        tasks = read_tasks()
        task_list = tasks.get("tasks", [])

        for task in task_list:
            if task["id"] == task_id:
                task_list.remove(task)
                with open("tasks.json", "w") as f:
                    json.dump(tasks, f, indent=2)
                return json.dumps({"message": "Task deleted"})

    except FileNotFoundError:
        return json.dumps({'message': 'File not found'})


    return json.dumps({'message': 'Task not found'})


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def put_task(task_id):
    try:
        data = read_tasks()
        task_list = data.get("tasks", [])
        for task in task_list:
            if task["id"] == task_id:
                task["description"] = request.json.get("description", task["description"])
                task["category"] = request.json.get("category", task["category"])


                with open("tasks.json", "w") as f:
                    json.dump(data, f, indent=2)
                return {"msg": "Task updated successfully!"}

    except FileNotFoundError:
        return {"msg": "File not found"}


@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def task_complete(task_id):
    try:
        data = read_tasks()
        task_list = data.get("tasks", [])

        for task in task_list:
            if task["id"] == task_id:
                task["status"] = "complete"
                with open("tasks.json", "w") as f:
                    json.dump(data, f, indent=2)
                return {"msg": "Task is now complete!"}

    except FileNotFoundError:
        return {"msg": "File not found"}


@app.route("/tasks/categories", methods=["GET"])
def categories():
    try:
        category_set = set()
        data = read_tasks()
        task_list = data.get("tasks", [])
        for task in task_list:
            category_set.add(task["category"])

        unique_categories = list(category_set)
        return json.dumps(unique_categories, indent=2)

    except FileNotFoundError:
        return {"msg": "File not found"}


@app.route("/tasks/categories/<category_name>", methods=["GET"])
def get_tasks_by_category(category_name):

    data = read_tasks()
    task_list = data.get("tasks", [])
    tasks_in_category = []

    for task in task_list:

        if task.get("category") == category_name:
            tasks_in_category.append(task)

    return {"tasks_in_category": tasks_in_category}


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

