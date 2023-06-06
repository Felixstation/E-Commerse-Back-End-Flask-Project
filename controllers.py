from app import app
from flask import render_template, request , redirect , flash
from models import * 
from forms import RegisterForm, LoginForm , SearchForm , CommentForm , ContactForm , FavoriteForm
from werkzeug.security import generate_password_hash
from flask_login import login_user , logout_user , login_required , current_user
from extensions import db

@app.context_processor
def base():
    form = SearchForm()
    return dict(form = form)


@app.route('/register' , methods = ['GET' , 'POST'])
def registry():
    form = RegisterForm()
    categories = category.query.all()
    favorite_items = Favorite.query.all()
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            user = User(
                full_name = form.full_name.data,
                email = form.email.data,
                password = generate_password_hash(form.password.data),

            )
            db.session.add(user)
            db.session.commit()
            return redirect ('/login')
        else: flash('Please Check Your Information')
    return render_template('register.html' , form = form , categories = categories , favorite_items = favorite_items)


@app.route('/login' , methods = ['GET' , 'POST'])
def LoGin():
    form = LoginForm()
    categories = category.query.all()
    favorite_items = Favorite.query.all()
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect ('/')
            else: flash('Check Your Information')   
    return render_template('login.html' , form = form , categories = categories , favorite_items = favorite_items)


@app.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect('/')


@app.route('/')
def home():
    items = product.query.all()
    categories = category.query.all()
    Colors = color.query.all()
    sizes = size.query.all()
    max_price = request.args.get('max_price')
    min_price = request.args.get('min_price')
    color_name = request.args.get('color')
    favorite_items = Favorite.query.all()
    size_name = request.args.get('size')



    price_1=  product.query.filter(product.price.between(0, 100 )).all()  
    price_2=  product.query.filter(product.price.between(100, 200 )).all()  
    price_3=  product.query.filter(product.price.between(200, 300 )).all()  
    price_4=  product.query.filter(product.price.between(300, 400 )).all()  
    price_5=  product.query.filter(product.price.between(400, 500 )).all()  

    
    
    

    if color_name:
        Color = color.query.filter_by(name = color_name).first()
        items = product.query.filter_by(color_id= Color.id).all()
        return render_template('shop.html'  , products = items  , categories = categories , colors = Colors ,  price_1= price_1 , 
                               price_2=price_2 , price_3 =price_3 , price_4 =price_4 ,price_5 = price_5 , sizes = sizes)
    

    if size_name:
        Size = size.query.filter_by(name = size_name).first()
        items = product.query.filter_by(size_id= Size.id).all()   
        return render_template('shop.html'  , products = items  , categories = categories ,colors = Colors , sizes = sizes ,  
                               price_1= price_1 , price_2=price_2 , price_3 =price_3 , price_4 =price_4 ,price_5 = price_5)
    
    
    if min_price and max_price:
        items= product.query.filter(product.price.between(min_price, max_price )).all()  
        items_count = product.query.filter_by(price = id).all()  
        return render_template('shop.html'  , products = items  ,count = items_count, categories = categories , sizes=sizes ,colors = Colors ,  
                               price_1= price_1 , price_2=price_2 , price_3 =price_3 , price_4 =price_4 ,price_5 = price_5)
    
    
    return render_template('shop.html'  , products = items  , categories = categories , sizes=sizes ,colors = Colors, 
                           price_1= price_1 , price_2=price_2 , price_3 =price_3 , price_4 =price_4 ,price_5 = price_5  , 
                           favorite_items = favorite_items)



@app.route('/detail/<int:id>' , methods = ['GET' , 'POST'])
def detail_page(id):
    products = product.query.filter_by(id = id).first()
    main_image = image.query.filter_by(product_id = id).first()
    images = image.query.filter_by(product_id = id).all()[1:]
    form = CommentForm(formdata= None)
    Comments = comments.query.filter_by(product_id = id)
    count = comments.query.filter_by(product_id = id).count()
    categories = category.query.all()
    same_products = category.query.filter_by(id = products.category_id).first().product[1::]
    favorite_items = Favorite.query.all()
    Color = color.query.filter_by(id = products.color_id).first()
    Size = size.query.filter_by(id = products.size_id).first()


    form_favorite = FavoriteForm()
    if request.method == 'POST':
        form = CommentForm(request.form)
        form_favorite = FavoriteForm(request.form)
        favorite = Favorite(
            product_id = id,
            user_id = current_user.id

                    )   
        favorite.save()
                
        
        if form.validate_on_submit():
            Comment = comments(
                comment = form.comment.data,
                product_id = id,
                user_id = current_user.id
            )
            
            Comment.save() 

       
        

    
    
    return render_template('detail.html' , product = products , same_products = same_products , images = images, main_image = main_image ,
                            comment = form , comment_view = Comments , count = count , categories = categories , favorite = form_favorite , 
                            favorite_items = favorite_items , color = Color , size = Size)


@app.route('/favorites')
def favorites():
    favorite_items = Favorite.query.all()
    
    return render_template('favorites.html' , favorite_items = favorite_items)



@app.route('/favorites/delete/<int:id>' , methods = ['GET' , 'POST'])
def delete_favorites(id):
    products = Favorite.query.filter_by(product_id = id).first()
    if products:
        db.session.delete(products)
        db.session.commit()
        return favorites()
    return render_template('favorites.html')


@app.route("/category/<string:name>")
def categories(name):
    items = category.query.filter_by(name = name).first().product
    categories = category.query.all()
    count = category.query.filter_by(name = name).count()
    favorite_items = Favorite.query.all()
    return render_template('shop.html', products = items, categories = categories , count = count , favorite_items = favorite_items)


@app.route('/search' , methods = ['POST'])
def search():   
    form = SearchForm()
    searching = product.query
    categories = category.query.all()
    favorite_items = Favorite.query.all()
    if form.validate_on_submit():
        search.searched = form.searched.data

        searching = searching.filter(product.name.like('%' + search.searched + '%'))
        searching = searching.order_by(product.name).all()
        return render_template('search.html' , form = form , searched = search.searched , searching = searching, 
                               product = product , categories = categories , favorite_items = favorite_items )
    

@app.route('/contact' , methods = ['GET' , 'POST'])
def contact_page():
    form = ContactForm(formdata= None)
    categories = category.query.all()
    if request.method == 'POST':
        form = ContactForm(request.form)
        if form.validate_on_submit():
            contact = Contact(
                name = form.name.data,
                email = form.email.data,
                subject = form.subject.data,
                message = form.message.data

            )
            flash("Succesfully Sent")
            db.session.add(contact)
            db.session.commit()
        else:
            flash('Please Check Your Information: ')
    return render_template('contact.html' , form = form , categories = categories)

