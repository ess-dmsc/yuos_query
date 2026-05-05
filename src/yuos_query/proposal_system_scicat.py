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
                url,
                headers=headers,
                proxies=self.proxies,
                timeout=10.0,
                verify=True,
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

    def _extract_sample_name(self, sample: dict) -> str:
        return (
            sample.get("sampleId")
            or sample.get("_id")
            or sample.get("description", "")
        )

    def _extract_samples(self, prop: dict) -> list:
        return [
            SampleInfo(name=self._extract_sample_name(s))
            for s in prop.get("samples", [])
        ]

    def get_proposals_for_instrument(self, name: str) -> Dict[str, ProposalInfo]:
        """
        Fetch proposals for a given instrument from SciCat, including samples.

        :param name: The short name of the instrument.
        :return: Dictionary of ProposalInfo objects keyed by proposal ID.
        """
        instrument_id = self._get_instrument_id(name)

        filter_query = json.dumps({
            "where": {"instrumentIds": instrument_id},
            "include": [{"relation": "samples"}],
        })
        proposals_data = self._execute_get(
            f"/api/v3/proposals?filters={quote(filter_query)}"
        )

        result = {}
        for prop in proposals_data:
            prop_id = prop.get("proposalId", "")
            pi_first = prop.get("pi_firstname", "").strip()
            pi_last = prop.get("pi_lastname", "").strip()
            proposer = User(
                pi_first,
                pi_last,
                self._generate_fed_id(pi_first, pi_last),
                "",
            )
            result[prop_id] = ProposalInfo(
                id=prop_id,
                title=prop.get("title", ""),
                proposer=proposer,
                users=[],
                db_id=0,
                samples=self._extract_samples(prop),
            )

        return result

    def get_proposal_by_id(self, proposal_id: str) -> Optional[ProposalInfo]:
        """
        Fetch a single proposal by its ID from SciCat.

        :param proposal_id: The proposal ID to look up.
        :return: ProposalInfo if found, None otherwise.
        """
        filter_query = json.dumps({
            "where": {"proposalId": proposal_id},
            "include": [{"relation": "samples"}],
        })
        proposals_data = self._execute_get(
            f"/api/v3/proposals?filters={quote(filter_query)}"
        )

        if not proposals_data:
            return None

        prop = proposals_data[0]
        prop_id = prop.get("proposalId", "")

        pi_first = prop.get("pi_firstname", "").strip()
        pi_last = prop.get("pi_lastname", "").strip()
        proposer = User(
            pi_first,
            pi_last,
            self._generate_fed_id(pi_first, pi_last),
            "",
        )

        return ProposalInfo(
            id=prop_id,
            title=prop.get("title", ""),
            proposer=proposer,
            users=[],
            db_id=0,
            samples=self._extract_samples(prop),
        )
