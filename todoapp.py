from flask import Flask, request, redirect, render_template_string
import re
import os
import pickle

app = Flask(__name__)
DATA_FILE = 'todo_data.pkl'

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'rb') as f:
        todo_list = pickle.load(f)
else:
    todo_list = []


template = """
<!doctype html>
<html>
<head><title>To-Do List</title></head>
<body>
    <h1>To-Do List</h1>
    {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
    <table border="1">
        <tr><th>Task</th><th>Email</th><th>Priority</th><th>Action</th></tr>
        {% for item in todo_list %}
        <tr>
            <td>{{ item['task'] }}</td>
            <td>{{ item['email'] }}</td>
            <td>{{ item['priority'] }}</td>
            <td>
                <form method="POST" action="/delete/{{ loop.index0 }}">
                    <button type="submit">Delete</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>

    <h2>Add New Item</h2>
    <form method="POST" action="/submit">
        Task: <input type="text" name="task"><br>
        Email: <input type="text" name="email"><br>
        Priority:
        <select name="priority">
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
        </select><br>
        <button type="submit">Add To Do Item</button>
    </form>

    <form method="POST" action="/clear">
        <button type="submit">Clear</button>
    </form>

    <form method="POST" action="/save">
        <button type="submit">Save</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(template, todo_list=todo_list, error=None)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form.get('task', '').strip()
    email = request.form.get('email', '').strip()
    priority = request.form.get('priority', '').strip()

    if not task or not email or not priority:
        return render_template_string(template, todo_list=todo_list, error="All fields are required.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return render_template_string(template, todo_list=todo_list, error="Invalid email format.")
    if priority not in ['Low', 'Medium', 'High']:
        return render_template_string(template, todo_list=todo_list, error="Invalid priority level.")

    todo_list.append({'task': task, 'email': email, 'priority': priority})
    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    todo_list.clear()
    return redirect('/')

@app.route('/save', methods=['POST'])
def save():
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(todo_list, f)
    return redirect('/')

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    if 0 <= item_id < len(todo_list):
        todo_list.pop(item_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
