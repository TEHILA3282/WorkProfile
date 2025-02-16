from typing import List
from flask import Flask, render_template, request, Response
from dbcontext import db_data, db_delete, db_add, health_check
from person import Person

app = Flask(__name__)

@app.route("/")
def main():
    data = db_data()
    return render_template("index.html.jinja", host_name=host_name,
                         db_host=db_host, data=data, backend=backend)

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id: int):
    return db_delete(id)

@app.route("/add", methods=["PUT"])
def add():
    body = request.json
    if body is not None:
        app.logger.info("Request to add person with body: %s", body)
        person = Person(0, body["firstName"], body["lastName"],
                       body["age"], body["address"], body["workplace"])
        return db_add(person)
    app.logger.error("Request body is empty")
    return Response(status=404)

import psutil
from flask import Flask, render_template, request, Response, jsonify

@app.route("/health")
def health():
    try:
        
        app_status = "Healthy"
        http_status = 200

        
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent 

        
        if memory_usage > 80:
            app_status = "Unhealthy - High Memory Usage"
            http_status = 503

     
        health_data = {
            "application": app_status,
            "memory_usage_percent": memory_usage,
        }

        return jsonify(health_data), http_status

    except Exception as e:
        app.logger.error(f"Health check failed: {e}")
        return jsonify({"application": "Unhealthy", "error": str(e)}), 503

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

