from flask import Flask, jsonify
from vector_store import VectorStore

app = Flask(__name__)
vs = VectorStore()
vs.load()

@app.route("/")
def home():
    return jsonify(vs.list_datasets())

@app.route("/datasets")
def list_datasets():
    return jsonify(vs.list_datasets())


@app.route("/health")
def health():
    return {"status": "GhostTrace Vector Store Active"}

@app.route("/datasets")
def datasets():
    return jsonify(...)


@app.route("/stats")
def stats():
    return jsonify({
        "total_vectors": vs.index.ntotal,
        "embedding_dim": vs.index.d,
        "index_type": type(vs.index).__name__
    })


if __name__ == "__main__":
    app.run(debug=True)
