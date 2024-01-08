from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from datetime import datetime


class MyDateField(DateField):
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                self.data = None
                raise ValueError('Invalid date format')


class AddTaskForm(FlaskForm):
    task_name = StringField('Task Name', validators=[DataRequired()])
    category_name = SelectField('Category Name', validators=[DataRequired()], choices=[])
    task_description = TextAreaField('Task Description')
    due_date = MyDateField('Due Date', validators=[DataRequired()])
    is_urgent = BooleanField('Is Urgent')
    submit = SubmitField('Add Task')

    def __init__(self, categories, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.category_name.choices = [(category, category) for category in categories]


class EditTaskForm(FlaskForm):
    task_name = StringField('Task Name', validators=[DataRequired()])
    category_name = SelectField('Category Name', validators=[DataRequired()], choices=[])
    task_description = TextAreaField('Task Description')
    due_date = DateField('Due Date', validators=[DataRequired()])
    is_urgent = BooleanField('Is Urgent')
    submit = SubmitField('Update Task')

    def __init__(self, categories, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)
        self.category_name.choices = [(category, category) for category in categories]


class CategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Add Category')
