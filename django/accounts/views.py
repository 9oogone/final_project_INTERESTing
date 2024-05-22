from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def charge_cash(request):
    try:
        amount = int(request.data.get('amount'))  # 정수로 변환
    except (TypeError, ValueError):
        return Response({'error': 'Invalid amount'}, status=400)

    if amount <= 0:
        return Response({'error': 'Amount must be greater than zero'}, status=400)

    user = request.user
    user.cash += amount
    user.save()

    return Response({'message': 'Cash charged successfully', 'amount': amount})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_nickname(request):
    new_nickname = request.data.get('nickname')
    if not new_nickname:
        return Response({"error": "Nickname is required"}, status=400)

    user = request.user
    user.nickname = new_nickname
    user.save()

    return Response({"success": "Nickname changed successfully"}, status=200)
