from backend.services.knowledge_chain import (
    reconstruct_knowledge_chain,
)
from backend.services.gemini import ask_gemini


def format_chains_for_llm(
    start_knowledge: dict | None,
    chains: list[dict],
) -> str:
    """
    Build complete evidence context including
    the starting knowledge unit and all
    reconstructed position-specific chains.
    """

    sections = []

    # =====================================================
    # Start Knowledge
    # =====================================================

    if start_knowledge:

        start_section = f"""
START KNOWLEDGE

Knowledge ID: {start_knowledge['knowledge_id']}
Knowledge Type: {start_knowledge['knowledge_type']}
Content: {start_knowledge['content']}
Source Type: {start_knowledge['source_type']}
Source Title: {start_knowledge['source_title']}
Source Location: {start_knowledge['source_location']}
System Name: {start_knowledge['system_name']}
""".strip()

        sections.append(start_section)

    # =====================================================
    # Position-Specific Chains
    # =====================================================

    for chain_result in chains:

        position_name = chain_result[
            "position_name"
        ]

        lines = [
            f"POSITION CONTEXT: {position_name}"
        ]

        for step in chain_result["chain"]:

            knowledge = step["knowledge"]

            lines.append(
                f"""
Relation: {step['relation_type']}
Knowledge ID: {knowledge['knowledge_id']}
Knowledge Type: {knowledge['knowledge_type']}
Content: {knowledge['content']}
Source Type: {knowledge['source_type']}
Source Title: {knowledge['source_title']}
Source Location: {knowledge['source_location']}
System Name: {knowledge['system_name']}
""".strip()
            )

        sections.append(
            "\n\n".join(lines)
        )

    return "\n\n---\n\n".join(
        sections
    )


def analyze_evidence(
    question: str,
    chain_context: str,
) -> str:
    """
    Separate confirmed facts, supported inference,
    and explicit evidence gaps.
    """

    prompt = f"""
You are analyzing enterprise knowledge evidence.

Your task is NOT to answer the user yet.

Classify the provided evidence into exactly three groups:

1. CONFIRMED_FACTS

Statements directly supported by the provided knowledge.

2. INFERENCES

Conclusions reasonably derived from relationships between
the confirmed facts, but not directly stated by the sources.

3. UNKNOWNS

Information required to answer the user's question with
certainty, but which cannot be established from the
provided evidence.

STRICT RULES:

- Use ONLY information contained in the provided evidence.
- Do NOT introduce external technical knowledge.
- Do NOT invent possible causes, examples, scenarios,
  technologies, symptoms, or explanations.
- Do NOT list hypothetical alternatives unless they are
  explicitly mentioned in the evidence.
- Never convert correlation into confirmed causation.
- A successful resolution does not prove root cause.
- If a source identifies something as a "factor",
  do not rewrite it as "the cause".
- Every INFERENCE must be traceable to CONFIRMED_FACTS.
- UNKNOWNS must describe missing evidence only.
- Do not speculate about what the missing information
  might contain.

Example:

Incorrect UNKNOWN:
- Network latency may also have caused the issue.

Correct UNKNOWN:
- The available evidence does not establish whether
  additional factors contributed to the issue.

User Question:
{question}

Knowledge Evidence:
{chain_context}

Return exactly:

CONFIRMED_FACTS:
- ...

INFERENCES:
- ...

UNKNOWNS:
- ...
"""

    return ask_gemini(
        prompt
    )


def generate_grounded_answer(
    question: str,
    user_context: str,
    evidence_analysis: str,
) -> str:
    """
    Generate the final answer while preserving
    the boundary between facts and inference.
    """

    prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question using ONLY the evidence
analysis below.

User Context:
{user_context}

User Question:
{question}

Evidence Analysis:
{evidence_analysis}

STRICT RULES:

1. CONFIRMED_FACTS may be stated as facts.

2. INFERENCES must always be clearly qualified using
   language such as:
   - suggests
   - likely
   - may have contributed
   - appears consistent with

3. Never present an inference as confirmed causation.

4. UNKNOWNS must remain unknown.
   Do not fill missing information using general
   technical knowledge.

5. Do NOT introduce examples of possible causes that
   are absent from the evidence.

6. Do NOT add external knowledge.

