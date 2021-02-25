from models.Profile import Profile
from models.ProfileImage import ProfileImage
from main import db
from schemas.ProfileSchema import profile_schema
from schemas.ProfileImageSchema import profile_image_schema
from flask import current_app, Blueprint, request, jsonify, render_template, redirect, url_for, flash, abort, Response
from flask_login import current_user, login_required
from pathlib import Path
import boto3
import os
from forms import ProfileForm, ProfileImageUpload

profile = Blueprint('profile', __name__, url_prefix="/web/profile")


def retrieve_profile():
    user_id = current_user.get_id()
    profile = Profile.query.filter_by(user_id=user_id).first()
    return user_id, profile

def retrieve_profile_picture(profile_image):
    s3 = boto3.client('s3')
    bucket = os.environ.get("AWS_S3_BUCKET")
    url = s3.generate_presigned_url('get_object', Params= {"Bucket": bucket, "Key": f"profile_images/{profile_image.filename}"}, ExpiresIn=5)
    return url
    # bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    # filename = profile_image.filename
    # file_obj = bucket.Object(f"profile_images/{filename}").get()

    # return Response(
    #     file_obj["Body"].read(),
    #     mimetype="image/*",
    #     headers={"Content-Disposition": f"attachment; filename=image"}
    # )

@profile.route("/", methods=["GET", "POST"])
@login_required
def profile_page():
    user_id, profile = retrieve_profile()
    profile_image = ProfileImage.query.filter_by(profile_id=profile.id).first()
    
    form = ProfileForm()
    uploadform = ProfileImageUpload()
    if form.validate_on_submit():
        new_profile = Profile(
            name=form.profile_name.data,
            user_id=user_id
        )
        db.session.add(new_profile)
        db.session.commit()
        flash("Profile name confirmed!")
        return redirect(url_for("profile.profile_page"))

    image = retrieve_profile_picture(profile_image)

    return render_template(
        "profile.html", profile=profile, form=form, uploadform=uploadform, image=image)


@profile.route("/uploadimage", methods=["GET", "POST"])
@login_required
def profile_image():
    user_id, profile = retrieve_profile()

    form = ProfileImageUpload()
    if form.validate_on_submit():
        image = form.image.data
        filename = f"{profile.id}-profile_image"
        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        key = f"profile_images/{filename}"
        bucket.upload_fileobj(image, key)

        if not profile.profile_image:
            new_image = ProfileImage()
            new_image.filename = filename
            profile.profile_image = new_image
            db.session.commit()

        return ("Upload successful")
    
    return "Upload not successful"


@profile.route("/profileimage", methods=["GET"])
def profile_image_show():
    profile_image = ProfileImage.query.get(3)

    return retrieve_profile_picture(profile_image)