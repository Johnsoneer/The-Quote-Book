from app import app, db
from app.models import users,phrases, quotes,people_quoted

@app.shell_context_processor
def make_shell_context():
    return {'db':db,'users':users, 'phrases':phrases,'quotes':quotes,'people_quoted':people_quoted}
