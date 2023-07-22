from logging import getLogger
from authapis.serializers import SignInRequestSerializer, TokenResponseSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from authapis.services.signin_service import SignInService
from drf_yasg.utils import swagger_auto_schema
from authapis.helpers import CustomExceptionHandler
from authapis.status_code import generic_error_2
from rest_framework.permissions import AllowAny

logger = getLogger("django")


class SignInView(GenericAPIView):
    serializer_class = SignInRequestSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
    responses={"200": TokenResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        logger.info("request: %s", request.body)
        status_code = 200
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid()
            response = SignInService(**serializer.data).get_user_token()
        except CustomExceptionHandler as e:
            logger.exception(f"exception CustomExceptionHandler {e}")
            response, status_code = e.detail, e.status_code
        except Exception as e:
            logger.exception(f"exception {e}")
            response, status_code = generic_error_2, 500
            
        logger.debug("response: %s", response)
        return Response(response, status=status_code)
