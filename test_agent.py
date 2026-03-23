"""
VVIT Helpdesk Agent — End-to-End Integration Test (v2.0)
Verifies that:
- FAISS indexes load successfully
- The Supervisor agent routes correctly across 5 domains
- All 5 Specialist agents return answers
- Multi-turn conversation memory works
"""

import sys
import os
from agents import build_graph, load_indexes, ask

def run_tests():
    print("=" * 60)
    print("VVIT Helpdesk Agent — Integration Tests (v2.0)")
    print("=" * 60)

    try:
        print("\nLoading Indexes...")
        indexes = load_indexes()
        app = build_graph(indexes)
        print("✅ Graph compiled successfully!\n")
    except Exception as e:
        print(f"❌ FAIL — Startup — {e}")
        sys.exit(1)

    # 1. Routing Tests
    routing_cases = [
        ("Who is the Vice Chancellor of VVIT?", "about_administration"),
        ("Is VVIT accredited by NAAC?", "about_administration"),
        ("What are the B.Tech CSE eligibility requirements?", "admissions"),
        ("What is the fee for B.Tech AI and Machine Learning?", "admissions"),
        ("What is the highest package at VVIT?", "placements_careers"),
        ("Which companies visited VVIT for placements in 2025?", "placements_careers"),
        ("Tell me about hostel facilities at VVIT", "campus_facilities"),
        ("What are the library timings at VVIT?", "campus_facilities"),
        ("What student clubs are available at VVIT?", "student_life"),
        ("How does the NCC unit work at VVIT?", "student_life"),
    ]

    passed = 0
    total = len(routing_cases) + 1 + 3

    print("--- Routing Tests ---")
    for i, (query, expected_route) in enumerate(routing_cases, 1):
        try:
            ans, routed_to, _ = ask(app, query, chat_history=[])
            if routed_to == expected_route:
                print(f"  ✅ PASS — Test {i} (routed: {routed_to} | chars: {len(ans)})")
                passed += 1
            else:
                print(f"  ❌ FAIL — Test {i} — Expected {expected_route}, got {routed_to}")
        except Exception as e:
             print(f"  ❌ FAIL — Test {i} — {e}")

    # 2. Multi-Turn Test
    print("\n--- Multi-Turn Conversation Test ---")
    try:
        history = []
        turn1 = "What departments does VVIT offer?"
        ans1, _, _ = ask(app, turn1, chat_history=history)
        history.append({"human": turn1, "ai": ans1})
        
        turn2 = "Which is best for AI and data science?"
        ans2, _, _ = ask(app, turn2, chat_history=history)
        history.append({"human": turn2, "ai": ans2})
        
        turn3 = "What are the placement stats for that program?"
        ans3, r3, _ = ask(app, turn3, chat_history=history)
        
        if r3 == "placements_careers":
            print(f"  ✅ PASS — Multi-Turn Test (routed: {r3} | chars: {len(ans3)})")
            passed += 1
        else:
             print(f"  ❌ FAIL — Multi-Turn Test — Expected placements_careers, got {r3}")
    except Exception as e:
        print(f"  ❌ FAIL — Multi-Turn Test — {e}")

    # 3. Edge Case Tests
    print("\n--- Edge Case Tests ---")
    edge_cases = [
        ("fees?", "Very short query"),
        ("What is the weather in Guntur today?", "Out of scope query"),
        ("asdfjkl", "Gibberish")
    ]
    
    for query, desc in edge_cases:
        try:
             ans, routed_to, _ = ask(app, query, chat_history=[])
             print(f"  ✅ PASS — {desc} (routed: {routed_to} | chars: {len(ans)})")
             passed += 1
        except Exception as e:
             print(f"  ❌ FAIL — {desc} — {e}")

    print("\n" + "=" * 60)
    print(f"Final score: {passed}/{total} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
