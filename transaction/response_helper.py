from rest_framework import status
from rest_framework.response import Response

class ResponseHelper:

    def get_status_404(self, msg="Not found"):
        message = {"data": {}, "message": msg, "status": status.HTTP_404_NOT_FOUND}
        return Response(message, status=status.HTTP_404_NOT_FOUND)

    def get_status_500(self, msg="Internal Server Error", data=None):
        if data is None:
            data = {}
        message = {"data": data, "message": msg, "status": status.HTTP_500_INTERNAL_SERVER_ERROR}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_status_200(self, msg="ok", data=None):
        if data is None:
            data = {}
        message = {"data": data, "message": msg, "status": status.HTTP_200_OK}
        return Response(message, status=status.HTTP_200_OK)

    def get_status_422(self, msg="data not as per requirement", data=None):
        if data is None:
            data = {}
        message = {"data": data, "message": msg, "status": status.HTTP_422_UNPROCESSABLE_ENTITY}
        return Response(message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_status_201(self, msg="success", data=None):
        if data is None:
            data = {}
        message = {"data": data, "message": msg, "status": status.HTTP_201_CREATED}
        return Response(message, status=status.HTTP_201_CREATED)

    def get_status_409(self, msg="CONFLICT"):
        message = {"data": {}, "message": msg, "status": status.HTTP_409_CONFLICT}
        return Response(message, status=status.HTTP_409_CONFLICT)