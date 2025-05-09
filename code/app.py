from flask import Flask, request, render_template, session, redirect, url_for
import pandas as pd
import joblib

app = Flask(__name__)
app.secret_key = "PROJECTsecrete"  # Required for session management

# Load the trained model (make sure this path is correct)
model = joblib.load("best_churn_model.pkl")

@app.route("/", methods=["GET"])
def home():
    # Home page with description of the app and options
    return render_template("home.html")

@app.route("/calculate", methods=["GET", "POST"])
def calculate_features():
    if request.method == "POST":
        # Get input values from the form
        monthly_charges = float(request.form["monthly_charges"])
        tenure = int(request.form["tenure"])
        tech_support = request.form["tech_support"]
        contract = request.form["contract"]
        action = request.form.get("action")  # Which button was clicked

        # Step 1: Calculate the engineered features
        engagement_score = 0.4 * monthly_charges + 0.3 * tenure + 0.3 * (1 if tech_support == 'Yes' else 0)
        interaction_frequency = 1 if tech_support == 'Yes' else 0
        long_term_contract = 0 if contract == 'Month-to-month' else 1

        # Step 2: Store calculated features in the session
        session['features'] = {
            'engagement_score': engagement_score,
            'interaction_frequency': interaction_frequency,
            'long_term_contract': long_term_contract
        }

        # Step 3: If the user clicked 'Predict Churn', make the prediction
        if action == "Predict Churn":
            input_data = pd.DataFrame({
                "EngagementScore": [engagement_score],
                "CustomerInteractionFrequency": [interaction_frequency],
                "LongTermContractStability": [long_term_contract]
            })

            # Predict churn and probability
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1]

            return render_template(
                "calculate.html",
                engagement_score=round(engagement_score, 2),
                interaction_frequency=interaction_frequency,
                long_term_contract=long_term_contract,
                result="Customer is likely to churn" if prediction == 1 else "Customer is not likely to churn",
                prob=round(probability * 100, 2)
            )

        # If action is to just calculate features
        return render_template(
            "calculate.html",
            engagement_score=round(engagement_score, 2),
            interaction_frequency=interaction_frequency,
            long_term_contract=long_term_contract,
            result=None,
            prob=None
        )

    # Default page load for '/calculate'
    return render_template("calculate.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)