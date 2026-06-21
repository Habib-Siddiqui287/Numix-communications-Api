from rest_framework import serializers
import phonenumbers

class DialingSerializer(serializers.Serializer):
    phone_number = serializers.CharField(help_text="The dial numbers string sequence")
    country_code = serializers.CharField(max_length=2, help_text="ISO 2-letter Country code format (e.g. PK or US)")

    def validate(self, data):
        number_str = data.get('phone_number')
        country_iso = data.get('country_code').upper()
        
        try:
            # Parse number structure matching target geographic criteria
            parsed_number = phonenumbers.parse(number_str, country_iso)
            
            # Check length and format rules mapping constraints
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("ALARM: Wrong Number! Invalid for this country.")
                
        except Exception:
            raise serializers.ValidationError("ALARM: Wrong Number! Format is unrecognizable.")
            
        return data