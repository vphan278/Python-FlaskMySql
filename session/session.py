from flask import Flask, request, redirect, session, flash, render_template
app = Flask(__name__)
#app.secret_key = "keep it safe"

app.secret_key = "c0de70e626ec29d18b824fb84a53954edcb212b41a6ab0bfe070430d73a24d58"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users", methods = ["POST"])
def create_user():
    
    session["first_name"] = request.form["first_name"]
    session["last_name"] = request.form["last_name"]
    session["email"] = request.form["email"]

    return redirect("/show")

@app.route("/show")
def show_user():
    return render_template("show.html", name_on_template = session["first_name"], name_on_template2 = session["last_name"], email_on_template =session["email"])

@app.route("/reset_session")
def reset_session():
    #session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)