from flask import jsonify, abort
from app import app

@app.route("/forbidden")
def forbidden():
    # Force a 403 error
    abort(403)

@app.route("/error")
def trigger_error():
    # Force a 500 error by raising an exception
    raise RuntimeError("Something went wrong!")

# --- Error Handlers ---

@app.errorhandler(403)
def error_403(e):
    response = {"error : 403": "Forbidden", "message": "You don’t have permission to access this resource."}
    return jsonify(response), 403

# app.register_error_handler(404, handle_not_found)

@app.errorhandler(404)
def error_404(e):
    response = {"error : 404": "Not Found", "message": "The requested resource could not be found."}
    return jsonify(response), 404


@app.errorhandler(500)
def error_500(e):
    # response = {"error": "Internal Server Error", "message": "An unexpected error occurred."}
    response = {"error : 500": "Internal Server Error", "message": "An unexpected error occurred.", "details": str(e)}
    return jsonify(response), 500