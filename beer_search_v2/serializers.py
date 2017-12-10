from rest_framework import routers, serializers, viewsets
from beer_search_v2.models import Product, ATVRProduct, UntappdEntity


class ATVRProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ATVRProduct
        fields = ("name", "price", "volume", "atvr_id", "container")


class UntappdEntitySerializer(serializers.HyperlinkedModelSerializer):
    brewery = serializers.StringRelatedField()
    style = serializers.StringRelatedField()

    class Meta:
        model = UntappdEntity
        fields = ("untappd_id", "brewery", "style", "rating", "logo_url", "untappd_name")


class ATVRProductViewSet(viewsets.ModelViewSet):
    queryset = ATVRProduct.objects.all()
    serializer_class = ATVRProductSerializer


class UntappdEntryViewSet(viewsets.ModelViewSet):
    queryset = UntappdEntity.objects.prefetch_related("style", "style__simplifies_to", "brewery").all()
    serializer_class = UntappdEntitySerializer


router = routers.DefaultRouter()
router.register(r"products", ATVRProductViewSet)
router.register(r"untappd-entries", UntappdEntryViewSet)
