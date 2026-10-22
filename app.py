from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
tasks = [
    {"id": 1, "title": "Learn Docker basics", "done": False},
    {"id": 2, "title": "Understand Jenkins pipeline", "done": True},
]
next_id = 3

@app.route("/")
def home():
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    global next_id
    title = request.form.get("title", "").strip()
    if title:
        tasks.append({"id": next_id, "title": title, "done": False})
        next_id += 1
    return redirect(url_for("home"))

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect(url_for("home"))

@app.route("/health")
def health():
    return {"status": "healthy", "application": "Student Task Tracker"}, 200

@app.route("/version")
def version():
    return {"message": "Student Task Tracker - CI/CD Version 1"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
