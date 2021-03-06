from main import db
from models.ProfileImage import ProfileImage
from models.Locations import Location
from models.Group_members import GroupMembers
from models.Posts import Posts
from models.Comments import Comments


class Profile(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    profile_image = db.relationship(
        ProfileImage, backref="profile", uselist=False)
    locations = db.relationship(Location, backref="profile", lazy="dynamic")
    groups = db.relationship(GroupMembers, backref="profiles")
    posts = db.relationship(Posts, backref="profile", lazy="dynamic")
    comments = db.relationship(Comments, backref="profile", lazy="dynamic")

    def __repr__(self):
        return f"Profile: {self.id}"
