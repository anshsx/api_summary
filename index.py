from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/ai_query', methods=['POST'])
def ai_query():
    """API endpoint to process a query and related content."""
    data = request.get_json()
    if not data or 'query' not in data or 'content' not in data:
        return jsonify({"error": "Invalid input JSON. 'query' and 'content' keys are required."}), 400

    query = data['query']
    content = data['content']

    # Prepare payload for AI API
    ai_api_url = "https://text.pollinations.ai/"
    payload = {
        "messages": [{"role": "user", "content": f"Fetch each and every useful information for the query : {query} from this data: {content} and write in a paragraph. Remember to fetch each basic to advanced information on the query"}],
        "model": "openai",
        "seed": "50",
        "jsonMode": True
    }

    try:
        response = requests.post(ai_api_url, json=payload, timeout=10)
        response.raise_for_status()
        ai_response = response.json()
        return jsonify(ai_response)
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to process AI query: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
