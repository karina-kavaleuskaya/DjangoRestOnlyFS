from rest_framework import serializers, generics
from only_app.models import Category, Product, Stock, Discount, ProductImage


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class CreatorProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', )


class CreatorProductSerializer(serializers.ModelSerializer):
    images = CreatorProductImageSerializer(many=True, source='productimage_set')

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'images')




class ProductCreateSerializer(serializers.ModelSerializer):
    images = CreatorProductImageSerializer(many=True, source='productimage_set')

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('productimage_set', [])
        product = Product.objects.create(**validated_data)

        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

        return product


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_path = representation['image']
        parts = image_path.rsplit('/', 1)
        representation['image'] = parts[0] + '/blur_' + parts[1]
        return representation


class BlurredProductImageSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(source='*')

    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductBlurredSerializer(serializers.ModelSerializer):
    images = BlurredProductImageSerializer(many=True, source='productimage_set')
    result_price = serializers.SerializerMethodField()

    def get_result_price(self, obj):
        price = obj.price
        discount = obj.discount

        if discount:
            discount_percent = discount.percent
            price = price * (100 - discount_percent) / 100

        return price

    class Meta:
        model = Product
        fields = ['id', 'name', 'result_price', 'images']


class StockSerializer(serializers.ModelSerializer):
    product = CreatorProductSerializer()

    class Meta:
        model = Stock
        fields = ['id', 'product']