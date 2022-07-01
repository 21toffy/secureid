
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import RegisterSerializer, ChangePasswordSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.shortcuts import get_object_or_404

from rest_framework_jwt.settings import api_settings
from rest_framework import status, generics
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated






class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            request.data['email']
            request.data['password']
        except LookupError as e:
            return Response(data={"code":status.HTTP_400_BAD_REQUEST , "status": "failed" ,"message":"{} field missing".format(e)}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email']
        if email is None:
            return Response({'error': 'Empty Email field'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = CustomUser.objects.get(email=email)
            if not user.check_password(request.data['password']):
                return Response(data={"code":status.HTTP_400_BAD_REQUEST , "status": "failed" ,"message":"Incorrect Email or password"}, status=status.HTTP_400_BAD_REQUEST)

            token, created = Token.objects.get_or_create(user=user)

            return Response(data = {"token": token.key, "user":RegisterSerializer(user,
                        context={'request': request}).data, "status": "success", "code":status.HTTP_201_CREATED }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(data={"code":status.HTTP_400_BAD_REQUEST , "status": "failed" ,"message":"User not found"}, status=status.HTTP_400_BAD_REQUEST)




class RegisterView(APIView):
    # queryset = CustomUser.objects.all()
    # permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"code":status.HTTP_201_CREATED , "status": "success" ,"message":"user Created"}, status=status.HTTP_201_CREATED)
        return Response(data={"code":status.HTTP_400_BAD_REQUEST , "status": "failed" ,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = CustomUser
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            print(self.get_object())
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response(data={"code":status.HTTP_400_BAD_REQUEST , "status": "failed" ,"message":"wrong password"}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





{
"email":"oketofoke@gmail.com",
"password":"toffy123"}





{
"email":"okedeji@yaoo.com",
"first_name": "tofunmi",
"last_name": "okedjie",
"password":"tofunklmkpdmdmmi"

}


{
"old_password":"jbiewjfneof",
"new_password": "ndwfnwfnwfni"
}




{
"email":"okedeji@yaoo.com",
"password":"tofunklmkpdmdmmi"
}




{
"email":"okedeji@yaoo.com",
"first_name": "tofunmi",
"last_name": "okedjie",
"password":"tofunklmkpdmdmmi"

}



{
"email":"okedeji@yaoo.com",
"password":"mdkmdkmdk"
}


{
"email":"okedeji@mail.com",
"password":"mdkmdkmdk"
}