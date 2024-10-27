from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from candidate.models import Candidate
from candidate.serializers import CandidateSerializer
from candidate.candidate_search import CandidateSearchService

class CandidateListCreateView(APIView):
    """
    View to create a candidate and list all candidates.
    """

    def get(self, request):
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateDetailView(APIView):
    """
    View to retrieve, update, and delete a candidate.
    """

    def get_object(self, pk):
        try:
            return Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            return None

    def get(self, request, pk):
        candidate = self.get_object(pk)
        if candidate is None:
            return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data)

    # def put(self, request, pk):
    #     candidate = self.get_object(pk)
    #     if candidate is None:
    #         return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = CandidateSerializer(candidate, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        candidate = self.get_object(pk)
        if candidate is None:
            return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CandidateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        candidate = self.get_object(pk)
        if candidate is None:
            return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)
        candidate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CandidateSearchView(APIView):
    """
    View to search candidates based on relevancy in their names.
    """

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({"error": "Search query is required."}, status=status.HTTP_400_BAD_REQUEST)

        candidates = CandidateSearchService.search_candidates(query)
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
