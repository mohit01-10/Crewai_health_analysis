from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from utils.email_utils import send_email
from utils.pdf_utils import extract_text_from_pdf  # Importing pdf utility
import os

# Import agent and task setup from the agents folder
from agents.agents import create_tasks

app = Flask(__name__)
app.config.from_object('config.Config')
jwt = JWTManager(app)
os.environ['LITELLM_LOG'] = 'DEBUG'

@app.route('/')
def index():
    return """
    <h1>Welcome to the Health Analysis API</h1>
    <p>This API allows you to analyze health data from blood test reports and provide health recommendations. Below are the instructions for using this API via Postman:</p>

    <h2>Endpoints:</h2>
    <ul>
        <li><strong>/login</strong> (POST): Authenticate using username and password.<br>
            <strong>Steps to test in Postman:</strong>
            <ol>
                <li>Open Postman and create a new <strong>POST</strong> request.</li>
                <li>Set the URL to <code>http://localhost:5000/login</code>.</li>
                <li>In the <strong>Body</strong> tab, choose <strong>raw</strong> and select <strong>JSON</strong> as the format.</li>
                <li>Enter the following JSON data in the body:
                <pre>{
    "username": "user",
    "password": "pass"
}</pre>
                </li>
                <li>Click <strong>Send</strong> to receive a JWT token.</li>
            </ol>
            <strong>Response:</strong> A JSON response with the access token.
        </li>
        
        <li><strong>/analyze</strong> (POST): Upload a blood test PDF and receive health recommendations via email.<br>
            <strong>Steps to test in Postman:</strong>
            <ol>
                <li>Open Postman and create a new <strong>POST</strong> request.</li>
                <li>Set the URL to <code>http://localhost:5000/analyze</code>.</li>
                <li>In the <strong>Authorization</strong> tab, select <strong>Bearer Token</strong> and paste the JWT token from the /login request.</li>
                <li>In the <strong>Body</strong> tab, choose <strong>form-data</strong>.</li>
                <li>Add the following fields:
                    <ul>
                        <li><strong>Key</strong>: <code>pdf</code> | <strong>Type</strong>: <code>File</code> | <strong>Value</strong>: Select the PDF file to upload.</li>
                        <li><strong>Key</strong>: <code>email</code> | <strong>Type</strong>: <code>Text</code> | <strong>Value</strong>: Enter your email address.</li>
                    </ul>
                </li>
                <li>Click <strong>Send</strong> to receive the analysis and recommendations.</li>
            </ol>
            <strong>Response:</strong> A JSON response with the analysis, health recommendations, and relevant health articles.
        </li>
    </ul>

    <h2>Additional Information:</h2>
    <ul>
        <li>Ensure the server is running by executing <code>python app.py</code>.</li>
        <li>You need valid credentials (username: <strong>user</strong>, password: <strong>pass</strong>) to log in and obtain the access token.</li>
        <li>Install all dependencies as listed in the requirements file before running the API.</li>
        <li>Create a .env file with all sercret keys as mentioned in ReadME.md file.</li>
        <li>Check your Spam folder for email.</li>
    </ul>

    <p>Happy health analysis! Use Postman to interact with this API quickly and easily.</p>
    """


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'user' or password != 'pass':
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    if 'pdf' not in request.files or 'email' not in request.form:
        return jsonify({"msg": "Missing file or email"}), 400
    
    pdf_file = request.files['pdf']
    user_email = request.form['email']
    
    # Save the uploaded file temporarily
    pdf_path = os.path.join('/tmp', pdf_file.filename)
    pdf_file.save(pdf_path)
    
    # Extract text from the PDF using the utility function
    raw_text = extract_text_from_pdf(pdf_path)
    
    # Create the tasks and run the crew
    crew = create_tasks(raw_text)
    inputs = {"input": raw_text}
    print(raw_text)
    results = crew.kickoff(inputs=inputs)

    # Assume results contain analysis and relevant data
    analysis = results['analysis']
    recommendations = results['recommendations']
    articles = results['articles']

    #analysis = "dummy text"
    #recommendations = "dummy text"
    #articles = "dummy text"
    
    # Send email with the results
    send_email(user_email, analysis, recommendations, articles)
    
    return jsonify({
        "analysis": analysis,
        "recommendations": recommendations,
        "articles": articles
    })

if __name__ == '__main__':
    app.run(debug=True)
