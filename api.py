import flask
from flask import request, jsonify
import psycopg2
from config import config

app = flask.Flask(__name__)
app.config["DEBUG"] = True

conn =None
try:
    params = config()
    conn = psycopg2.connect(**params)

    @app.route('/api/v1/resources/countries/all', methods=['GET'])
    def api_all():
        
        cur = conn.cursor()
        cur.execute('SELECT * FROM country;')
        record = cur.fetchall()
        return jsonify(record)

    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404</h1><p>The resource could not be found.</p>", 404

    @app.route('/api/v1/resources/countries', methods=['GET'])
    def api_filter():
        query_parameters = request.args

        name = query_parameters.get('name')
        capital = query_parameters.get('capital')
        country_code = query_parameters.get('country_code')

        query = "SELECT * FROM country WHERE"
        to_filter = []

        if name:
            query += ' name=%s AND'
            to_filter.append(name)
        if capital:
            query += ' capital=%s AND'
            to_filter.append(capital)
        if country_code:
            query += ' country_code=%s AND'
            to_filter.append(country_code)
        if not (name or capital or country_code):
            return page_not_found(404)

        query = query[:-4] + ';'
        
        cur = conn.cursor()
        results = cur.execute(query, to_filter)
        record = cur.fetchall()

        return jsonify(record)

except (Exception, psycopg2.DatabaseError) as error:
        print("Error is :",error)


if __name__ == "__main__":
    app.run()
