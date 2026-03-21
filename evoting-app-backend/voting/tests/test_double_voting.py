import os
import django
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from accounts.models import VoterProfile
from elections.models import VotingStation, Poll, Position, PollPosition, Candidate
from voting.services import VoteCastingService
from voting.models import Vote
from datetime import date, timedelta

User = get_user_model()

class DoubleVotingTestCase(TestCase):
    def setUp(self):
        self.station = VotingStation.objects.create(
            name="Test Station", location="Loc", capacity=100
        )
        self.user = User.objects.create_user(
            username="voter@test.com", email="voter@test.com", password="password123",
            role=User.Role.VOTER, is_verified=True
        )
        self.profile = VoterProfile.objects.create(
            user=self.user, national_id="NID123", date_of_birth=date(2000, 1, 1),
            gender="M", station=self.station
        )
        self.poll = Poll.objects.create(
            title="General Election", election_type="General",
            start_date=date.today(), end_date=date.today() + timedelta(days=1),
            status=Poll.Status.OPEN
        )
        self.poll.stations.add(self.station)
        self.pos = Position.objects.create(title="President", level="National")
        self.pp = PollPosition.objects.create(poll=self.poll, position=self.pos)
        self.candidate = Candidate.objects.create(
            full_name="Candidate A", national_id="CID1", date_of_birth=date(1980, 1, 1),
            gender="M", party="Party A", education="Bachelors"
        )
        self.pp.candidates.add(self.candidate)
        self.service = VoteCastingService()

    def test_voter_cannot_vote_twice(self):
        vote_data = {
            "poll_id": self.poll.id,
            "votes": [{"poll_position_id": self.pp.id, "candidate_id": self.candidate.id}]
        }
        # First vote
        self.service.cast(self.user, vote_data)
        
        # Second vote should fail
        with self.assertRaises(ValidationError) as cm:
            self.service.cast(self.user, vote_data)
        self.assertEqual(cm.exception.detail[0], "You have already voted in this poll.")
