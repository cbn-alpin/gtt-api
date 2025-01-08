from app import db

# User model
class User(db.Model):
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, email, first_name, last_name, is_admin=False, password=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.password = password


# Project model
class Project(db.Model):
    __tablename__ = 'project'

    id_project = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    is_archived = db.Column(db.Boolean, default=False)

    def __init__(self, code, name, description=None, start_date=None, end_date=None, is_archived=False):
        self.code = code
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.is_archived = is_archived


# Action model
class Action(db.Model):
    __tablename__ = 'action'

    id_action = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=True)
    id_project = db.Column(db.Integer, db.ForeignKey('project.id_project'), nullable=False)

    def __init__(self, name, description=None, id_project=None):
        self.name = name
        self.description = description
        self.id_project = id_project


# UserAction model
class UserAction(db.Model):
    __tablename__ = 'user_action'

    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), primary_key=True)
    id_action = db.Column(db.Integer, db.ForeignKey('action.id_action'), primary_key=True)

    def __init__(self, id_user, id_action):
        self.id_user = id_user
        self.id_action = id_action


# UserActionTime model
class UserActionTime(db.Model):
    __tablename__ = 'user_action_time'

    id_user_action_time = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Numeric, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    id_action = db.Column(db.Integer, db.ForeignKey('action.id_action'), nullable=False)

    def __init__(self, date, duration, id_user, id_action):
        self.date = date
        self.duration = duration
        self.id_user = id_user
        self.id_action = id_action


# Travel model
class Travel(db.Model):
    __tablename__ = 'travel'

    id_travel = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_place = db.Column(db.String(50), nullable=False)
    return_place = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    purpose = db.Column(db.String(50), nullable=False)
    start_municipality = db.Column(db.String(50), nullable=True)
    destination = db.Column(db.String(50), nullable=True)
    night_count = db.Column(db.SmallInteger, nullable=True)
    meal_count = db.Column(db.SmallInteger, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    license_vehicle = db.Column(db.String(12), nullable=True)
    comment_vehicle = db.Column(db.Text, nullable=True)
    start_km = db.Column(db.SmallInteger, nullable=True)
    end_km = db.Column(db.SmallInteger, nullable=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    id_project = db.Column(db.Integer, db.ForeignKey('project.id_project'), nullable=False)

    def __init__(self, start_date, end_date, start_place, return_place, status, purpose, id_user, id_project,
                 start_municipality=None, destination=None, night_count=None, meal_count=None, comment=None,
                 license_vehicle=None, comment_vehicle=None, start_km=None, end_km=None):
        self.start_date = start_date
        self.end_date = end_date
        self.start_place = start_place
        self.return_place = return_place
        self.status = status
        self.purpose = purpose
        self.id_user = id_user
        self.id_project = id_project
        self.start_municipality = start_municipality
        self.destination = destination
        self.night_count = night_count
        self.meal_count = meal_count
        self.comment = comment
        self.license_vehicle = license_vehicle
        self.comment_vehicle = comment_vehicle
        self.start_km = start_km
        self.end_km = end_km


# Expense model
class Expense(db.Model):
    __tablename__ = 'expense'

    id_expense = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    amount = db.Column(db.Numeric, nullable=False)
    id_travel = db.Column(db.Integer, db.ForeignKey('travel.id_travel'), nullable=False)

    def __init__(self, name, amount, id_travel, comment=None):
        self.name = name
        self.amount = amount
        self.id_travel = id_travel
        self.comment = comment
