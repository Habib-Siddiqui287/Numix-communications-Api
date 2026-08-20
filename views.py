import json
import phonenumbers
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny


from .models import CallLog, MessageLog

def home_frontend(request):
    return render(request, 'index.html')


@method_decorator(csrf_exempt, name='dispatch')
class DialNumberView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone_number = request.data.get('phone_number', request.data.get('number', '')).strip()
        
        if not phone_number or phone_number in ["Dial Number...", "Target Number..."]:
            return Response({"non_field_errors": ["Please enter a valid number first."]}, status=status.HTTP_400_BAD_REQUEST)
        
        # Cleanup for prefix validation
        clean_digits = phone_number.replace('+', '').strip()

        # Assignment Country Matrix
        prefixes = {
            "92": "PK", "03": "PK", "3": "PK",
            "1": "US", "44": "UK", "91": "IN", 
            "966": "SA", "971": "AE"
        }

        matched_region = "Unknown"
        for prefix, region in prefixes.items():
            if clean_digits.startswith(prefix) and len(clean_digits) >= 3:
                matched_region = region
                break

        is_valid_number = False
        country_iso = matched_region
        
        try:
            formatted_num = phone_number if phone_number.startswith('+') else '+' + phone_number
            parsed_number = phonenumbers.parse(formatted_num, None)
            
            if phonenumbers.is_possible_number(parsed_number) and matched_region != "Unknown":
                country_iso = phonenumbers.region_code_for_number(parsed_number) or matched_region
                is_valid_number = True
        except Exception:
            if matched_region != "Unknown" and len(clean_digits) >= 10:
                is_valid_number = True

        # Determine Final Status
        final_status = "Correct" if is_valid_number else "Wrong"

        CallLog.objects.create(
            phone_number=phone_number,
            status=final_status,
            country=country_iso
        )

        if is_valid_number:
            return Response({
                "status": "success",
                "message": f"Transmission routed successfully to {country_iso} region!"
            }, status=status.HTTP_200_OK)
        
        
        return Response({
            "non_field_errors": ["Invalid Number Structure / Destination Unreachable"]
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LogMessageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        target_number = request.data.get('target_number', '').strip()
        message_payload = request.data.get('message_payload', '').strip()

        if not target_number or target_number in ["Target Number...", "Dial Number..."]:
            return Response({"non_field_errors": ["Target phone number missing."]}, status=status.HTTP_400_BAD_REQUEST)

        clean_digits = target_number.replace('+', '').strip()

        prefixes = {
            "92": "PK", "03": "PK", "3": "PK",
            "1": "US", "44": "UK", "91": "IN", 
            "966": "SA", "971": "AE"
        }

        matched_region = "Unknown"
        for prefix, region in prefixes.items():
            if clean_digits.startswith(prefix) and len(clean_digits) >= 3:
                matched_region = region
                break

        is_valid_number = False
        country_iso = matched_region

        try:
            formatted_num = target_number if target_number.startswith('+') else '+' + target_number
            parsed_number = phonenumbers.parse(formatted_num, None)
            if phonenumbers.is_possible_number(parsed_number) and matched_region != "Unknown":
                country_iso = phonenumbers.region_code_for_number(parsed_number) or matched_region
                is_valid_number = True
        except Exception:
            if matched_region != "Unknown" and len(clean_digits) >= 10:
                is_valid_number = True

        final_status = "Correct" if is_valid_number else "Wrong"

    
        MessageLog.objects.create(
            target_number=target_number,
            message_payload=message_payload,
            status=final_status,
            country=country_iso
        )

        if is_valid_number:
            return Response({
                "status": "success",
                "message": "Message Dispatched successfully!"
            }, status=status.HTTP_200_OK)

        return Response({
            "non_field_errors": ["Invalid Number Structure / Message Delivery Failed"]
        }, status=status.HTTP_400_BAD_REQUEST)