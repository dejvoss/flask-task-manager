import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import AddTaskForm, EditTaskForm, CategoryForm
from datetime import datetime

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    categories = [category['category_name'] for category in mongo.db.categories.find()]
    form = AddTaskForm(categories)
    print(form.due_date.data)
    if form.validate_on_submit():

        tasks = mongo.db.tasks
        tasks.insert_one(request.form.to_dict())
        return redirect(url_for('get_tasks'))
    else:
        print(form.errors)
        print(form.due_date.data)

    return render_template('add_task.html', form=form)


@app.route('/edit_task/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    print(task_id)
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    print(the_task)
    categories = [category['category_name'] for category in mongo.db.categories.find()]
    form = EditTaskForm(categories)
    the_task['due_date'] = datetime.strptime(the_task['due_date'], '%Y-%m-%d')
    form.process(data=the_task)  # populate form with task data
    if request.method == 'POST':
        if form.validate_on_submit():
            tasks = mongo.db.tasks
            tasks.update_one(
                {'_id': ObjectId(task_id)},
                {'$set': {
                    'task_name': request.form.get('task_name'),
                    'category_name': request.form.get('category_name'),
                    'task_description': request.form.get('task_description'),
                    'due_date': request.form.get('due_date'),
                    'is_urgent': request.form.get('is_urgent')
                }}
            )
            return redirect(url_for('get_tasks'))
        else:
            print(form.errors)

    return render_template('edittask.html', task=the_task, form=form, categories=mongo.db.categories.find())


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find())


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.delete_one({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        categories = mongo.db.categories
        category_data = {
            'category_name': form.category_name.data,
        }
        categories.insert_one(category_data)
        return redirect(url_for('get_categories'))
    return render_template('add_category.html', form=form)


@app.route('/edit_category/<category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    the_category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    form = CategoryForm(data=the_category)
    if form.validate_on_submit():
        categories = mongo.db.categories
        category_data = {
            'category_name': form.category_name.data,
        }
        categories.update_one({'_id': ObjectId(category_id)}, {'$set': category_data})
        return redirect(url_for('get_categories'))

    return render_template('editcategory.html', category=the_category, form=form)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
