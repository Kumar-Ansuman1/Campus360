"""
Campus360 Advanced RAG - Evidence Retrieval Layer

Retrieves relevant operational knowledge from a local knowledge base
and provides evidence that can be attached to AI recommendations.

Designed so a real embedding/vector database can be plugged in later.
"""

from pathlib import Path
import re
from datetime import datetime


class RAGEngine:

    def __init__(self, knowledge_dir="ai/data/knowledge"):
        self.knowledge_dir = Path(knowledge_dir)
        self.documents = []

        self._load_documents()

    def _load_documents(self):
        """Load local knowledge documents."""

        self.knowledge_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        for file in self.knowledge_dir.glob("*.txt"):

            try:
                text = file.read_text(
                    encoding="utf-8"
                )

                self.documents.append({
                    "source": file.name,
                    "text": text
                })

            except Exception as e:
                print(
                    f"Could not load {file}: {e}"
                )

    def _tokenize(self, text):
        """Simple normalized tokenization."""

        return set(
            re.findall(
                r"\b[a-zA-Z0-9]+\b",
                text.lower()
            )
        )

    def _score_document(self, query, document):
        """
        Calculate relevance using keyword overlap.

        This is intentionally deterministic and explainable.
        """

        query_tokens = self._tokenize(query)
        document_tokens = self._tokenize(
            document["text"]
        )

        if not query_tokens:
            return 0.0

        overlap = (
            query_tokens &
            document_tokens
        )

        return round(
            len(overlap) /
            len(query_tokens),
            4
        )

    def retrieve(self, query, top_k=3):
        """
        Retrieve the most relevant documents.
        """

        results = []

        for document in self.documents:

            score = self._score_document(
                query,
                document
            )

            if score > 0:

                results.append({
                    "source": document["source"],
                    "relevance_score": score,
                    "text": document["text"]
                })

        results.sort(
            key=lambda x: x["relevance_score"],
            reverse=True
        )

        return results[:top_k]

    def build_evidence(self, query, top_k=3):
        """
        Create an evidence package for the reasoning layer.
        """

        retrieved = self.retrieve(
            query=query,
            top_k=top_k
        )

        evidence = []

        for item in retrieved:

            evidence.append({
                "source": item["source"],
                "relevance_score":
                    item["relevance_score"],
                "evidence":
                    item["text"]
            })

        return {
            "query": query,
            "retrieved_documents": len(evidence),
            "evidence": evidence,
            "generated_at":
                datetime.now().isoformat()
        }


if __name__ == "__main__":

    print("=" * 60)
    print("CAMPUS360 ADVANCED RAG ENGINE")
    print("=" * 60)

    engine = RAGEngine()

    print(
        f"\nKnowledge documents loaded: "
        f"{len(engine.documents)}"
    )

    query = (
        "high energy consumption HVAC "
        "efficiency inspection"
    )

    result = engine.build_evidence(
        query=query,
        top_k=3
    )

    print("\nQuery:")
    print(query)

    print(
        "\nRetrieved documents:",
        result["retrieved_documents"]
    )

    for item in result["evidence"]:

        print("\n----------------------------------------")
        print(
            "Source:",
            item["source"]
        )
        print(
            "Relevance:",
            item["relevance_score"]
        )
        print(
            "Evidence:",
            item["evidence"][:500]
        )

    print("\n" + "=" * 60)
    print("RAG ENGINE TEST COMPLETE")
    print("=" * 60)