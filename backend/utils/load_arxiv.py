import arxiv

class ArxivLoader:
    def __init__(self, query: str, max_results: int = 3):
        self.query = query
        self.max_results = max_results

    def load(self, print_results: bool = False):
        """
        Load papers from arXiv based on the provided query.
        Args:
            print_results (bool): If True, prints the results to the console.
        Returns:
            List[Dict]: A list of dictionaries containing paper details.
        """
        if not self.query:
            raise ValueError("Query must be provided to load papers from arXiv.")
        
        if self.max_results <= 0:
            raise ValueError("max_results must be a positive integer.")
        
        if print_results:
            print(f"Loading papers from arXiv with query: {self.query} and max_results: {self.max_results}")
        # Perform the search on arXiv
        search = arxiv.Search(
            query=self.query,
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for result in search.results():
            results.append({
                "title": result.title,
                "summary": result.summary,
                "authors": [author.name for author in result.authors],
                "published": result.published,
                "pdf_url": result.pdf_url
            })

        if print_results:
            if not results:
                print("No results found for the given query.")
                return results
            for idx, paper in enumerate(results):
                print(f"Paper {idx + 1}:")
                print(f"Title: {paper['title']}")
                print(f"Authors: {', '.join(paper['authors'])}")
                print(f"Published: {paper['published']}")
                print(f"Summary: {paper['summary']}\n")
                print(f"PDF URL: {paper['pdf_url']}\n")
            
        
        return results