from flask import Flask 
app = Flask(__name__)

@app.route('/main')
def main():
	# if user subscribed 2 some people, show them those pages 1st
	# if user subscribed 2 know pages, show him trending pages
	return render_template('starters.html')

if __name__=='__main__':
	app.run(debug=True)