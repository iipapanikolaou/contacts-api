from flask import Flask

app = Flask(__name__)

contactsList = [
    {
        id:'1',
        name:'jhon'
        number:'6985698458'
    },
    {
        id:'2',
        name:'adam'
        number:'6985688458'
    },
    {
        id:'3',
        name:'peter'
        number:'6934698458'
    },
    {
        id:'4',
        name:'jason'
        number:'6968698458'
    },
]

@app.route('/')
def homepage():
    return '<h1>Hello there!</h1>'

@app.get('/contacts')
def list_contacts:

    