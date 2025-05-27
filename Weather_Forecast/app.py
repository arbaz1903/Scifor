import json
import requests
from flask import Flask, request, render_template, send_file
from fpdf import FPDF
import io

API_KEY = "5d7aaac434msh33cec5f36478cf3p13133djsn35670054324a"
API_HOST = "weatherapi-com.p.rapidapi.com"
API_URL = "https://weatherapi-com.p.rapidapi.com/current.json"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_weather', methods=['POST'])
def predict_weather():
    if request.method == 'POST':
        q = request.form['location']
        querystring = {"q": q}
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": API_HOST
        }
        try:
            response = requests.get(API_URL, headers=headers, params=querystring)
            json_data = response.json()

            # Extract values
            data = {
                "name": json_data['location']['name'],
                "region": json_data['location']['region'],
                "country": json_data['location']['country'],
                "lat": json_data['location']['lat'],
                "lon": json_data['location']['lon'],
                "tz_id": json_data['location']['tz_id'],
                "localtime_epoch": json_data['location']['localtime_epoch'],
                "localtime": json_data['location']['localtime'],
                "last_updated_epoch": json_data['current']['last_updated_epoch'],
                "last_updated": json_data['current']['last_updated'],
                "temp_c": json_data['current']['temp_c'],
                "temp_f": json_data['current']['temp_f'],
                "is_day": json_data['current']['is_day'],
                "condition_text": json_data['current']['condition']['text'],
                "condition_icon": json_data['current']['condition']['icon'],
                "wind_mph": json_data['current']['wind_mph'],
                "wind_kph": json_data['current']['wind_kph'],
                "wind_degree": json_data['current']['wind_degree'],
                "wind_dir": json_data['current']['wind_dir'],
                "pressure_mb": json_data['current']['pressure_mb'],
                "pressure_in": json_data['current']['pressure_in'],
                "precip_mm": json_data['current']['precip_mm'],
                "precip_in": json_data['current']['precip_in'],
                "humidity": json_data['current']['humidity'],
                "cloud": json_data['current']['cloud'],
                "feelslike_c": json_data['current']['feelslike_c'],
                "feelslike_f": json_data['current']['feelslike_f'],
                "vis_km": json_data['current']['vis_km'],
                "vis_miles": json_data['current']['vis_miles'],
                "uv": json_data['current']['uv'],
                "gust_mph": json_data['current']['gust_mph'],
                "gust_kph": json_data['current']['gust_kph'],
            }

            return render_template('home.html', **data)
        except:
            return render_template('home.html', error='Please enter a correct Place name...')

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    weather_json = request.form.get('weather_data')
    if not weather_json:
        return "No data to export", 400

    data = json.loads(weather_json)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Live Weather Report", ln=True, align='C')
    pdf.ln(10)

    for key, value in data.items():
        label = key.replace('_', ' ').title()
        pdf.cell(200, 10, txt=f"{label}: {value}", ln=True)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return send_file(pdf_output, as_attachment=True, download_name="weather_report.pdf")

if __name__ == '__main__':
    app.run(debug=True)
