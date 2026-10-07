"""
Campus360 AI - Advanced Semantic RAG

Responsibilities:
- Load facility knowledge documents
- Chunk documents
- Generate semantic embeddings
- Build FAISS vector index
- Retrieve relevant evidence
- Provide grounded context to the reasoning engine

Compatible interfaces:
    AdvancedRAG
    AdvancedSemanticRAG
"""

import os
import glob

try:
    import faiss
except ImportError:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class AdvancedRAG:

    def __init__(
        self,
        knowledge_path=None,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):
        if knowledge_path is None:
            knowledge_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "data",
                    "knowledge"
                )
            )

        self.knowledge_path = knowledge_path
        self.model_name = model_name

        self.documents = []
        self.embeddings = None
        self.index = None
        self.model = None

        self._initialize()

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def _initialize(self):

        try:
            if SentenceTransformer is None:
                print(
                    "RAG warning: sentence-transformers is not installed."
                )
                return

            self.model = SentenceTransformer(
                self.model_name
            )

        except Exception as exc:
            print(
                "RAG model initialization warning:",
                exc
            )
            self.model = None
            return

        self.load_documents()

        if self.documents:
            self.build_index()

    # =========================================================
    # LOAD KNOWLEDGE
    # =========================================================

    def load_documents(self):

        self.documents = []

        if not os.path.exists(
            self.knowledge_path
        ):
            print(
                "RAG warning: knowledge directory not found:",
                self.knowledge_path
            )
            return

        files = glob.glob(
            os.path.join(
                self.knowledge_path,
                "*.txt"
            )
        )

        for file_path in files:

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    text = file.read().strip()

                if not text:
                    continue

                chunks = self.chunk_text(text)

                for chunk in chunks:

                    self.documents.append(
                        {
                            "text": chunk,
                            "source": os.path.basename(
                                file_path
                            )
                        }
                    )

            except Exception as exc:

                print(
                    "RAG document warning:",
                    file_path,
                    exc
                )

        print(
            "\nKnowledge chunks:",
            len(self.documents)
        )

    # =========================================================
    # CHUNKING
    # =========================================================

    @staticmethod
    def chunk_text(
        text,
        chunk_size=700,
        overlap=100
    ):

        words = text.split()

        if not words:
            return []

        chunks = []

        start = 0

        while start < len(words):

            end = min(
                start + chunk_size,
                len(words)
            )

            chunk = " ".join(
                words[start:end]
            )

            if chunk.strip():
                chunks.append(chunk)

            if end >= len(words):
                break

            start = max(
                0,
                end - overlap
            )

        return chunks

    # =========================================================
    # BUILD VECTOR INDEX
    # =========================================================

    def build_index(self):

        if not self.documents:
            print(
                "RAG: No knowledge documents found."
            )
            return False

        if self.model is None:
            print(
                "RAG: Embedding model unavailable."
            )
            return False

        if faiss is None:
            print(
                "RAG: FAISS is not installed."
            )
            return False

        try:

            texts = [
                document["text"]
                for document in self.documents
            ]

            self.embeddings = self.model.encode(
                texts,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

            dimension = self.embeddings.shape[1]

            self.index = faiss.IndexFlatIP(
                dimension
            )

            self.index.add(
                self.embeddings.astype(
                    "float32"
                )
            )

            print(
                "Vector index created."
            )

            print(
                "Embedding dimension:",
                dimension
            )

            return True

        except Exception as exc:

            print(
                "RAG index creation warning:",
                exc
            )

            self.index = None

            return False

    # =========================================================
    # SEMANTIC SEARCH
    # =========================================================

    def search(
        self,
        query,
        top_k=3
    ):

        if not query:
            return []

        if self.model is None:
            return []

        if self.index is None:

            if not self.build_index():
                return []

        try:

            top_k = max(
                1,
                min(
                    int(top_k),
                    len(self.documents)
                )
            )

            query_embedding = self.model.encode(
                [str(query)],
                convert_to_numpy=True,
                normalize_embeddings=True
            )

            scores, indices = self.index.search(
                query_embedding.astype(
                    "float32"
                ),
                top_k
            )

            results = []

            for score, index in zip(
                scores[0],
                indices[0]
            ):

                if index < 0:
                    continue

                if index >= len(
                    self.documents
                ):
                    continue

                document = self.documents[index]

                results.append(
                    {
                        "source":
                            document["source"],

                        "score":
                            round(
                                float(score),
                                4
                            ),

                        "text":
                            document["text"]
                    }
                )

            return results

        except Exception as exc:

            print(
                "RAG search warning:",
                exc
            )

            return []

    # =========================================================
    # CONTEXT
    # =========================================================

    def build_context(
        self,
        query,
        top_k=3
    ):

        results = self.search(
            query,
            top_k
        )

        context_parts = []

        for result in results:

            context_parts.append(
                f"""
SOURCE: {result['source']}
RELEVANCE: {result['score']}

{result['text']}
""".strip()
            )

        context = "\n\n".join(
            context_parts
        )

        return context, results


# =============================================================
# PIPELINE COMPATIBILITY ALIAS
# =============================================================

AdvancedSemanticRAG = AdvancedRAG


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("CAMPUS360 ADVANCED SEMANTIC RAG")
    print("=" * 60)

    rag = AdvancedRAG()

    query = (
        "The office campus has unusually high "
        "energy consumption. HVAC efficiency "
        "appears poor and the forecast shows "
        "increasing demand. What should facility "
        "operators investigate?"
    )

    context, results = rag.build_context(
        query,
        top_k=3
    )

    print("\nQUERY:")
    print(query)

    print("\nRETRIEVED EVIDENCE:")

    for result in results:

        print(
            f"\nSource: {result['source']}"
        )

        print(
            f"Similarity: {result['score']}"
        )

        print(
            result["text"][:500]
        )

    print("\nEvidence count:")
    print(len(results))

    print("=" * 60)
    print("ADVANCED RAG TEST COMPLETE")
    print("=" * 60)