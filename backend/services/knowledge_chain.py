from backend.services.kc_retrieval import (
    search_kc_knowledge,
)
from backend.services.chain_builder import (
    build_chains,
)
from backend.repositories.user_repository import (
    get_user_positions,
)
from backend.repositories.kc_knowledge_repository import (
    get_kc_knowledge_by_id,
)


def reconstruct_knowledge_chain(
    user_id: int,
    question: str,
) -> dict:
    """
    Reconstruct multiple knowledge chains
    based on semantic search and the user's
    position context.

    Flow:
        User
          ↓
        Positions
          ↓
        Semantic Search
          ↓
        Start Knowledge
          ↓
        Position-specific Chains
    """

    # =====================================================
    # 1. Get User Context
    # =====================================================

    positions = get_user_positions(
        user_id
    )

    if not positions:

        return {
            "user_id": user_id,
            "positions": [],
            "question": question,
            "start_knowledge_id": None,
            "start_knowledge": None,
            "search_score": None,
            "chains": [],
        }

    # =====================================================
    # 2. Semantic Search
    # =====================================================

    search_results = search_kc_knowledge(
        question=question,
        top_k=1,
    )

    if not search_results:

        return {
            "user_id": user_id,
            "positions": positions,
            "question": question,
            "start_knowledge_id": None,
            "start_knowledge": None,
            "search_score": None,
            "chains": [],
        }

    top_result = search_results[0]

    start_knowledge_id = top_result[
        "KnowledgeId"
    ]

    search_score = top_result[
        "Score"
    ]

    # =====================================================
    # 3. Retrieve Start Knowledge
    #
    # Important:
    # The semantic search result itself must also
    # become part of the evidence given to the LLM.
    #
    # Before v0.6.1 only the destination knowledge
    # contained in the relations was passed onward,
    # which caused the original Incident to be lost.
    # =====================================================

    start_knowledge = get_kc_knowledge_by_id(
        start_knowledge_id
    )

    if not start_knowledge:

        return {
            "user_id": user_id,
            "positions": positions,
            "question": question,
            "start_knowledge_id": start_knowledge_id,
            "start_knowledge": None,
            "search_score": search_score,
            "chains": [],
        }

    # =====================================================
    # 4. Build Position-Aware Multiple Chains
    # =====================================================

    chains = build_chains(
        start_knowledge_id=start_knowledge_id,
        user_positions=positions,
    )

    # =====================================================
    # 5. Return Complete Reconstruction
    # =====================================================

    return {
        "user_id": user_id,
        "positions": positions,
        "question": question,
        "start_knowledge_id": start_knowledge_id,
        "start_knowledge": start_knowledge,
        "search_score": search_score,
        "chains": chains,
    }


# =========================================================
# Local Test
# =========================================================

if __name__ == "__main__":

    question = (
        "Why did the nightly batch processing become slow?"
    )

    for user_id in [1, 2, 3]:

        result = reconstruct_knowledge_chain(
            user_id=user_id,
            question=question,
        )

        print("\n================================")

        print(
            f"UserId   : "
            f"{result['user_id']}"
        )

        position_names = [
            position["position_name"]
            for position in result["positions"]
        ]

        print(
            f"Positions: "
            f"{', '.join(position_names)}"
        )

        print(
            f"Question : "
            f"{result['question']}"
        )

        print(
            f"Start    : "
            f"{result['start_knowledge_id']}"
        )

        if result["search_score"] is not None:

            print(
                f"Similarity: "
                f"{result['search_score']:.4f}"
            )

        # -------------------------------------------------
        # Start Knowledge
        # -------------------------------------------------

        print("\nStart Knowledge:")

        start_knowledge = result[
            "start_knowledge"
        ]

        if start_knowledge:

            print(
                f"  "
                f"{start_knowledge['knowledge_type']}: "
                f"{start_knowledge['content']}"
            )

            print(
                f"  Source: "
                f"{start_knowledge['source_type']} "
                f"({start_knowledge['source_title']})"
            )

        else:

            print(
                "  No start knowledge found."
            )

        # -------------------------------------------------
        # Reconstructed Chains
        # -------------------------------------------------

        print("\nChains:")

        if not result["chains"]:

            print(
                "  No relevant chains found."
            )

        for chain_result in result["chains"]:

            print(
                f"\n  "
                f"[{chain_result['position_name']}]"
            )

            for step in chain_result["chain"]:

                knowledge = step[
                    "knowledge"
                ]

                print(
                    f"    "
                    f"{step['from_knowledge_id']} "
                    f"--[{step['relation_type']}]--> "
                    f"{step['to_knowledge_id']}"
                )

                print(
                    f"       "
                    f"{knowledge['knowledge_type']}: "
                    f"{knowledge['content']}"
                )

                print(
                    f"       "
                    f"Source: "
                    f"{knowledge['source_type']} "
                    f"({knowledge['source_title']})"
                )