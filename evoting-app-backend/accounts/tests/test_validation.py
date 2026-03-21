from django.test import TestCase
from rest_framework.exceptions import ValidationError
from accounts.serializers import VoterRegistrationSerializer
from datetime import date, timedelta
from elections.models import VotingStation

class ValidationEdgeCasesTestCase(TestCase):
    def setUp(self):
        self.station = VotingStation.objects.create(name="S1", location="L1", capacity=10)

    def test_age_calculation_edge_cases(self):
        today = date.today()
        # Exactly 18 today
        dob_18 = today.replace(year=today.year - 18)
        # 1 day under 18
        dob_under = dob_18 + timedelta(days=1)
        
        data_18 = {
            "full_name": "Test User", "national_id": "N1", "date_of_birth": dob_18,
            "gender": "M", "address": "Addr", "phone": "123", "email": "a@b.com",
            "station_id": self.station.id, "password": "pass123", "confirm_password": "pass123"
        }
        serializer = VoterRegistrationSerializer(data=data_18)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        data_under = data_18.copy()
        data_under["date_of_birth"] = dob_under
        data_under["national_id"] = "N2"
        data_under["email"] = "c@d.com"
        serializer = VoterRegistrationSerializer(data=data_under)
        self.assertFalse(serializer.is_valid())
        self.assertIn("You must be at least 18 years old.", str(serializer.errors))

    def test_email_uniqueness(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create_user(username="dup@test.com", email="dup@test.com", password="pass")
        
        data = {
            "full_name": "Test User", "national_id": "N3", "date_of_birth": "2000-01-01",
            "gender": "M", "address": "Addr", "phone": "123", "email": "dup@test.com",
            "station_id": self.station.id, "password": "pass123", "confirm_password": "pass123"
        }
        serializer = VoterRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("A user with this email already exists.", str(serializer.errors))
