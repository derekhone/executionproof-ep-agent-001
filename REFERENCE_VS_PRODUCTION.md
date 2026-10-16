### Reference vs. Production

This repository publishes research/reference material or public integration interfaces; its specific scope is below. It does not ship RF's private production backend. Experimental behavior, fixture policies, local/test keys and published results apply only to the identified implementation and stated conditions. Do not use public test keys as production trust roots or treat fixture conformance as proof of production security. This notice does not change existing licenses, results, preregistrations or preserved failures.

This public packet supplies integration adapters, contracts, fixtures and results. The controlled reference verifier is identified in EXECUTIONPROOF_PIN.md but is not shipped here. The existing README, pin, contract, fixtures, result stores and manifests are preserved unchanged. This additive notice is outside the historical research manifest.

### API route scope — do not assume aliases

| Surface | Published verification route | Scope |
|---|---|---|
| Builder site and VaultProof client | `POST /v2/verify` | Advertised/client-default route; workflow/proposed_action/actor/context payload. |
| ExecutionProof OpenAPI | `POST /v2/boundaries/{boundaryId}/verify` | Published boundary-scoped specification with its own request/response schema. |
| EP-AGENT controlled reference verifier | `POST /verify` | Frozen research contract only; not a production endpoint alias. |

These paths and payloads are not proven interchangeable. A URL-only substitution is not a compatibility fix. Before integration, obtain the deployment-specific versioned contract from RF, including route, request/response fields and authentication requirements. Until that contract is confirmed, do not infer a canonical deployed route or silently rewrite client requests. This clarification does not change runtime behavior, the OpenAPI specification or historical reference contracts.
