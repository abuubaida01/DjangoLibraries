from django.urls import path 
from graphene_django.views import GraphQLView
from .GetSchema import schema as GetSchema
from .PostSchema import schema as PostSchema
from .PutSchema import schema as PutSchema
from .DeleteSchema import schema as DeleteSchema


urlpatterns = [
    path('graphql/get/', GraphQLView.as_view(graphiql=True, schema=GetSchema)),
    path('graphql/post/', GraphQLView.as_view(graphiql=True, schema=PostSchema)),
    path('graphql/put/', GraphQLView.as_view(graphiql=True, schema=PutSchema)),
    path('graphql/del/', GraphQLView.as_view(graphiql=True, schema=DeleteSchema)),

]
