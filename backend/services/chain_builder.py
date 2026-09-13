from backend.repositories.knowledge_relation_repository import (
    get_relations_from_knowledge,
)


def build_chain_for_position(
    start_knowledge_id: int,
    position_id: int,
    max_depth: int = 10,
) -> list[dict]:
    """
    Build one chain for one position.
    """

    chain = []

    visited = {start_knowledge_id}
    current_knowledge_id = start_knowledge_id

    depth = 0

    while depth < max_depth:

        relations = get_relations_from_knowledge(
            current_knowledge_id
        )

        if not relations:
            break

        candidates = []

        for relation in relations:

            relation_position_ids = {
                position["position_id"]
                for position in relation["positions"]
            }

            if position_id not in relation_position_ids:
                continue

            confidence = (
                relation["confidence"]
                if relation["confidence"] is not None
                else 0
            )

            candidates.append(
                {
                    "relation": relation,
                    "confidence": confidence,
                }
            )

        if not candidates:
            break

        candidates.sort(
            key=lambda x: x["confidence"],
            reverse=True,
        )

        relation = candidates[0]["relation"]

        next_knowledge_id = relation[
            "to_knowledge_id"
        ]

        if next_knowledge_id in visited:
            break

        chain.append(relation)

        visited.add(next_knowledge_id)

        current_knowledge_id = next_knowledge_id

        depth += 1

    return chain


def build_chains(
    start_knowledge_id: int,
    user_positions: list[dict],
    max_depth: int = 10,
) -> list[dict]:
    """
    Build one relevant knowledge chain
    for each user position.
    """

    chains = []

    for position in user_positions:

        position_id = position["position_id"]
        position_name = position["position_name"]

        chain = build_chain_for_position(
            start_knowledge_id=start_knowledge_id,
            position_id=position_id,
            max_depth=max_depth,
        )

        if not chain:
            continue

        chains.append(
            {
                "position_id": position_id,
                "position_name": position_name,
                "chain": chain,
            }
        )

    return chains