from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product 
from .serializers import ProductSerializer

class ProductListView(APIView):
    def post(self, request):
        title = request.data.get( "title")
        content = request.data.get( "content")
        product = Product.objects.create(title=title, content=content)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)