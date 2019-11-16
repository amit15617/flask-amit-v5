from smartStore import db, app
from flask import render_template, redirect, request, url_for, abort, session, flash
from flask_login import login_user,login_required, logout_user
from smartStore.models import User, Admin, Products
from smartStore.forms import LoginForm, RegistrationForm, AdminLoginForm,AddProductForm, SearchProductForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

################################
####  ADMIN DETAILS ############
##### ID- admin@admin.com ######
##### Pass- admin ###############
################################
# db.create_all()
# admin = Admin(email = 'admin@admin.com', username = 'admin1', password = 'admin')
# db.session.add(admin)
# db.session.commit()


admin =False
@app.route('/')
def home():
    return render_template('home.html',admin=admin)


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html',admin=admin)
 
@app.route('/welcome_admin', methods=['GET','POST'])
@login_required
def welcome_admin(): 
    print(admin)
    product_list =[]

    
    for  i in Products.query.with_entities(Products.category, func.count(Products.category)).group_by(Products.category).all():
        product_list.append(list(i))
    
    form = AddProductForm()
    if form.validate_on_submit():
        product = Products(name=form.name.data,description=form.description.data,price=form.price.data,category=form.category.data)
        db.session.add(product)
        db.session.commit()
        flash("added successfully")
        return redirect(url_for('view_products'))
    return render_template("welcome_admin.html",form=form,admin=admin,product_list=product_list)


@app.route('/view_products', methods=['GET','POST'])
@login_required
def view_products():
    products = Products.query.all()
    product_list =[]
    product_price=[]

    for  i in Products.query.with_entities(Products.price, func.count(Products.price)).group_by(Products.price).all():
        product_price.append(list(i))
        
    for  i in Products.query.with_entities(Products.category, func.count(Products.category)).group_by(Products.category).all():
        product_list.append(list(i))
    return render_template('viewproduct.html',products = products,product_list = product_list,admin=admin)


@app.route('/search_products', methods=['GET','POST'])
@login_required
def search_products():
    form = SearchProductForm()
    if form.validate_on_submit():
        search_results = Products.query.filter_by(name=form.productname.data)
        return render_template('viewproduct.html',products = search_results)
    return render_template("searchproduct.html",form=form,admin=admin)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/adminlogout')
@login_required
def adminlogout():
    logout_user()
    global admin 
    admin=False
    return redirect(url_for('home'))

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():

    
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('welcome_admin')
                global admin 
                admin=True
            return redirect(next)
            
    return render_template('adminlogin.html', form=form,admin=admin)

@app.route('/products', methods = ['GET', 'POST'])
@login_required
def products():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form,admin=admin)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form,admin=admin)


if __name__ == '__main__':
    app.run(debug=True)
