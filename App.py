from flask import Flask,url_for,flash,render_template,request,redirect

app = Flask(__name__)
'''app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'SecretoAcero11!'
app.config['MYSQL_DB'] = 'cloudFlaskCherryTreeDB'
mysql = MySQL(app)
'''

@app.route('/')

def Index():
    '''cur = mysql.connection.cursor()
    mysql.connection.commit()

    cur.execute('SELECT * FROM Results')
    data = cur.fetchall()
    '''
    return render_template('index.html')
'''
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
       technology = request.form['technology']
       post = request.form['post']
       cur = mysql.connection.cursor()
       cur.execute('INSERT INTO posts (technology,post) VALUES(%s,%s)',
       (technology,post))
       mysql.connection.commit()
       flash('Post added successfully')
       return redirect(url_for('Index'))

@app.route('/edit/<id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        technology = request.form['technology']
        post = request.form['post']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts 
            SET fullname = %s,
                technology = %s,
                post = %s
            WHERE id = %s
        """, (technology,post,id))
        mysql.connection.commit()
        flash('Post Updated Succesfully')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Post deleted successfully')
    return redirect(url_for('Index'))
'''

if __name__ == '__main__':
    app.run(port=3000, debug=True)

