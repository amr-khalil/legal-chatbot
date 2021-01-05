# server.py to start the app server
from app import app, db
from app.models import User, Post

'''
Create  User and Posts tables in database
The app.shell_context_processor decorator registers the function as a shell context function
'''
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

# Main function
if __name__=='__main__':
	app.run(debug=True, port=5000)
