from brainly_api import BrainlyGraphQLAPI, Market, str_to_graphql_id
from .entities import GQLQuestion, Question


class BrainlyAPI:
    _api: BrainlyGraphQLAPI

    def __init__(self, token: str, host: str):
        self._api = BrainlyGraphQLAPI(
            market=Market.RU,
            token=token,
            host=host
        )

    async def get_question(self, id: int) -> Question | None:
        response = await self._api.query("""
            query GetQuestion($questionId: ID!) {
                question(id: $questionId) {
                    created
                    content
                    answers {
                      nodes {
                        created
                      }
                    }
                    subject {
                      name
                    }
                }
            }
            """, variables={
            "questionId": str_to_graphql_id(f"question:{id}")
        })

        question = response.data["question"]

        if question is None:
            return None

        return GQLQuestion.from_dict(question)
