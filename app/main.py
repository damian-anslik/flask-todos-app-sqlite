from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models import Todo
from . import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/todos")
@login_required
def todos():
    """
    This function renders the todos page.

    args:
        None
    """
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template("todos.html", todos=todos)


@main.route("/todos", methods=["POST"])
@login_required
def add_todo():
    """
    Add a todo to the database
    args:
        request: the request object
    """
    todo_description = request.form.get("todo_description")
    if not todo_description:
        flash("Please enter a todo description")
        return redirect(url_for("main.todos"))
    todo = Todo(
        description=request.form.get("todo_description"), user_id=current_user.id
    )
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("main.todos"))


@main.route("/todos/<int:todo_id>/delete", methods=["DELETE"])
@login_required
def delete_todo(todo_id: int):
    """
    Delete a todo item
    args:
        todo_id: int
    """
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:  # check if the user is the owner of the todo
        return "Forbidden", 403
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("main.todos"))


@main.route("/todos/<int:todo_id>/set-completed", methods=["PUT"])
@login_required
def set_completed_todo(todo_id: int):
    """
    Set a todo item as completed
    args:
        todo_id: int
    """
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:  # check if the user is the owner of the todo
        return "Forbidden", 403
    todo.completed = True
    db.session.commit()
    return redirect(url_for("main.todos"))
