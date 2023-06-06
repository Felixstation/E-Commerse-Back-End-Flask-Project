from extensions import db , login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    full_name = db.Column(db.String(20) , nullable = False)
    email = db.Column(db.String(100) , nullable = False)
    password = db.Column(db.String(255) , nullable = False)
    comments = db.relationship('comments' , backref = 'User')
    favorite = db.relationship('Favorite' , backref= 'User')

    def __init__(self , full_name , email , password):
        self.full_name = full_name
        self.email = email
        self.password = password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.full_name

    def save(self):
        db.session.add(self)
        db.session.commit()


class color(db.Model):
    id = db.Column(db.Integer, primary_key = True , autoincrement = True)
    name = db.Column(db.String(20))
    product = db.relationship('product', backref = 'color')
   
    def __init__(self , name):
        self.name = name
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class size(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10))
    product = db.relationship('product', backref = 'size')

    def __init__(self,name):
        self.name = name
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()



class category(db.Model):
    id = db.Column(db.Integer, primary_key = True , autoincrement = True)
    name = db.Column(db.String(30))
    product = db.relationship('product', backref = 'category')
    
    def __init__(self,name):
        self.name = name
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class product(db.Model):
    id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    name = db.Column(db.String(100) , nullable = False)
    price = db.Column(db.Integer , nullable = False)
    old_price = db.Column(db.Integer , nullable = False)
    overview = db.Column(db.String(255) , nullable = False)
    category_id = db.Column(db.Integer ,db.ForeignKey('category.id') ,nullable = False)
    size_id = db.Column(db.Integer ,db.ForeignKey('size.id'))
    color_id = db.Column(db.Integer ,db.ForeignKey('color.id') , nullable = False)
    thumb_id = db.Column(db.String(50))
    description = db.Column(db.String(255) , nullable = False)
    image = db.relationship('image', backref = 'product')
    comments = db.relationship('comments' , backref = 'product')
    favorite = db.relationship('Favorite' , backref= 'product')
   
    def __init__(self , name , price , old_price , overview , category_id , size_id , color_id , description , thumb_id):
        self.name = name
        self.price = price
        self.old_price = old_price
        self.overview = overview 
        self.category_id = category_id
        self.size_id = size_id
        self.color_id = color_id
        self.description = description
        self.thumb_id = thumb_id

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


class image(db.Model):
    id = db.Column(db.Integer, primary_key=True ,autoincrement = True)
    name = db.Column(db.String(100) , nullable = False)  
    product_id = db.Column(db.Integer , db.ForeignKey('product.id'))
    

    def __init__(self , name):
        self.name = name

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()




class comments(db.Model):
    id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    comment = db.Column(db.String(255) , nullable = False)
    product_id = db.Column(db.Integer , db.ForeignKey('product.id'))
    published_date = db.Column(db.DateTime , default = datetime.utcnow)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))

    def __init__(self , comment , product_id , user_id):
        self.comment = comment
        self.product_id = product_id
        self.user_id = user_id
    
    def __repr__(self) :
        return self.comment

    def save(self):
        db.session.add(self)
        db.session.commit()



class Contact(db.Model):
    id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    name = db.Column(db.String(20) , nullable = False)
    email = db.Column(db.String(100) , nullable = False )
    subject = db.Column(db.String(50) , nullable = False)
    message = db.Column(db.String(255) , nullable = False)

    def __init__(self ,  name , email , subject , message):
       self.name = name
       self.email = email
       self.subject = subject
       self.message = message
    
    def __repr__(self):
        return self.comment

    def save(self):
        db.session.add(self)
        db.session.commit()


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer , db.ForeignKey('product.id'))



    def __init__(self , product_id  , user_id):
       self.product_id = product_id
       self.user_id = user_id
    
    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()
