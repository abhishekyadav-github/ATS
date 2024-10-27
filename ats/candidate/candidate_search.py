# recruiter/services.py
from django.db.models import Q, Count, Case, When, IntegerField, Value
from candidate.models import Candidate

class CandidateSearchService:
    @staticmethod
    def search_candidates(query: str):
        search_terms = query.split()
        filters = Q()
        
        for term in search_terms:
            filters |= Q(name__icontains=term)

        relevancy = sum(
            Case(When(name__icontains=term, then=Value(1)), output_field=IntegerField()) 
            for term in search_terms
        )
        
        return (
            Candidate.objects
            .filter(filters)
            .annotate(relevancy=relevancy)
            .order_by('-relevancy')
        )
