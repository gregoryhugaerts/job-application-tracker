from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
    abort,
    request,
)
from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms_alchemy import ModelFormField, model_form_factory

from .models import Application, Company, db

applications_bp = Blueprint("applications", __name__)

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(cls):
        return db.session


class CompanyForm(ModelForm):
    class Meta:
        model = Company


class ApplicationForm(ModelForm):
    class Meta:
        model = Application

    company = ModelFormField(CompanyForm)


@applications_bp.route("/")
@applications_bp.route("/applications")
def applications():
    applications = db.session.scalars(
        select(Application).order_by(Application.applied_on),
    ).all()
    return render_template(
        "applications/applications.html",
        applications=applications,
    )


@applications_bp.route("/applications/new", methods=["GET", "POST"])
def create_application():
    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application()
        form.populate_obj(application)
        db.session.add(application)
        db.session.commit()
        flash("Application created successfully!", "success")
        return redirect(url_for("applications.applications"))
    return render_template("applications/create_application.html", form=form)


@applications_bp.route(
    "/applications/<int:application_id>/edit", methods=["GET", "POST"]
)
def edit_application(application_id):
    application = db.session.scalars(
        select(Application).where(Application.id == application_id)
    ).one_or_none()
    if application is None:
        abort(404)
    form = ApplicationForm(obj=application)
    if form.validate_on_submit():
        form.populate_obj(application)
        db.session.commit()
        flash("Application updated successfully!", "success")
        return redirect(url_for("applications.applications"))
    return render_template("applications/edit_application.html", form=form)


@applications_bp.route(
    "/applications/<int:application_id>/delete", methods=["GET", "POST"]
)
def delete_application(application_id):
    application = db.session.scalars(
        select(Application).where(Application.id == application_id)
    ).one_or_none()
    if application is None:
        abort(404)
    if request.method == "POST":
        db.session.delete(application)
        db.session.commit()
        flash("Application deleted successfully!", "success")
        return redirect(url_for("applications.applications"))
    return render_template(
        "applications/delete_application.html", application=application
    )
