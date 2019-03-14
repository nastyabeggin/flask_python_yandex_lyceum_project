from add_news_form import AddNewsForm
from db import DB
from flask import Flask, redirect, render_template, session, request
from login_form import LoginForm
from news_model import NewsModel
from users_model import UsersModel
from register_form import RegisterModel
from book_model import BookModel
from books_content import content
from books_form import BooksForm


import json
import cgi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
NewsModel(db.get_connection()).init_table()
UsersModel(db.get_connection()).init_table()

flag_perm = False

admins = json.loads(open('static/admins.txt', 'r', encoding='utf-8').read())

image = []
# print(admins)
# user_model_2 = UsersModel(db.get_connection())
# for i in admins:
#     if user_model_2.is_username_busy(i):
#         print(i)
#         user_model_2.insert(i, admins[i])

# один пользователь: test - username; qwerty123 - password


book_model = BookModel(db.get_connection())
for info in content:
    if not book_model.exists(info["title"], info["name"]):
        book_model.insert(info["img"], info["title"],
                          info["content"], info["year"], info["name"])


# http://127.0.0.1:8080/login

def make_session_permanent():
    session.permanent = False


@app.route('/login', methods=['GET', 'POST'])
def login():
    global flag_perm
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        perm = form.remember_me.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
            if perm:
                session.permanent = True
                flag_perm = True
            else:
                session.permanent = False
                flag_perm = True
            return redirect("/index")
        else:
            return render_template('login.html', form=form, error=1)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/')
@app.route('/index/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        form = cgi.FieldStorage()
        if 'username' not in session or not flag_perm and not session.permanent:
            if "username" in session:
                return redirect("/logout")
            return redirect('/login')
        news = NewsModel(db.get_connection()).get_all(session['user_id'])
        user_model = UsersModel(db.get_connection())
        all_news = NewsModel(db.get_connection()).get_all()
        all_users = user_model.get_all()
        if session['username'] in admins:
            return render_template('index.html', news=reversed(all_news),
                                   admins=admins, username=session['username'], all_users=all_users,
                                   adm_n=news)
        return render_template('index.html', username=session['username'], news=reversed(news), admins=admins)


@app.route('/site_users')
def site_users():
    if 'username' not in session:
        return redirect('/login')
    if session['username'] not in admins:
        return redirect('/')
    user_model = UsersModel(db.get_connection())
    num = user_model.get_all()
    all_users = []
    for i in num:
        id = i[0]
        username = i[1]
        password = i[2]
        k = user_model.count(id)
        all_users.append((id, username, password, k))
    return render_template('site_users.html', users=all_users, admins=admins, username=session['username'])


@app.route('/add_news/<book>', methods=['GET', 'POST'])
def add_news(book):
    if book == "none":
        if 'username' not in session:
            return redirect('/login')
        form = AddNewsForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            nm = NewsModel(db.get_connection())
            nm.insert("Без книги", title, content, session['user_id'])
            return redirect("/index")
        return render_template('add_news.html', title='Добавление заметки', form=form,
                               username=session['username'], admins=admins, book="")
    else:
        if 'username' not in session:
            return redirect('/login')
        form = AddNewsForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            nm = NewsModel(db.get_connection())
            nm.insert(book, title, content, session['user_id'])
            return redirect("/index")
        return render_template('add_news.html', title='Добавление заметки', form=form,
                               username=session['username'], admins=admins, book=book)


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


@app.route('/delete_book/<int:book_id>', methods=['GET'])
def delete_book(book_id):
    if 'username' not in session:
        return redirect('/login')
    bm = BookModel(db.get_connection())
    bm.delete(book_id)
    return redirect("/all_books")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'username' in session:
        return redirect('/')
    form = RegisterModel()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data
        user = UsersModel(db.get_connection())
        flag = user.is_username_busy(user_name)
        if flag and user_name not in admins:
            user.insert(user_name, password)
            session['username'] = user_name
            exists = user.exists(user_name, password)
            session['user_id'] = exists[1]
            return redirect("/")
        else:
            return render_template('register.html', form=form, error=1)
    return render_template('register.html', form=form)


@app.route('/all_books')
def all_books():
    if session['username'] in admins:
        book_model = BookModel(db.get_connection())
        old_books = book_model.get_all()
        books = []
        for i in range(len(old_books)):
            if i % 2 == 0:
                if i != len(old_books) - 1:
                    books.append(old_books[i] + old_books[i + 1])
        return render_template('all_books.html', show=1, books=books, username=session["username"], admins=admins)
    else:
        book_model = BookModel(db.get_connection())
        old_books = book_model.get_all()
        books = []
        for i in range(len(old_books)):
            if i % 2 == 0:
                if i != len(old_books) - 1:
                    books.append(old_books[i] + old_books[i + 1])
        return render_template('all_books.html', books=books, username=session["username"], admins=admins)


@app.route('/upload')
def upload_files():
    if 'username' not in session:
        return redirect('/')
    return render_template('add_book_img.html', show=1)


@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    if 'username' not in session:
        return redirect('/')
    form = BooksForm()
    image_name = image[-1]
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        year = form.year.data
        book = BookModel(db.get_connection())
        flag = book.is_title_busy(title)
        if not flag:
            book.insert(image_name, title, content, year, title)
            return redirect("/all_books")
        else:
            return render_template('add_book.html', form=form, error=1)
    return render_template('add_book.html', form=form)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        f = request.files['file']
        f.save("static/{}".format(f.filename))
        img_name = "/static/{}".format(f.filename)
        image.append(img_name)
        return redirect('/add_book')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
