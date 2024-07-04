from flask import Blueprint, request, jsonify
from .models import QuestionAnswer
from . import db
import openai
import os

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

main = Blueprint("main", __name__)


# Endpoint that will get all the questions and answers(used for testing)
@main.route("/questions", methods=["GET"])
def get_questions():
    questions = QuestionAnswer.query.all()
    print(questions)
    return jsonify(
        [
            {"question": qa.question, "answer": qa.answer, "created_at": qa.created_at}
            for qa in questions
        ]
    )


@main.route("/ask", methods=["POST"])
def ask():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    # Use OpenAI API to get an answer
    try:
        assistant = client.beta.assistants.create(
            name="ChatGPT",
            instructions="You are a personal helper who can answer any question the user have.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview",
        )

        thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question,
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="The user has a premium account.",
        )

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            answer = " ".join(
                message.content[0].text.value
                for message in messages
                if message.content[0].type == "text"
            )
        else:
            answer = "Failed to get a response from the assistant."

        client.beta.assistants.delete(assistant.id)

        answer = answer.replace(question, "")
        print(answer)

        # Save the question and answer to the database
        new_qa = QuestionAnswer()
        new_qa.question = question
        new_qa.answer = answer
        db.session.add(new_qa)
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"answer": answer})
