# from flask_app.controllers import users
from flask_app import app
from flask_app.controllers import users, pies

# Ensure file is run directly and not from different
# module, and run localhost on port 5001 for mac
if __name__ == "__main__":
    app.run(debug=True)