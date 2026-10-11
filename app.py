from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculator():
    # Set default values for when the page first loads
    result = None
    system_status = None
    inputs = {
        "mass_flow": 5.0,
        "cp": 4.18,
        "t_in": 50.0,
        "t_out": 75.0,
        "boiling_point": 100.0
    }

    if request.method == "POST":
        try:
            # Retrieve data entered by the user in the HTML form
            inputs["mass_flow"] = float(request.form.get("mass_flow", 0))
            inputs["cp"] = float(request.form.get("cp", 0))
            inputs["t_in"] = float(request.form.get("t_in", 0))
            inputs["t_out"] = float(request.form.get("t_out", 0))
            inputs["boiling_point"] = float(request.form.get("boiling_point", 0))

            # Core Spreadsheet Equation: Q = m * Cp * (Tout - Tin)
            heat_duty = inputs["mass_flow"] * inputs["cp"] * (inputs["t_out"] - inputs["t_in"])
            result = round(heat_duty, 1)

            # Phase Safety Automation Logic
            if inputs["t_out"] < inputs["boiling_point"]:
                system_status = "Safe Liquid Phase (Operating safely below boiling threshold)"
            else:
                system_status = "CRITICAL WARNING: Phase Change / Vaporization Risk"
                
        except ValueError:
            system_status = "Error: Please enter valid numerical values."

    return render_template("index.html", inputs=inputs, result=result, system_status=system_status)

if __name__ == "__main__":
    app.run(debug=True)
