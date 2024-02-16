from flask import Flask,url_for,flash,render_template,request,redirect
import pyodbc


app = Flask(__name__)
# Session and cache
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'


server = 'beerprocesssimulatorsql.database.windows.net'
database = 'CloudCherryTreeDB'
username = 'titansax'
password = 'SecretoGlasgow11!'
drivers = [item for item in pyodbc.drivers()]
driver = drivers[-1]



@app.route('/')

def Index():
    #Create a connection string
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    cur = cnxn.cursor()

    cur.execute('SELECT * FROM posts')
    data = cur.fetchall()
    cur.execute('SELECT DISTINCT technology FROM [dbo].[posts]')
    uniquedata = cur.fetchall()
    return render_template('index.html',posts=data, technologies= uniquedata)

@app.route('/filter/<technology>')

def filter_technology(technology):
    technology_selected = technology

    #Create a connection string
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cur = cnxn.cursor()
    cur.execute('SELECT * FROM [dbo].[posts] Where Technology = ?',technology_selected)
    data = cur.fetchall()
    cur.execute('SELECT DISTINCT technology FROM [dbo].[posts]')
    uniquedata = cur.fetchall()
    return render_template('index.html',posts=data, technologies= uniquedata)


@app.route('/add/<id>')
def create_post_form(id):
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cur = cnxn.cursor()

    cur.execute('SELECT * FROM posts WHERE id = ?', id)
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('add-post.html', post = data[0])


@app.route('/add_post', methods=['POST'])
def add_post():
    if request.method == 'POST':
       technology = request.form['technology']
       post = request.form['post']

       # Create a connection string
       cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
       cur = cnxn.cursor()
       cur.execute('INSERT INTO posts (technology,post) VALUES(?,?)',
       (technology,post))
       cnxn.commit()
       cnxn.close()
       flash('Post added successfully')
       return redirect(url_for('Index'))

@app.route('/edit/<id>')
def edit_post(id):
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cur = cnxn.cursor()

    cur.execute('SELECT * FROM posts WHERE id = ?', id)
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-post.html', post = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_post(id):
    if request.method == 'POST':
        technology = request.form['technology']
        post = request.form['post']
        cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cur = cnxn.cursor()
        cur.execute("""
            UPDATE posts 
            SET fullname = %s,
                technology = %s,
                post = %s
            WHERE id = %s
        """, (technology,post,id))
        cnxn.commit()
        cnxn.close()
        flash('Post Updated Succesfully')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_post(id):
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cur = cnxn.cursor()
    cur.execute('DELETE FROM posts WHERE id = {0}'.format(id))
    cnxn.commit()
    cnxn.close()
    flash('Post deleted successfully')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)

