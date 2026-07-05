from pathlib import Path

from flask import Flask, jsonify, request

from services.data_service import DataService, OllamaModelError


ROOT = Path(__file__).resolve().parents[1]


def create_app() -> Flask:
    app = Flask(__name__)
    service = DataService()

    @app.get("/")
    def index():
        return jsonify({"message": "Fake data generator API is running"})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/database")
    def database_records():
        try:
            records = service.get_database_records()
        except FileNotFoundError:
            return jsonify({"error": "Database file not found"}), 404
        except Exception as exc:
            return jsonify({"error": f"Database query failed: {exc}"}), 500

        return jsonify({"database": "fakedata.db", "records": records})

    @app.route("/generate", methods=["GET", "POST"])
    def generate():
        payload = request.get_json(silent=True) or {}
        if request.method == "GET":
            payload = request.args.to_dict(flat=True)

        provider = payload.get("provider", "faker")
        count = payload.get("count", 5)
        model = payload.get("model", "phi4:latest")
        base_url = payload.get("base_url", "http://localhost:11434")

        if isinstance(count, str):
            try:
                count = int(count)
            except ValueError:
                return jsonify({"error": "count must be an integer"}), 400

        if not isinstance(count, int) or count < 1:
            return jsonify({"error": "count must be a positive integer"}), 400

        try:
            payload = service.generate_records(provider=provider, count=count, model=model, base_url=base_url)
        except OllamaModelError as exc:
            return jsonify({"error": str(exc)}), 500
        except ImportError as exc:
            return jsonify({"error": str(exc)}), 500
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception as exc:
            return jsonify({"error": f"Generation failed: {exc}"}), 500

        return jsonify(payload)

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify({"error": "Method not allowed"}), 405

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
