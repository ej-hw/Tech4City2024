import model
import random
from database import save_analysis, get_analyses, delete_analysis
from flask import Flask, request, Response
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/api/docs"
API_URL = "/swagger.json"

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
)

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui_blueprint)


@app.post("/api/analyze")
def analyze():
    data = request.get_json()
    topic = data.get('topic', 'something')
    seed = data.get('seed', '')
    message = data.get('message')

    if not message:
        return 'Message is required', 400

    results = model.analyze(message)
    reply = None

    if results["should_reply"]:
        reply = model.get_completion(topic, seed, message)

    analysis = save_analysis(
        topic=topic,
        seed=seed,
        message=message,
        results=results,
        reply=reply
    )

    return {
        "id": analysis.id,
        'topic': analysis.topic,
        'seed': analysis.seed,
        'message': analysis.message,
        "results": results,
        "reply": reply,
        "created_at": analysis.created_at
    }


@app.get('/api/seed')
def seed():
    topic = random.choice(["science", "maths", "music", "sports"])
    return {"topic": topic, "text": model.get_seed(topic)}


@app.get("/api/results")
def results():
    return get_analyses()


@app.delete("/api/results/<int:id>")
def delete_result(id):
    delete_analysis(id)
    return Response()


@app.route('/', defaults={'path': 'index.html'})
@app.route("/<path:path>")
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
