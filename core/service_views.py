from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Service
from core.service_serializers import serialize_service


def _published_queryset():
    return (
        Service.objects.filter(is_published=True)
        .prefetch_related("deliverables", "process_steps", "use_cases", "faqs", "media")
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def public_services_list(request):
    services = _published_queryset()
    return Response([serialize_service(service, request) for service in services])


@api_view(["GET"])
@permission_classes([AllowAny])
def public_service_detail(request, slug):
    try:
        service = _published_queryset().get(slug=slug)
    except Service.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(serialize_service(service, request))
