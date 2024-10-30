from flask import Flask, render_template, request, url_for, jsonify
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os
app = Flask(__name__)

def generate_plots(N, mu, sigma2, S):

    plot1_path = "./static/plot1.png"
    plot2_path = "./static/plot2.png"
    
    # Delete existing plot images if they exist
    if os.path.exists(plot1_path):
        print("deleted!")
        os.remove(plot1_path)
    if os.path.exists(plot2_path):
        os.remove(plot2_path)


    X = np.random.rand(N)
    Y = mu + np.random.normal(0, np.sqrt(sigma2), N)

    model = LinearRegression()
    model.fit(X.reshape(-1, 1), Y)
    slope = model.coef_[0]
    intercept = model.intercept_

    plt.figure(figsize=(8, 6))
    plt.scatter(X, Y, color='blue', label='Data')
    plt.plot(X, model.predict(X.reshape(-1, 1)), color='red', label=f'Y = {slope:.2f} * X + {intercept:.2f}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Scatter Plot with Regression Line')
    plt.legend()
    plot1_path = "static/plot1.png"
    plt.savefig(plot1_path)
    plt.close()

    slopes = []
    intercepts = []
    for _ in range(S):
        X_sim = np.random.rand(N)
        Y_sim = mu + np.random.normal(0, np.sqrt(sigma2), N)
        sim_model = LinearRegression()
        sim_model.fit(X_sim.reshape(-1, 1), Y_sim)
        slopes.append(sim_model.coef_[0])
        intercepts.append(sim_model.intercept_)

    plt.figure(figsize=(10, 5))
    plt.hist(slopes, bins=20, alpha=0.5, color="blue", label="Slopes")
    plt.hist(intercepts, bins=20, alpha=0.5, color="orange", label="Intercepts")
    plt.axvline(slope, color="blue", linestyle="--", linewidth=1, label=f"Slope: {slope:.2f}")
    plt.axvline(intercept, color="orange", linestyle="--", linewidth=1, label=f"Intercept: {intercept:.2f}")
    plt.title("Histogram of Slopes and Intercepts")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plot2_path = "static/plot2.png"
    plt.savefig(plot2_path)
    plt.close()

    slope_more_extreme = sum(s > slope for s in slopes) / S
    intercept_more_extreme = sum(i < intercept for i in intercepts) / S

    return plot1_path, plot2_path, slope_more_extreme, intercept_more_extreme

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.headers.get("X-Requested-With"))
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            N = int(request.form["N"])
            mu = float(request.form["mu"])
            sigma2 = float(request.form["sigma2"])
            S = int(request.form["S"])

            plot1, plot2, slope_extreme, intercept_extreme = generate_plots(N, mu, sigma2, S)

            response_data = {
                "plot1_url": url_for("static", filename="plot1.png"),
                "plot2_url": url_for("static", filename="plot2.png"),
                "slope_extreme": slope_extreme,
                "intercept_extreme": intercept_extreme
            }
            print("used jsonify")
            return jsonify(response_data)
        else:
            print("used render template")
            return render_template("index.html")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)