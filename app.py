from flask import Flask, request, Response
import requests

app = Flask(__name__)

JIO_LICENSE_URL = "https://jiotv.jio.com/license/"

@app.route('/license/<ch_id>', methods=['GET', 'POST', 'OPTIONS'])
def proxy_license(ch_id):
    if request.method == 'OPTIONS':
        return '', 200

    headers = {
        "User-Agent": "StreamFlex(StreamFlex; JioSTB) JioTVPlus-AndroidTv",
        "Accept": "*/*"
    }
    
    # ਪਲੇਅਰ ਵੱਲੋਂ ਆਈਆਂ ਕੁਕੀਜ਼ ਜਾਂ ਹੈਡਰਸ ਨੂੰ ਅੱਗੇ ਪਾਸ ਕਰਨਾ
    if 'Cookie' in request.headers:
        headers['Cookie'] = request.headers.get('Cookie')
    elif 'cookie' in request.headers:
        headers['Cookie'] = request.headers.get('cookie')

    try:
        # Jio ਸਰਵਰ ਨੂੰ ਰਿਕਵੈਸਟ ਭੇਜਣਾ
        resp = requests.post(
            f"{JIO_LICENSE_URL}{ch_id}",
            data=request.get_data(),
            headers=headers,
            timeout=15
        )
        return Response(
            resp.content, 
            status=resp.status_code, 
            content_type=resp.headers.get('content-type', 'application/octet-stream')
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
