from flask import Flask,render_template,request
from datetime import date,datetime

app=Flask(__name__)
@app.route("/")

def home():
    return render_template("index.html")

@app.route("/calculate",methods=['POST'])
def calculate():
    try:
        birthyear=int(request.form.get("birthyear"))
        current_year=datetime.now().year
        if birthyear>current_year or current_year<1900:
            return render_template("index.html",error="Please enter a valid year!")
        else:
            age=current_year-birthyear
            print(age)
            return render_template("index.html",age=age)
    except ValueError:
        return render_template("index.html",error="Please enter a valid year")

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)