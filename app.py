from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_bootstrap import Bootstrap




# app = Flask(__name__,template_folder='./templates')  #应用实例
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET'])
def index():
    response = {
        'msg': 'Connection !'
    }
    return jsonify(response)    #（jsonify返回一个json格式的数据）
    # return 'connection'