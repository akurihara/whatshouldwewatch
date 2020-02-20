from django.urls import reverse
from rest_framework.test import APITestCase

from whatshouldwewatch.elections.models import Candidate, Election, Participant
from whatshouldwewatch.movies import constants as movie_constants
from whatshouldwewatch.movies.models import Movie
from whatshouldwewatch.users.models import Device


class TestElectionsView(APITestCase):
    def setUp(self):
        self.url = reverse("elections")

    def tearDown(self):
        Participant.objects.all().delete()
        Election.objects.all().delete()
        Device.objects.all().delete()

    def test_post_initiates_election(self):
        device = Device.objects.create(device_token="some-device-token")
        initiator_name = "John"
        election_description = "This is a test description."
        data = {
            "election_description": election_description,
            "initiator_name": initiator_name,
        }
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        response = self.client.post(self.url, data=data, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIsNotNone(response_json["id"])
        external_id = response_json["id"]

        # Verify election in database.
        election = Election.objects.filter(external_id=external_id).first()
        self.assertIsNotNone(election)
        self.assertEqual(election.description, election_description)

        # Verify participant in database.
        self.assertEqual(election.participants.count(), 1)
        participant = election.participants.first()
        self.assertEqual(participant.name, initiator_name)
        self.assertTrue(participant.is_initiator)

    def test_post_creates_device_if_none_exists(self):
        initiator_name = "John"
        election_description = "This is a test description."
        data = {
            "election_description": election_description,
            "initiator_name": initiator_name,
        }
        device_token = "new-device-token"
        headers = {"HTTP_X_DEVICE_ID": device_token}

        response = self.client.post(self.url, data=data, format="json", **headers)

        # Verify response.
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIsNotNone(response_json["id"])

        # Verify device in database.
        device = Device.objects.filter(device_token=device_token).first()
        self.assertIsNotNone(device)

    def test_post_returns_error_when_election_description_is_missing(self):
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        response = self.client.post(
            self.url, data={"iniator_name": "John"}, format="json", **headers
        )

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(
            response_json["error"], "Missing parameter: `election_description`."
        )

    def test_post_returns_error_when_initiator_name_is_missing(self):
        device = Device.objects.create(device_token="some-device-token")
        headers = {"HTTP_X_DEVICE_ID": device.device_token}

        response = self.client.post(
            self.url,
            data={"election_description": "This is a test description."},
            format="json",
            **headers
        )

        # Verify response.
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json["error"], "Missing parameter: `initiator_name`.")


class TestCandidatesView(APITestCase):
    def setUp(self):
        self.url = reverse("candidates")

    def tearDown(self):
        Candidate.objects.all().delete()
        Participant.objects.all().delete()
        Election.objects.all().delete()
        Device.objects.all().delete()
        Movie.objects.all().delete()

    def post_create_candidate(self):
        # Set up election
        election = Election.objects.create(description="test", external_id="abc123")
        device = Device.objects.create(device_token="abc123")
        participant = Participant.objects.create(
            name="John", election=election, device=device, is_initiator=True
        )
        movie = Movie.objects.create(
            provider_slug=movie_constants.MOVIE_PROVIDER_THE_MOVIE_DB,
            provider_id="abc123",
        )

        response = self.client.post(
            self.url, data={"movie_id": movie.id}, format="json"
        )

        # Verify response.
        self.assertEqual(response.status_code, 200)

        # Verify candidate in database.
        self.assertEqual(participant.candidates.count(), 1)
        candidate = participant.candidates.first()
        self.assertEqual(candidate.movie_id, movie.id)