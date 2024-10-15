import sqlite3

from flask import Flask, render_template, request, redirect, url_for, jsonify

from algorithms.api.openweathermap_api import get_pollution_data, get_pm_values
from algorithms.mailing_service.send_email import send_aqi_alert_to_subscribers
from algorithms.mailing_service.mailing_utils import add_email, get_all_emails
from algorithms.model.calculate_results_for_aqi import calculate_air_quality, calculate_air_quality_manually, \
    calculate_air_quality_manually_final_suggested_verdict
from algorithms.text2text_generation.google_flan_t5_large import generate_text__google_flan_t5_large
from algorithms.text2text_generation.intel_distilgpt2_wikitext2 import generate_text__intel_distilgpt2_wikitext2
from algorithms.text2text_generation.gpt_2_base_non_fine_tuned import generate_text__gpt2_base_non_fine_tuned
from data.chatbot_phrases import chatbot_conversations
from data.chatbot_aqi_queries import aqi_queries
from algorithms.summarizer.facebook_bart_large_cnn import summarize
from algorithms.summarizer.falconsai_text_summarization_model_t5 import summarize_model_t5
from algorithms.summarizer.meta_llama import summarize__llama_api
from algorithms.nlp_module.nlp__utils import query_key_comparator
from mm_algorithms.algorithms.algorithmic_toolbox import get_future_predictions, get_future_predictions_mlt

# Intel Optimised Model
from algorithms.model.intel_optimised_models.use_intel_optimised_model_for_calculation import \
    intel__calculate_air_quality_manually, intel__calculate_air_quality_manually_final_suggested_verdict

RECENT_CHATS = []
DATABASE = r"B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\database\emailing_list.db"
COMMUNITY_FORUM_DATABASE = r"B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\database\community_forum\community_forum.db"

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('HomePage.html')


@app.route('/process_input_for_aqi', methods=['POST', 'GET'])
def process_input():
    try:
        # Get the JSON data from the request
        data = request.json

        # Extract values from the request
        co = float(data.get('co'))
        no = float(data.get('no'))
        no2 = float(data.get('no2'))
        so2 = float(data.get('so2'))
        o3 = float(data.get('o3'))
        nh3 = float(data.get('nh3'))

        # Debug: Print the received data
        result_message = f"Received CO: {co}, NO: {no}, NO2: {no2}, SO2: {so2}, O3: {o3}, NH3: {nh3}"
        print(result_message)

        # Call your function with the extracted values
        # INTEL OPTIMIZATION
        fetch_from__calculate_results_for_aqi = intel__calculate_air_quality_manually(co, no, no2, so2, o3, nh3)

        print("Fetch >>> ", fetch_from__calculate_results_for_aqi)

        # Convert the dictionary to an HTML formatted string
        html_message = "<h3>Air Quality Results</h3><ul>"
        for key, value in fetch_from__calculate_results_for_aqi.items():
            html_message += f"<li><strong>{key}:</strong> {value}</li>"
        html_message += "</ul>"

        print(html_message)

        # Return the result as JSON with the HTML formatted string
        return jsonify({'message': html_message})

    except Exception as e:
        # Return an error message in case of an exception
        return jsonify({'error': str(e)}), 500


@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')

    if user_message.lower() in aqi_queries and 'aqi' in user_message.lower():
        pollution_data = get_pollution_data()  # this is a dictionary

        co = float(pollution_data.get('co'))
        no = float(pollution_data.get('no'))
        no2 = float(pollution_data.get('no2'))
        so2 = float(pollution_data.get('so2'))
        o3 = float(pollution_data.get('o3'))
        nh3 = float(pollution_data.get('nh3'))

        # Build the HTML message
        html_message = "<h3>Air Quality Results</h3><ul>"
        for key, value in pollution_data.items():
            html_message += f"<li><strong>{key}:</strong> {value}</li>"
        html_message += "</ul>"

        # INTEL OPTIMIZATION
        html_message += f"<br><h3>Verdict: <b>{intel__calculate_air_quality_manually_final_suggested_verdict(co, no, no2, o3, so2, nh3)}</b></h3>"

        # Print the message for debugging
        print("get_aqi_results: ", html_message)
        RECENT_CHATS.append((user_message, html_message))
        return jsonify({'response': html_message})

    print("Hello from the chat bot")
    print(RECENT_CHATS)

    for key in chatbot_conversations.keys():
        if user_message == key:
            bot_response = chatbot_conversations[key]

            RECENT_CHATS.append((user_message, bot_response))

            return jsonify({"response": bot_response})

    else:
        for key in chatbot_conversations.keys():
            if user_message.lower() in key.lower():
                bot_response = chatbot_conversations[key]

                RECENT_CHATS.append((user_message, bot_response))

                return jsonify({"response": bot_response})
        else:
            for key in chatbot_conversations.keys():
                if query_key_comparator(query=user_message, key=key, threshold=0.54666) is True:
                    bot_response = chatbot_conversations[key]

                    RECENT_CHATS.append((user_message, bot_response))
                    return jsonify({"response": bot_response})

    # Ensure user_message is a string
    if isinstance(user_message, str) and user_message.strip():
        bot_response = generate_text__gpt2_base_non_fine_tuned(user_message)
        bot_response += "<br><h4>Generated text from Intel/distilgpt2-wikitext2</h4><b><i>(not fine-tuned)</i></b><br><br>"
        bot_response += generate_text__intel_distilgpt2_wikitext2(user_message)
        # Add to recent chats
        RECENT_CHATS.append((user_message, bot_response))
    else:
        bot_response = "I didn't get that."

    return jsonify({"response": bot_response})


