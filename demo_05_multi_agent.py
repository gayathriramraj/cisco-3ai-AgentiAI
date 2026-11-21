"""Demo 5: writer and reviewer agents collaborate with limited revision."""
from agent_core import ask_llm

if __name__ == "__main__":
    topic = input("Topic (Enter for sample): ").strip() or "Explain password safety to first-year students"
    writer_system = "You are a training-content writer. Draft a clear mini lesson with 3 tips and 1 short quiz question. Avoid unsupported statistics."
    reviewer_system = "You are a strict training quality reviewer. Evaluate correctness, clarity, inclusivity and completeness. Return concrete improvements, and flag unsupported claims."
    print("\n[Agent 1: Writer] Creating draft...")
    draft = ask_llm(writer_system, topic)
    print(draft)
    print("\n[Agent 2: Reviewer] Checking draft...")
    review = ask_llm(reviewer_system, f"Topic: {topic}\n\nDraft:\n{draft}")
    print(review)
    print("\n[Agent 1: Writer] Revising once based on review...")
    revised = ask_llm(writer_system, f"Improve the draft using the reviewer feedback.\nDraft:\n{draft}\nFeedback:\n{review}")
    print("\nFINAL VERSION:\n", revised)
