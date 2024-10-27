from django.urls import path
from candidate.views import CandidateListCreateView, CandidateDetailView, CandidateSearchView

urlpatterns = [
    path('candidates/', CandidateListCreateView.as_view(), name='candidate-list-create'),
    path('candidates/<int:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),
    path('candidates/search/', CandidateSearchView.as_view(), name='candidate-search'),
]


# search API request url format -- /api/candidates/search/?q=first_name+middle_name+last_name
