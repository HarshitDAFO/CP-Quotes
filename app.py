import os
import pandas as pd
from flask import Flask, render_template, request, send_file
from datetime import datetime
from generate_pdf import create_final_pdf
from google_sheet import save_to_google_sheet

app = Flask(__name__)

# Load premium data once
premium_df = pd.read_excel('Premium CP.xlsx')

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    rm_name = request.form['rm_name']
    doctor_name = request.form['doctor_name']
    specialization = request.form['specialization']
    sum_assured = request.form['sum_assured']

    # Filter for this specialization & sum assured
    df_filtered = premium_df[
        (premium_df['Specialization'] == specialization) &
        (premium_df['Sum Assured'] == sum_assured)
    ]

    if df_filtered.empty or len(df_filtered) < 2:
        return "Premium data not found for selected inputs.", 400

    # Get PI row
    pi_row = df_filtered[df_filtered['Plan Type'] == 'PI'].iloc[0]
    pi_1 = (int(pi_row['1Y Amount']), float(pi_row['1Y Saving']))
    pi_2 = (int(pi_row['2Y Amount']), float(pi_row['2Y Saving']))
    pi_3 = (int(pi_row['3Y Amount']), float(pi_row['3Y Saving']))

    # Get Protect+ row
    pp_row = df_filtered[df_filtered['Plan Type'] == 'Protect+'].iloc[0]
    pp_1 = (int(pp_row['1Y Amount']), float(pp_row['1Y Saving']))
    pp_2 = (int(pp_row['2Y Amount']), float(pp_row['2Y Saving']))
    pp_3 = (int(pp_row['3Y Amount']), float(pp_row['3Y Saving']))

    # Create PDF
    output_path = create_final_pdf(
        doctor_name, specialization, sum_assured,
        pi_1, pi_2, pi_3,
        pp_1, pp_2, pp_3
    )

    # Save to Google Sheets
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_to_google_sheet([
        timestamp, rm_name, doctor_name, specialization, sum_assured,
        pi_1[0], pi_2[0], pi_3[0],
        pp_1[0], pp_2[0], pp_3[0]
    ])

    return send_file(output_path, as_attachment=True, download_name=f"Dr.{doctor_name}.pdf")

if __name__ == "__main__":
    app.run(debug=True)
