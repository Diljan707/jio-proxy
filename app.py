from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Jio ਦਾ ਅਸਲੀ ਲਾਇਸੈਂਸ ਸਰਵਰ
JIO_LICENSE_URL = "https://jiotv.jio.com/license/"

@app.route('/license/<ch_id>', methods=['GET', 'POST'])
def proxy_license(ch_id):
    headers = {
        "User-Agent": "StreamFlex(StreamFlex; JioSTB) JioTVPlus-AndroidTv"
    }
    
    # ਜੇ ਕੋਈ ਕੁਕੀ ਜਾਂ ਟੋਕਨ ਹੋਵੇ ਤਾਂ ਉਹ ਵੀ ਅੱਗੇ ਭੇਜ ਦੇਵਾਂਗੇ
    if 'cookie' in request.headers:
        headers['cookie'] = request.headers.get('cookie')

    try:
        # Jio ਸਰਵਰ ਨੂੰ ਰਿਕਵੈਸਟ ਭੇਜਣਾ
        resp = requests.post(
            f"{JIO_LICENSE_URL}{ch_id}",
            data=request.get_data(),
            headers=headers,
            timeout=10
        )
        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('content-type'))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.app.run(host='0.0.0.0', port=5000)
