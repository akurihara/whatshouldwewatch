class ParticipantNotPartOfElectionError(Exception):
    message = "The participant is not part of the election."


class CandidateAlreadyExistsError(Exception):
    message = "A candidate for the movie provided already exists."
