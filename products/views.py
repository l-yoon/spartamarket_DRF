from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response   
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductSerializer

# 글 추가, 리스트 뷰 
class ProductListView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()

    def post(self, request):
        permission_classes = [IsAuthenticated]
        
        title = request.data.get("title")
        content = request.data.get("content")
        image = request.data.get("image")
        
        # 현재 유저 작성자로 설정
        product = Product.objects.create(
            title=title, 
            content=content, 
            image=image, 
            author=request.user
        )
    
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=201)

# 특정 글 수정, 삭제
class ProductDetailView(APIView):
    def get(self, request, productId):
        product = get_object_or_404(Product, id=productId)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, productId):
        product = get_object_or_404(Product, id=productId)

        # 작성자만 수정 가능
        if product.author != request.user:
            return Response({"error": "작성자가 일치하지 않습니다."}, status=403)
        
        # 업테이트
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, productId):
        product = get_object_or_404(Product, id=productId)

        # 작성자만 글 삭제 가능
        if product.author != request.user:
            return Response({"error": "작성자가 일치하지 않습니다."}, status=403)

        product.delete()
        return Response({"detail": "게시글이 삭제되었습니다."}, status=204)