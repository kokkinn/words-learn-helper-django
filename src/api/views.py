from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import WordSerializer
from words.models import Word


@login_required
@api_view(['GET'])
def getData(request):
    user = request.user
    words = user.words.all()
    
    serializer = WordSerializer(words, many=True)
    return Response(serializer.data)
