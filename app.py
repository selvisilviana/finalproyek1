from flask import Flask, render_template, request

#import package untuk safebot
from process import preparation, generate_response

# Download nltk
preparation()

# Start Chatbot
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_input = str(request.args.get('msg'))
    result = generate_response(user_input)
    return result

if __name__ == "__main__":
    app.run(debug=True)
