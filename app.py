from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

# Get database credentials from environment variables for security
server = os.getenv('DB_SERVER', 'xxxxxxxxxxxxx')
database = os.getenv('DB_DATABASE', 'xxxxxxxxxxxxxx')
username = os.getenv('DB_USERNAME', 'xxxxxxxxxxxxxx')
password = os.getenv('DB_PASSWORD', 'xxxxxxxxxxxxxx')

# Ensure the ODBC driver is set correctly
driver = 'ODBC Driver 18 for SQL Server'

# Function to create the database connection
def create_connection():
    connection = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return connection

@app.route('/')
def index():
    cnxn = create_connection()
    cur = cnxn.cursor()

    try:
        cur.execute('SELECT * FROM posts')
        data = cur.fetchall()

        cur.execute('SELECT DISTINCT technology FROM [dbo].[posts]')
        uniquedata = cur.fetchall()

    except pyodbc.Error as e:
        flash(f"Database error: {e}", 'error')
        return render_template('index.html', posts=[], technologies=[])

    finally:
        cur.close()
        cnxn.close()
        print(data)
        print(uniquedata)

    return render_template('index.html', posts=data, technologies=uniquedata)


@app.route('/filter', methods=['GET'])
def filter_posts():
    technology = request.args.get('technology', '')
    post_keyword = request.args.get('post', '')

    cnxn = create_connection()
    cur = cnxn.cursor()

    try:
        query = 'SELECT * FROM [dbo].[posts] WHERE 1=1'
        params = []

        if technology:
            query += ' AND technology = ?'
            params.append(technology)

        if post_keyword:
            query += ' AND post LIKE ?'
            params.append(f'%{post_keyword}%')

        cur.execute(query, params)
        data = cur.fetchall()

        cur.execute('SELECT DISTINCT technology FROM [dbo].[posts]')
        uniquedata = cur.fetchall()

    except pyodbc.Error as e:
        flash(f"Database error: {e}", 'error')
        return render_template('index.html', posts=[], technologies=[])

    finally:
        cur.close()
        cnxn.close()

    return render_template('index.html', posts=data, technologies=uniquedata)




@app.route('/filter/<technology>')
def filter_technology(technology):
    cnxn = create_connection()
    cur = cnxn.cursor()

    try:
        cur.execute('SELECT * FROM [dbo].[posts] WHERE Technology = ?', technology)
        data = cur.fetchall()

        cur.execute('SELECT DISTINCT technology FROM [dbo].[posts]')
        uniquedata = cur.fetchall()

    except pyodbc.Error as e:
        flash(f"Database error: {e}", 'error')
        return render_template('index.html', posts=[], technologies=[])

    finally:
        cur.close()
        cnxn.close()

    return render_template('index.html', posts=data, technologies=uniquedata)

@app.route('/add/<id>')
def create_post_form(id):
    cnxn = create_connection()
    cur = cnxn.cursor()

    try:
        cur.execute('SELECT * FROM posts WHERE id = ?', id)
        data = cur.fetchall()
        return render_template('add-post.html', post=data[0] if data else None)
    except pyodbc.Error as e:
        flash(f"Database error: {e}", 'error')
        return redirect(url_for('index'))
    finally:
        cur.close()
        cnxn.close()

@app.route('/add_post', methods=['POST'])
def add_post():
    if request.method == 'POST':
        technology = request.form['technology']
        post = request.form['post']

        cnxn = create_connection()
        cur = cnxn.cursor()

        try:
            cur.execute('INSERT INTO posts (technology, post) VALUES (?, ?)', (technology, post))
            cnxn.commit()
            flash('Post added successfully', 'success')

        except pyodbc.Error as e:
            flash(f"Database error: {e}", 'error')

        finally:
            cur.close()
            cnxn.close()

        return redirect(url_for('index'))

@app.route('/edit/<id>')
def edit_post(id):
    cnxn = create_connection()
    cur = cnxn.cursor()

    try:
        cur.execute('SELECT * FROM posts WHERE id = ?', id)
        data = cur.fetchall()
        return render_template('edit-post.html', post=data[0] if data else None)
    except pyodbc.Error as e:
        flash(f"Database error: {e}", 'error')
        return redirect(url_for('index'))
    finally:
        cur.close()
        cnxn.close()

@app.route('/update/<id>', methods=['POST'])
def update_post(id):
    if request.method == 'POST':
        technology = request.form['technology']
        post = request.form['post']

        cnxn = create_connection()
        cur = cnxn.cursor()

        try:
            cur.execute("""
                UPDATE posts 
                SET technology = ?, post = ?
                WHERE id = ?
            """, (technology, post, id))
            cnxn.commit()
            flash('Post updated successfully', 'success')

        except pyodbc.Error as e:
            flash(f"Database error: {e}", 'error')

        finally:
            cur.close()
            cnxn.close()

        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_post(id):
    cnxn = create_connection()
    cur = cnxn.cursor()

    try:
        cur.execute('DELETE FROM posts WHERE id = ?', (id,))
        cnxn.commit()
        flash('Post deleted successfully', 'success')

    except pyodbc.Error as e:
        flash(f"Database error: {e}", 'error')

    finally:
        cur.close()
        cnxn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
