from flask import Flask

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

@app.route('/')
def home():
    return 'hello from NFT-Marketplace'

if __name__ == '__main__':
    app.run(debug=True)


