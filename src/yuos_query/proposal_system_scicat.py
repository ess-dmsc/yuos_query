import json
import requests
from typing import Dict, Optional
from urllib.parse import quote, urljoin

from yuos_query.data_classes import ProposalInfo, SampleInfo, User
from yuos_query.exceptions import (
    ConnectionException,
    InvalidTokenException,
    ServerException,
    UnknownInstrumentException,
)


class ProposalRequester:
    """
    SciCat REST implementation of ProposalRequester.
    Acts as a drop-in replacement for the GraphQL-based ProposalRequester.
    """

    def __init__(self, url: str, token: str, proxies: dict):
        self.url = url
        self.token = token
        self.proxies = proxies

    def _execute_get(self, endpoint: str):
        try:
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            }
            url = urljoin(self.url, endpoint)
            response = requests.get(
                url, headers=headers, proxies=self.proxies, verify=True
            )
            if response.status_code in (401, 403):
                raise InvalidTokenException("Invalid or missing token")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            raise ServerException(error) from error
        except requests.exceptions.RequestException as error:
            raise ConnectionException(error) from error

    def _get_instrument_id(self, name: str) -> str:
        data = self._execute_get("/api/v3/instruments")
        for inst in data:
            # SciCat stores 'User Office Short Code' in customMetadata, or fallback to 'name'
            short_code = (
                inst.get("customMetadata", {})
                .get("User Office Short Code", {})
                .get("value")
            )
            if not short_code:
                short_code = inst.get("name")

            if short_code and str(short_code).lower() == name.lower():
                # Prefer 'id', fallback to '_id' or 'pid'
                return inst.get("id") or inst.get("_id") or inst.get("pid")

        raise UnknownInstrumentException(f"Unknown instrument {name}")

    def _generate_fed_id(self, firstname: str, lastname: str) -> str:
        return f"{firstname}{lastname}".lower()

    def get_proposals_for_instrument(self, name: str) -> Dict[str, ProposalInfo]:
        """
        Fetch proposals for a given instrument from SciCat.

        :param name: The short name of the instrument.
        :return: Dictionary of ProposalInfo objects keyed by proposal ID.
        """
        instrument_id = self._get_instrument_id(name)

        # 1. Fetch proposals for the instrument
        filter_query = json.dumps({"where": {"instrumentIds": instrument_id}})
        encoded_filter = quote(filter_query)
        proposals_endpoint = f"/api/v3/proposals?filters={encoded_filter}"
        proposals_data = self._execute_get(proposals_endpoint)

        result = {}
        for prop in proposals_data:
            prop_id = prop.get("proposalId", "")
            title = prop.get("title", "")
            print(f"Processing proposal: {prop.get('proposalId', 'N/A')}")

            # Proposer
            # pi_first = prop.get("pi_firstname", "").strip()
            pi_first = prop.get("pi_firstname", "").strip()
            pi_last = prop.get("pi_lastname", "").strip()
            # SciCat doesn't currently provide institution, defaulting to empty string
            pi_institution = ""
            proposer = User(
                pi_first,
                pi_last,
                self._generate_fed_id(pi_first, pi_last),
                pi_institution
            )

            # Co-proposers (Empty response for now as requested)
            users = []

            # 2. Fetch samples for each proposal
            sample_filter = json.dumps({"where": {"proposalId": prop_id}})
            sample_encoded_filter = quote(sample_filter)
            samples_endpoint = f"/api/v3/samples?filter={sample_encoded_filter}"
            samples_data = self._execute_get(samples_endpoint)

            samples = []
            for sample in samples_data:
                sample_name = sample.get("description", "")
                samples.append(SampleInfo(name=sample_name))

            # Database ID (mapping SciCat's _id to db_id)
            # SciCat exposes id as a string, dropping into db_id as 0 since data_classes expects int
            # and the system mostly relies on the string `id` properties.
            db_id = 0

            result[prop_id] = ProposalInfo(
                id=prop_id,
                title=title,
                proposer=proposer,
                users=users,
                db_id=db_id,
                samples=samples
            )

        return result

    def get_proposal_by_id(self, proposal_id: str) -> Optional[ProposalInfo]:
        """
        Fetch a single proposal by its ID from SciCat.

        :param proposal_id: The proposal ID to look up.
        :return: ProposalInfo if found, None otherwise.
        """
        filter_query = json.dumps({"where": {"proposalId": proposal_id}})
        encoded_filter = quote(filter_query)
        proposals_data = self._execute_get(
            f"/api/v3/proposals?filters={encoded_filter}"
        )

        if not proposals_data:
            return None

        prop = proposals_data[0]
        prop_id = prop.get("proposalId", "")
        title = prop.get("title", "")

        pi_first = prop.get("pi_firstname", "").strip()
        pi_last = prop.get("pi_lastname", "").strip()
        proposer = User(
            pi_first,
            pi_last,
            self._generate_fed_id(pi_first, pi_last),
            "",
        )

        sample_filter = json.dumps({"where": {"proposalId": prop_id}})
        sample_encoded_filter = quote(sample_filter)
        samples_data = self._execute_get(
            f"/api/v3/samples?filter={sample_encoded_filter}"
        )
        samples = [
            SampleInfo(name=s.get("description", "")) for s in samples_data
        ]

        return ProposalInfo(
            id=prop_id,
            title=title,
            proposer=proposer,
            users=[],
            db_id=0,
            samples=samples,
        )
