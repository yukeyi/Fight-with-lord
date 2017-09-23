import json, zlib
from flask import Flask, render_template, url_for, request, redirect, session, jsonify, abort, send_file, make_response

#import game as gameApp
#import ai as aiApp
#import random

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
	info = json.loads(request.form['data'])
	for i in range(3):
		if i != info['turn']:
			info['handCard'][i] = [0] * 15
			break
	card = []
	#card = random.choice(gameApp.generate(info))
	#card = aiApp.getNextMove(info, info['turn'], 'model/iter2')
	#print(info, card)
	return json.dumps(card)


app.secret_key = 'A0Zr98a/3yX R~akj!jmk]Lzx/,?RT'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=23333)
