import graphene
import event_app.schema as app_schema


class Query(app_schema.Query, graphene.ObjectType):
    # Combine the queries from different apps
    pass


class Mutation(app_schema.Mutation, graphene.ObjectType):
    # Combine the mutations from different apps
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)