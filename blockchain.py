# Python module imports
import datetime as dt
from flask import Flask, request, render_template, jsonify

# Importing local functions
from genesis import create_blockchain
from newBlock import add_block
from getBlock import find_records, get_all_attendance_records
from checkChain import check_integrity, get_blockchain_stats
from persistence import save_blockchain, load_blockchain, export_blockchain_csv
from analytics import get_attendance_analytics, generate_attendance_report, export_analytics

# Flask declarations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'blockendance-secret-key-2018'

# Add cache control headers
@app.after_request
def after_request(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

# Initializing blockchain with the genesis block
# Try to load existing blockchain first
loaded_blockchain, load_message = load_blockchain()
if loaded_blockchain:
    blockchain = loaded_blockchain
    print(f"Loaded existing blockchain: {load_message}")
else:
    blockchain = create_blockchain()
    print(f"Created new blockchain: {load_message}")
    # Save the new blockchain
    save_blockchain(blockchain)

print(f"Blockchain initialized with genesis block: {blockchain[0]}")

# Default Landing page of the app
@app.route('/',  methods = ['GET'])
def index():
    return render_template("index.html")

# Get Form input and decide what is to be done with it
@app.route('/', methods = ['POST'])
def parse_request():
    try:
        # Step 1: Teacher enters name
        if request.form.get("name"):
            teacher_name = request.form.get("name").strip()
            if not teacher_name:
                return render_template("index.html", error="Please enter a valid name")

            return render_template("class.html",
                                    name = teacher_name,
                                    date = dt.date.today())

        # Step 2: Teacher enters class details
        elif request.form.get("number"):
            teacher_name = request.form.get("teacher_name", "").strip()
            course = request.form.get("course", "").strip()
            year = request.form.get("year", "").strip()
            number = request.form.get("number", "0")

            # Validate inputs
            if not all([teacher_name, course, year]):
                return render_template("class.html",
                                     error="Please fill all required fields",
                                     name=teacher_name,
                                     date=dt.date.today())

            try:
                student_count = int(number)
                if student_count <= 0:
                    raise ValueError("Invalid student count")
            except ValueError:
                return render_template("class.html",
                                     error="Please enter a valid number of students",
                                     name=teacher_name,
                                     date=dt.date.today())

            return render_template("attendance.html",
                                    name = teacher_name,
                                    course = course,
                                    year = year,
                                    number = student_count,
                                    date = str(dt.date.today()))

        # Step 3: Teacher submits attendance
        elif request.form.get("roll_no1"):
            # Extract form data
            form_data = [
                request.form.get("teacher_name", "").strip(),
                request.form.get("date", "").strip(),
                request.form.get("course", "").strip(),
                request.form.get("year", "").strip()
            ]

            # Validate required data
            if not all(form_data):
                return render_template("result.html",
                                     result="Error: Missing required information")

            result = add_block(request.form, form_data, blockchain)

            # Auto-save blockchain after adding new block
            if "added" in result:
                save_success, save_msg = save_blockchain(blockchain)
                if save_success:
                    result += f" Blockchain automatically saved."
                else:
                    result += f" Warning: Failed to save blockchain - {save_msg}"

            return render_template("result.html", result=result)

        else:
            return render_template("index.html", error="Invalid form submission")

    except Exception as e:
        return render_template("index.html", error=f"An error occurred: {str(e)}")

# Show page to get information for fetching records
@app.route('/view.html',  methods = ['GET'])
def view():
    return render_template("class.html", view_mode=True)

# Process form input for fetching records from the blockchain
@app.route('/view.html',  methods = ['POST'])
def show_records():
    try:
        # Validate form inputs
        name = request.form.get("name", "").strip()
        course = request.form.get("course", "").strip()
        year = request.form.get("year", "").strip()
        date = request.form.get("date", "").strip()
        number = request.form.get("number", "0")

        if not all([name, course, year, date]):
            return render_template("class.html",
                                 view_mode=True,
                                 error="Please fill all required fields")

        try:
            student_count = int(number)
            if student_count <= 0:
                raise ValueError("Invalid student count")
        except ValueError:
            return render_template("class.html",
                                 view_mode=True,
                                 error="Please enter a valid number of students")

        # Search for records
        attendance_data = find_records(request.form, blockchain)

        if attendance_data == -1:
            return render_template("view.html",
                                name = name,
                                course = course,
                                year = year,
                                date = date,
                                number = student_count,
                                status = [],
                                error = "No records found for the specified criteria")

        return render_template("view.html",
                                name = name,
                                course = course,
                                year = year,
                                date = date,
                                number = student_count,
                                status = attendance_data,
                                success = f"Found attendance record with {len(attendance_data)} students present")

    except Exception as e:
        return render_template("class.html",
                             view_mode=True,
                             error=f"An error occurred: {str(e)}")

# Show page with result of checking blockchain integrity
@app.route('/result.html',  methods = ['GET'])
def check():
    try:
        integrity_result = check_integrity(blockchain)
        stats = get_blockchain_stats(blockchain)
        return render_template("result.html",
                             result=integrity_result,
                             stats=stats)
    except Exception as e:
        return render_template("result.html",
                             result=f"Error checking blockchain: {str(e)}")

# API endpoint to get blockchain statistics
@app.route('/api/stats', methods=['GET'])
def api_stats():
    try:
        stats = get_blockchain_stats(blockchain)
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to get all attendance records
@app.route('/api/records', methods=['GET'])
def api_records():
    try:
        records = get_all_attendance_records(blockchain)
        return jsonify({"records": records, "count": len(records)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to get analytics
@app.route('/api/analytics', methods=['GET'])
def api_analytics():
    try:
        analytics = get_attendance_analytics(blockchain)
        return jsonify(analytics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to export data
@app.route('/api/export/<format>', methods=['GET'])
def api_export(format):
    try:
        if format == 'csv':
            success, message = export_blockchain_csv(blockchain)
            return jsonify({"success": success, "message": message})
        elif format == 'analytics':
            success, message = export_analytics(blockchain)
            return jsonify({"success": success, "message": message})
        elif format == 'json':
            success, message = save_blockchain(blockchain)
            return jsonify({"success": success, "message": message})
        else:
            return jsonify({"error": "Invalid export format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to get attendance report
@app.route('/api/report', methods=['GET'])
def api_report():
    try:
        format_type = request.args.get('format', 'json')
        if format_type == 'text':
            report = generate_attendance_report(blockchain, format='text')
            return report, 200, {'Content-Type': 'text/plain'}
        else:
            report = generate_attendance_report(blockchain, format='json')
            return report, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to load blockchain from file
@app.route('/api/load', methods=['POST'])
def api_load():
    try:
        global blockchain
        loaded_blockchain, message = load_blockchain()
        if loaded_blockchain:
            blockchain = loaded_blockchain
            return jsonify({"success": True, "message": message, "blocks": len(blockchain)})
        else:
            return jsonify({"success": False, "message": message}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the flask app when program is executed
if __name__ == "__main__":
    print("Starting Blockendance - Blockchain-based Attendance System")
    print(f"Blockchain initialized with {len(blockchain)} blocks")
    print("Access the application at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
