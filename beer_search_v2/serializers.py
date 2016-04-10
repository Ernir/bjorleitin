from rest_framework import routers, serializers, viewsets
from beer_search_v2.models import Product


class ATVRProductSerializer(serializers.HyperlinkedModelSerializer):
    container = serializers.StringRelatedField(
            read_only=True,
    )

    class Meta:
        model = Product
        fields = ("name", "price", "volume", "product_id", "container")


class ATVRProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("container").filter(source=0).all()
    serializer_class = ATVRProductSerializer


router = routers.DefaultRouter()
router.register(r"products", ATVRProductViewSet)
