import strawberry
from strawberry.asgi import GraphQL

from apps.mastermind.infrastructure.graphql.mutations import Mutation
from apps.mastermind.infrastructure.graphql.queries import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)
