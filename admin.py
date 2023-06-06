from extensions import db , admin
from flask_admin.contrib.sqla import ModelView
from models import *






admin.add_view(ModelView(product , db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(image, db.session))
admin.add_view(ModelView(size, db.session))
admin.add_view(ModelView(color, db.session))
admin.add_view(ModelView(category, db.session))
admin.add_view(ModelView(comments, db.session))