7. If the root cause is not confirmed, explicitly say:
   "The definitive root cause is not established by
   the available knowledge."

8. Keep the answer concise and evidence-focused.

Answer:
"""

    return ask_gemini(
        prompt
    )


def answer_with_knowledge_chain(
    user_id: int,
    question: str,
) -> dict:
    """
    End-to-end Knowledge Chain answer generation.

    Flow:
        Question
          ↓
        Semantic Search
          ↓
        Start Knowledge
          ↓
        User Position Context
          ↓
        Multi-Chain Reconstruction
          ↓
        Evidence Analysis
          ↓
        Fact / Inference Separation
          ↓
        Grounded Answer
    """

    # =====================================================
    # 1. Reconstruct Knowledge Chains
    # =====================================================

    reconstruction = (
        reconstruct_knowledge_chain(
            user_id=user_id,
            question=question,
        )
    )

    chains = reconstruction[
        "chains"
    ]

    positions = reconstruction[
        "positions"
    ]

    start_knowledge = reconstruction[
        "start_knowledge"
    ]

    position_names = [
        position["position_name"]
        for position in positions
    ]

    # =====================================================
    # 2. No Relevant Chain
    # =====================================================

    if not chains:

        return {
            "answer": (
                "No relevant organizational knowledge "
                "was found for the user's current "
                "position context."
            ),
            "evidence_analysis": None,
            "evidence_context": None,
            "user_id": user_id,
            "positions": position_names,
            "question": question,
            "start_knowledge_id": reconstruction[
                "start_knowledge_id"
            ],
            "start_knowledge": start_knowledge,
            "search_score": reconstruction[
                "search_score"
            ],
            "chains": [],
        }

    # =====================================================
    # 3. Build User Context
    # =====================================================

    user_context = ", ".join(
        position_names
    )

    # =====================================================
    # 4. Build Complete Evidence Context
    # =====================================================

    evidence_context = (
        format_chains_for_llm(
            start_knowledge=start_knowledge,
            chains=chains,
        )
    )

    # =====================================================
    # 5. Evidence Analysis
    # =====================================================

    evidence_analysis = (
        analyze_evidence(
            question=question,
            chain_context=evidence_context,
        )
    )

    # =====================================================
    # 6. Grounded Answer Generation
    # =====================================================

    answer = (
        generate_grounded_answer(
            question=question,
            user_context=user_context,
            evidence_analysis=evidence_analysis,
        )
    )

    # =====================================================
    # 7. Return Result
    # =====================================================

    return {
        "answer": answer,
        "evidence_analysis": evidence_analysis,
        "evidence_context": evidence_context,
        "user_id": user_id,
        "positions": position_names,
        "question": question,
        "start_knowledge_id": reconstruction[
            "start_knowledge_id"
        ],
        "start_knowledge": start_knowledge,
        "search_score": reconstruction[
            "search_score"
        ],
        "chains": chains,
    }


# =========================================================
# Local Test
# =========================================================

if __name__ == "__main__":

    question = (
        "Why did the nightly batch processing become slow?"
    )

    for user_id in [
        1,
        2,
        3,
    ]:

        result = (
            answer_with_knowledge_chain(
                user_id=user_id,
                question=question,
            )
        )

        print(
            "\n================================"
        )

        print(
            f"UserId   : "
            f"{result['user_id']}"
        )

        print(
            f"Positions: "
            f"{', '.join(result['positions'])}"
        )

        print(
            f"Question : "
            f"{result['question']}"
        )

        print(
            f"Start    : "
            f"{result['start_knowledge_id']}"
        )

        if (
            result["search_score"]
            is not None
        ):

            print(
                f"Similarity: "
                f"{result['search_score']:.4f}"
            )

        # ---------------------------------------------
        # Evidence Context
        # ---------------------------------------------

        if result["evidence_context"]:

            print(
                "\n--- Evidence Context ---"
            )

            print(
                result["evidence_context"]
            )

        # ---------------------------------------------
        # Evidence Analysis
        # ---------------------------------------------

        if result["evidence_analysis"]:

            print(
                "\n--- Evidence Analysis ---"
            )

            print(
                result["evidence_analysis"]
            )

        # ---------------------------------------------
        # Final Answer
        # ---------------------------------------------

        print(
            "\n--- Final Answer ---"
        )

        print(
            result["answer"]
        )