@app.route('/load_chats', methods=['GET'])
def load_chats():
    return jsonify({"recent_chats": RECENT_CHATS})


@app.route('/get_aqi_results', methods=['POST'])
def get_aqi_results():
    print("Hello !!!")
    pollution_data = get_pollution_data()  # this is a dictionary

    # Build the HTML message
    html_message = "<h3>Air Quality Results</h3><ul>"
    for key, value in pollution_data.items():
        html_message += f"<li><strong>{key}:</strong> {value}</li>"
    html_message += "</ul>"

    # Print the message for debugging
    print("get_aqi_results: ", html_message)

    # Return the result as JSON with the HTML formatted string
    return jsonify({'message': html_message})


# Email submission route
@app.route('/submit_email', methods=['POST'])
def submit_email():
    try:
        # Get the email from the request JSON body
        data = request.get_json()
        user_email = data.get('User_email')

        print(user_email)

        # Validate if an email is provided (add further validation if necessary)
        if not user_email:
            return jsonify({'message': 'Failed! No email provided.'}), 400

        # Optionally: Add logic to store/process the email here
        add_email(user_email, DATABASE)
        print("database >>> ", get_all_emails(DATABASE))
        # For example, saving the email to a database or sending a notification

        # Return success if everything went fine
        return jsonify({'message': 'Success!'}), 200
    except Exception as e:
        # Log error and return failure response
        print(f"Error: {e}")
        return jsonify({'message': 'Failed!'}), 500


def get_db_connection():
    conn = sqlite3.connect(COMMUNITY_FORUM_DATABASE)
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn


# Route to post a new comment
@app.route('/post_comment', methods=['POST'])
def post_comment():
    comment = request.json.get('comment')

    if not comment:
        return jsonify({'error': 'Comment cannot be empty'}), 400

    print("Comment entered: ", comment)

    conn = get_db_connection()
    conn.execute('INSERT INTO comments (comment) VALUES (?)', (comment,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Comment added successfully'}), 201


# Route to get all comments (latest first)
@app.route('/get_comments', methods=['GET'])
def get_comments():
    conn = get_db_connection()
    comments = conn.execute('SELECT comment, timestamp FROM comments ORDER BY timestamp DESC').fetchall()
    conn.close()

    # Convert to list of dictionaries
    comment_list = [{'comment': row['comment'], 'timestamp': row['timestamp']} for row in comments]

    return jsonify(comment_list), 200


def get_only_comments_as_text():
    conn = get_db_connection()

    # Fetch all comments from the database
    comments = conn.execute('SELECT comment FROM comments ORDER BY timestamp DESC').fetchall()
    conn.close()

    # Extract the comment from each tuple and join them into a single string
    comments_text = " ".join([i[0] for i in comments])
    return comments_text


@app.route('/get_summary')
def get_summary():
    # You can dynamically generate or fetch the summary content here
    comments = get_only_comments_as_text()

    summary = summarize__llama_api(comments)
    return summary


@app.route('/city-report')
def city_report():
    return render_template('CityReport.html')


@app.route('/what-are-pollutants')
def what_are_pollutants():
    return render_template('WhatArePollutantsInfo.html')


@app.route('/return-home')
def return_home():
    return render_template('HomePage.html')


@app.route('/pollution-factors')
def pollution_factors():
    return render_template('PollutionFactors.html')


@app.route('/get_daily_data', methods=['GET'])
def get_daily_data():
    averages, next_day = get_future_predictions()
    return jsonify(next_day)


@app.route('/get_weekly_data', methods=['GET'])
def get_weekly_data():
    # Get data for the next 7 days
    averages, next_day = get_future_predictions()
    return jsonify(averages)


@app.route('/api/predictions')
def get_predictions():
    # Sample prediction data (this should be replaced with real prediction data)
    pm_values = get_pm_values()
    actual_pm2_5 = pm_values['pm2.5']
    actual_pm10 = pm_values['pm10']
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    aqi_values, predicted_aqi = get_future_predictions_mlt()

    # Return as JSON
    return jsonify({
        'predicted_aqi': predicted_aqi,
        'predicted_pm2_5': actual_pm2_5,
        'predicted_pm10': actual_pm10,
        'days': days,
        'aqi_values': aqi_values
    })


if __name__ == '__main__':
    app.run(debug=True)
    app.run()
