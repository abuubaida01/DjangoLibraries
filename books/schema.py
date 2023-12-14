import graphene 
from graphene_django import DjangoObjectType
from .models import Books

# this is much like serializer
class BooksType(DjangoObjectType):
  class Meta:
    model = Books
    fields = ('id', 'title', 'excerpt')



# this will generate queries 
class Query(graphene.ObjectType):
  all_books = graphene.List(BooksType)

  # for getting all objects
  def resolve_all_books(root, info):
    return Books.objects.all()

  # for getting filtered objects 
  def resolve_all_books(root, info):
    return Books.objects.filter(title='Django')



# define Schema
schema = graphene.Schema(query=Query)