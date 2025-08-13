from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"


class LeaveApplicationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    department = StringField("Department", validators=[DataRequired()])
    reason = TextAreaField("Reason", validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[DataRequired()], format="%Y-%m-%d")
    end_date = DateField("End Date", validators=[DataRequired()], format="%Y-%m-%d")
    submit = SubmitField("Apply Leave")

    def validate(self):
        rv = super().validate()
        if not rv:
            return False
        if self.end_date.data < self.start_date.data:
            self.end_date.errors.append("End date cannot be earlier than start date.")
            return False
        return True

@app.route("/")
def home():
    return redirect(url_for("leave_application"))

@app.route("/", methods=["GET", "POST"])
def leave_application():
    form = LeaveApplicationForm()
    if form.validate_on_submit():
        duration = (form.end_date.data - form.start_date.data).days + 1
        flash(f"Leave applied successfully for {duration} day(s)!", "success")
        return redirect(url_for("leave_application"))
    return render_template("leave_application.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
