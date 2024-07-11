from flask import Flask  
  
app = Flask(__name__)  

# app.route(rule, options)
@app.route('/hello')

def home():  
    return "hello welcome to the website";  

if __name__ =='__main__':
    # app.run(host, port, debug, options)  
    app.run(debug = True)