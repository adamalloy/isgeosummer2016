import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_file, make_response, jsonify
from flask.ext.script import Manager, Server
import requests
from flask.ext.sqlalchemy import SQLAlchemy
import json
import csv
from flask.ext.pymongo import PyMongo
from db import db
# import logging why do I need logging


"""
# ------------------------------
# Configure logger for debugging
# ------------------------------
need to edit this and still don't totally understand what logger does
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.debug("Celeya Database Online.")
"""


# -------------
# Configure app
# -------------


SQLALCHEMY_DATABASE_URI = \
    '{engine}://{username}:{password}@{hostname}/{database}'.format(
        engine='mysql+pymysql',
        username=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        hostname=os.getenv('MYSQL_HOST'),
        database=os.getenv('MYSQL_DATABASE')
        )

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", use_debugger=True))
db = SQLAlchemy(app)
#--------------------
# Convert CSV To JSON
#--------------------
"""
This converts the comma separated values input file to a more usable JSON file.
Should I include the path as an input
"""
def convercsv():
	csvfile = open('/adamalloy/downloads/CeleyaData.csv', 'r')
	reader = csv.DictReader(csvfile, fieldnames =  ("Team Number", "Station Number", "Date and Time of Data", "Coordinates of Site", 
"Prepended text", "Station references", "Fault Name", "Data Type", "Strike of Fault", "Angle Between Surface and Slip or Dip", "Throw of Fault", "Slip of Fault", "Hand Written Notes", "Image 1 Link", "Image 1 Subject", "Image Description and Key Words", "Image 2 Link", "Image 2 Subject", "Image 2 Descrition and Key Words", "Image 3 Link","Image 3 Subject", "Image 3 Description and Key Words", "Track Map Image", "Track Map URL", "More Comments")
	out = json.dumps([ row for row in reader])
	print out
	return out


#----------------
# Database Models
#----------------

class SubsidencePoint(db.Model):

__tablename__ = 'SubsidencePoint'

# Dimensions
id = db.Column(db.Integer, primary_key=True)
team_number = db.Column(db.String(256))
station_number = db.Column(db.String(256))
data_time = db.Column(db.String(256))
coordinates = db.Column(db.String(256))
prepended_text = db.Column(db.String(256))
station_references = db.Column(db.String(256))
fault = db.Column(db.String(256))
data_type = db.Column(db.String(256))
strike = db.Column(db.Integer) #this may need to be float or string
angle = db.Column(db.Integer) #same
throw = db.Column(db.Integer) #same
slip = db.Column(db.Integer) #same
notes = db.Column(db.String(256))
image_1_link = db.Column(db.String(256)) 
image_1_subject = db.Column(db.String(256))
image_1_description = db.Column(db.String(256))
image_2_link = db.Column(db.String(256)) 
image_2_subject = db.Column(db.String(256))
image_2_description = db.Column(db.String(256))
image_3_link = db.Column(db.String(256)) 
image_3_subject = db.Column(db.String(256))
image_3_description = db.Column(db.String(256))

	def serialize(self):
	return dict(id = self.id, team_number = self.team_number, station_number = self.station_number, data_time = self.data_time, coordinates = self.coordinates, prepended_text = self.prepended_text, station_references = self.station_references , fault = self.fault, data_type = self.data_type, strike = self.strike, angle = self.angle, throw = self.throw, slip = self.slip, notes = self.notes, image_1_link = self. image_1_link, image_1_subject = self.image_1_subject, image_1_description = self.image_1_description, image_2_link = self.image_2_link, image_2_subject = self.image_2_subject, image_2_description = self.image_2_description,image_3_link = self.image_3_link, image_3_subject = self.image_3_subject, image_3_description = self.image_3_description)

#-------------
# initialize tables
#-------------


def init_subsidence_point(out):
	for data in out:
	s = SubsidencePoint(team_number = data["team_number"], station_number ["station_number"], data_time = data["data_time"], coordinates = data["coordinates"], prepended_text = data["prepended_text"], station_references = data["station_references"] , fault =data["fault"], data_type = data["data_type"], strike = data["strike"], angle = data["angle"], throw = data["throw"], slip = data["slip"], notes = data["notes"], image_1_link = data["image_1_link"], image_1_subject = data["image_1_subject"], image_1_description = data["image_1_description"], image_2_link = data["image_2_link"], image_2_subject = data["image_2_subject"], image_2_description = data["image_2_description"],image_3_link = data["image_3_link"], image_3_subject = data["image_3_subject"], image_3_description = data["image_3_description"])

@manager.command
def init_database
	db.drop_all()
	db.create_all()
	logger.debug("initializing subsidence points")
	init_subsidence_point(convertcsv(out))

	

# ----------------
# Manager Commands
# ----------------

@manager.command
def create_db():
    """
    This command is used to initialize the database and insert the data scraped     """

    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()
    db.create_all()
    init_db()
    db.session.commit()

@manager.command
def drop_db():
    """
    This command can be called to drop all tables used for our models.
    """
    # logger.debug("drop_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()

# -------
# Run App
# -------

if __name__ == '__main__':
    manager.run()


