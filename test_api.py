#!/usr/bin/env python3
"""
API Test Script for AI Proctoring System
Tests all major endpoints to ensure everything is working
"""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

def print_test(test_name):
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print('='*60)

def test_root():
    print_test("Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_register():
    print_test("User Registration")
    try:
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }
        response = requests.post(f"{BASE_URL}/api/register", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        # 400 is OK if user already exists
        assert response.status_code in [200, 400]
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_login():
    print_test("User Login")
    try:
        data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/api/login", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        assert response.status_code == 200
        assert "user_id" in result
        print("✅ PASSED")
        return result
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return None

def test_create_question():
    print_test("Create Question")
    try:
        data = {
            "question_text": "What is 2+2?",
            "option_a": "3",
            "option_b": "4",
            "option_c": "5",
            "option_d": "6",
            "correct_answer": "B",
            "subject": "Mathematics",
            "difficulty": "easy"
        }
        response = requests.post(f"{BASE_URL}/api/questions", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_get_questions():
    print_test("Get Questions")
    try:
        response = requests.get(f"{BASE_URL}/api/questions?limit=5")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Total questions: {result['total']}")
        if result['total'] > 0:
            print(f"First question: {result['questions'][0]['question_text'][:50]}...")
        assert response.status_code == 200
        print("✅ PASSED")
        return result['questions']
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return []

def test_start_exam(user_id):
    print_test("Start Exam")
    try:
        response = requests.post(
            f"{BASE_URL}/api/exam/start",
            json={"user_id": user_id, "exam_name": "Test Exam"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        assert response.status_code == 200
        assert "exam_id" in result
        print("✅ PASSED")
        return result["exam_id"]
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return None

def test_submit_answer(exam_id, question_id):
    print_test("Submit Answer")
    try:
        data = {
            "exam_id": exam_id,
            "question_id": question_id,
            "user_answer": "A"
        }
        response = requests.post(f"{BASE_URL}/api/exam/submit", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_finish_exam(exam_id):
    print_test("Finish Exam")
    try:
        response = requests.post(
            f"{BASE_URL}/api/exam/finish",
            json={"exam_id": exam_id}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        assert response.status_code == 200
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_get_results(exam_id):
    print_test("Get Exam Results")
    try:
        response = requests.get(f"{BASE_URL}/api/exam/results/{exam_id}")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Score: {result['exam']['score']}")
        print(f"Total answers: {len(result['answers'])}")
        print(f"Total violations: {len(result['violations'])}")
        assert response.status_code == 200
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_generate_questions():
    print_test("Generate Questions (AI)")
    try:
        data = {
            "subject": "Python Programming",
            "difficulty": "easy",
            "count": 3
        }
        response = requests.post(f"{BASE_URL}/api/questions/generate", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Generated: {result['count']} questions")
        assert response.status_code == 200
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("AI PROCTORING SYSTEM - API TEST SUITE")
    print("="*60)
    
    results = {
        "passed": 0,
        "failed": 0
    }
    
    # Test 1: Root endpoint
    if test_root():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    sleep(0.5)
    
    # Test 2: Registration
    if test_register():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    sleep(0.5)
    
    # Test 3: Login
    user_data = test_login()
    if user_data:
        results["passed"] += 1
        user_id = user_data["user_id"]
    else:
        results["failed"] += 1
        print("\n⚠️ Cannot continue tests without login")
        return
    
    sleep(0.5)
    
    # Test 4: Create question
    if test_create_question():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    sleep(0.5)
    
    # Test 5: Get questions
    questions = test_get_questions()
    if questions:
        results["passed"] += 1
    else:
        results["failed"] += 1
        print("\n⚠️ No questions available for exam tests")
        return
    
    sleep(0.5)
    
    # Test 6: Start exam
    exam_id = test_start_exam(user_id)
    if exam_id:
        results["passed"] += 1
    else:
        results["failed"] += 1
        return
    
    sleep(0.5)
    
    # Test 7: Submit answer
    if questions and test_submit_answer(exam_id, questions[0]['id']):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    sleep(0.5)
    
    # Test 8: Finish exam
    if test_finish_exam(exam_id):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    sleep(0.5)
    
    # Test 9: Get results
    if test_get_results(exam_id):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    sleep(0.5)
    
    # Test 10: Generate questions
    if test_generate_questions():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Total: {results['passed'] + results['failed']}")
    print("="*60)
    
    if results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED! System is working correctly.")
    else:
        print(f"\n⚠️ {results['failed']} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
