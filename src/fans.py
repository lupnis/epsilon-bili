import flask
from flask import Flask, render_template_string
from flask_cors import CORS
from gevent import pywsgi as wsgi
import requests
import json


def webApp():
    app = Flask(__name__)
    app.config['HOST'] = 'localhost'
    app.config['PORT'] = '2333'
    app.config['RESTPLUS_MASK_SWAGGER'] = False
    CORS(app)       
    
    
    
    
    @app.route('/get_fans')
    def get_fans():
        try:
            uid = flask.request.args.get('uid')
            url='https://api.bilibili.com/x/relation/stat?vmid='+str(uid)
            headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2882.18 Safari/537.36'}
            resp=requests.get(url,headers)
            json_resp=json.loads(resp.text)
            return str(json_resp['data']['follower'])
        except:
            return "invalid uid or ip blocked by requested server"
    
    @app.route('/', methods=['GET'])
    def index():
        return "obelisk epsilonBili"
    
    @app.route('/fans_card')
    def fanscard():
        ret_str = """<!DOCTYPE html>
<html>
<head>
    <script src="https://code.jquery.com/jquery-3.0.0.min.js"></script>
    <style>
        @font-face {
            font-family: OdibeeSans-Regular;
            src: url('{{url_for('static',filename='OdibeeSans-Regular.ttf')}}');
        }
        @font-face {
            font-family: LibreBarcode39-Regular;
            src: url('{{url_for('static',filename='LibreBarcode39-Regular.ttf')}}')
        }
        
        .container {
            width: 800pt;
            height: 150pt;
            display: flex;
            align-items: center;
            padding-left:50pt
        }
        
        .notify {
            font-family: 'OdibeeSans-Regular';
            position: relative;
            font-size: 50pt;
            color:#ff6300;
            margin-left: 5pt;
            animation: slide 2s ease-in-out forwards;
            -webkit-text-stroke: 4px rgba(0,0,0,.5);
        }
        
        @keyframes slide {
            0% {
                padding-bottom: 0;
                opacity: 0;
            }
            80% {
                padding-bottom: 50pt;
                opacity: 1;
            }
            100% {
                padding-bottom: 50pt;
                opacity: 0;
            }
        }
        
        #val {
            font-family: 'OdibeeSans-Regular';
            font-size: 80pt;
            color:#000000;
            animation: update 1s ease-in-out forwards;
        }
        
        @keyframes update {
            from {
                margin-left: -40pt;
                opacity: 0;
            }
            to {
                margin-left: 0;
                opacity: 1;
            }
        }
    </style>
</head>

<body>
    <div class="container" id="container">
        <p id="val">-XD-</p>
        <p class="notify" id="plus"></p>
    </div>
    <script type="text/javascript ">
        var uid, refresh_t, fans_count = 0;
        refresh_t = 5000;
        uid = 23328894;
        setInterval(getFans, refresh_t);

        function getFans() {
            var new_val = '-XD-';
            $.ajax({
                url: '/get_fans?uid=' + uid,
                type: 'GET',
                cache: false,
                success: function(data) {
                    console.log(data);
                    new_val = eval(data);
                },
                async: false
            });
            if (new_val != '-XD-' && new_val > fans_count) {
                document.getElementById('container').innerHTML = '<p id="val"></p> <p class="notify" id="plus"></p>';
               
                document.getElementById('plus').innerText = '+' + (new_val - fans_count);
            }
             document.getElementById('val').innerText = new_val;
            fans_count = new_val;
        }
    </script>
</body>

</html>"""
        return render_template_string(ret_str)
    
    return app


if __name__ == "__main__":
    appli =  webApp()
    print("running service at http://127.0.0.1:2333")
    print("for fans card, use http://127.0.0.1:2333/fans_card")
    server = wsgi.WSGIServer(('0.0.0.0', 2333), appli)
    server.serve_forever()
    


