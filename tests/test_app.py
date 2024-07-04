import pytest
import requests

BASE_URL = "http://localhost:5000"  # URL where the Docker container is running


@pytest.fixture
def client():
    yield requests.Session()


def test_ask_endpoint_saves_question_and_answer(client):
    # Given
    question = "What is the capital of France?"
    expected_answer = "The capital of France is Paris."

    # When
    response = client.post(f"{BASE_URL}/ask", json={"question": question})

    # Then
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert expected_answer in data["answer"].strip()

    # Check if the question and answer are saved in the database
    response = client.get(f"{BASE_URL}/questions")
    saved_qa = response.json()
    assert any(
        qa["question"] == question and expected_answer in qa["answer"].strip()
        for qa in saved_qa
    )


def test_ask_endpoint_saves_multiple_questions_and_answers(client):
    # Given
    questions_and_answers = [
        ("What is the capital of France?", "The capital of France is Paris."),
        ("Who wrote Pride and Prejudice?", "Jane Austen wrote Pride and Prejudice."),
        (
            "What is the speed of light?",
            "The speed of light is approximately 299,792 kilometers per second.",
        ),
    ]

    # When
    for question, answer in questions_and_answers:
        response = client.post(f"{BASE_URL}/ask", json={"question": question})
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert (
            answer.split()[0] in data["answer"].strip()
        )  # Check if the first word of the expected answer is in the actual answer

    # Then
    # Check if all questions and answers are saved in the database
    response = client.get(f"{BASE_URL}/questions")
    saved_qa = response.json()
    for question, answer in questions_and_answers:
        assert any(
            qa["question"] == question and answer.split()[0] in qa["answer"].strip()
            for qa in saved_qa
        )


def test_ask_endpoint_saves_empty_question(client):
    # Given
    question = ""

    # When
    response = client.post(f"{BASE_URL}/ask", json={"question": question})

    # Then
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"] == "Question is required"

    # Check if no question and answer are saved in the database
    response = client.get(f"{BASE_URL}/questions")
    saved_qa = response.json()
    assert not any(qa["question"] == question for qa in saved_qa)


def test_ask_endpoint_saves_question_with_special_characters(client):
    # Given
    question = "What is the symbol for the element Gold?"

    # When
    response = client.post(f"{BASE_URL}/ask", json={"question": question})

    # Then
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"].strip() != ""

    # Check if the question and answer are saved in the database
    response = client.get(f"{BASE_URL}/questions")
    saved_qa = response.json()
    assert any(
        qa["question"] == question and qa["answer"].strip() != "" for qa in saved_qa
    )
