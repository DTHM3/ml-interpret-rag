import sentence_transformers

class Embedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = sentence_transformers.SentenceTransformer(model_name)

    def embed(self, texts):
        """
        Embed a list of texts using the specified model.
        
        :param texts: List of strings to embed.
        :return: List of embeddings.
        """
        return self.model.encode(texts, convert_to_tensor=True)