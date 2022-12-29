import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types

from apps.auth.infrastructure.graphql.context import Context
from apps.auth.infrastructure.graphql.mutations import AuthMutations
from apps.mastermind.infrastructure.graphql.mutations import MastermindMutations
from apps.mastermind.infrastructure.graphql.queries import MastermindQueries


Query = merge_types("Query", (MastermindQueries,))

Mutation = merge_types("Mutation", (MastermindMutations, AuthMutations))

schema = strawberry.Schema(query=Query, mutation=Mutation)


async def get_context() -> Context:
    return Context()


graphql_app = GraphQLRouter(schema, context_getter=get_context, path="/")
