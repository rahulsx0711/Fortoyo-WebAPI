from flask import Flask
from flask_restful import Resource, Api
import os
from urllib import parse
import psycopg2
import json

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
app = Flask(__name__)
api = Api(app)

class VulnerabilityData(Resource):
    def get(self):
        cur = conn.cursor()
        cur.execute("select * from vulninfo")
        columns = ['title','summary','createdate']
        # result = {'data': [dict(zip(columns,row)) for row in cur.fetchall()]}
        result =[dict(zip(columns, row)) for row in cur.fetchall()]
        return {'body':result[0]}

api.add_resource(VulnerabilityData, '/api/vuln')

if __name__ == '__main__':
    app.run(debug=True)
