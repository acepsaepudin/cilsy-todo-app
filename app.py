from flask import Flask, render_template, request, jsonify, redirect, url_for
import boto3
import uuid
import json

app = Flask(__name__)

# Load secrets from AWS Secrets Manager
def get_secret(secret_name, region_name="us-east-1"):
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

# Load DynamoDB and Secrets Manager
region = "ap-southeast-1"
secrets = get_secret("prod/todo-app")
dynamodb = boto3.resource("dynamodb", region_name=region)
table = dynamodb.Table(secrets["dynamodb_table"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/todos", methods=["GET", "POST", "DELETE"])
def todos():
    if request.method == "GET":
        response = table.scan()
        return jsonify(response["Items"])

    elif request.method == "POST":
        data = request.json
        todo_id = str(uuid.uuid4())
        item = {"id": todo_id, "title": data["title"]}
        table.put_item(Item=item)
        return jsonify({"message": "Todo added!", "id": todo_id}), 201

    elif request.method == "DELETE":
        todo_id = request.json.get("id")
        table.delete_item(Key={"id": todo_id})
        return jsonify({"message": "Todo deleted!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

