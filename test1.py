from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_health_conditions():
    # Retrieve a list of health conditions from your database or an external API
    health_conditions = ["Headache", "Fever", "Cough", "Sore throat"]
    return health_conditions

def get_severity_levels():
    # Retrieve a list of severity levels from your database or an external API
    severity_levels = ["Mild", "Moderate", "Severe"]
    return severity_levels

def handle_user_input(user_input):
    # Process the user input and return a response
    # You can implement your business logic here
    return "You selected: " + user_input

@app.route("/", methods=["GET", "POST"])
def helpdesk():
    if request.method == "POST":
        selected_condition = request.form.get("condition")
        selected_severity = request.form.get("severity")

        # Pass user input to the ChatGPT API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpdesk assistant."},
                    {"role": "user", "content": selected_condition},
                    {"role": "user", "content": selected_severity},
                ]
            }
        )

        if response.status_code == 200:
            output = response.json()["choices"][0]["message"]["content"]
            return render_template("index.html", output=output)
        else:
            error_message = "Error: " + response.text
            return render_template("index.html", error=error_message)

    else:
        health_conditions = get_health_conditions()
        severity_levels = get_severity_levels()
        return render_template("index.html", conditions=health_conditions, severity_levels=severity_levels)

if __name__ == "__main__":
    app.run()
