import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Quizzes, Category, Question, Answer

# they define the relationship btw model and schema
# they convert models into the schema format
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id","name")

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id","title","category","quiz")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title","quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question","answer_text")

class Query(graphene.ObjectType):

    # graphene file, will only return individual field by query that defines on the client
    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    
    # here we will get the list of fields DListField is similar to graphene.list
    all_answers = graphene.List(AnswerType, id=graphene.Int())
    all_quizzes = DjangoListField(QuizzesType) 

    # here root is some sort of entry point, and INfo is the query information
    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)

    def resolve_all_quizzes(root, info):
      return Quizzes.objects.all()

schema = graphene.Schema(query=Query)


'''
# How to write queries in the graphql: 

Query: 
  {
    allQuizzes{
      title
    }
  }

Answer: 
{
  "data": {
    "allQuizzes": [
      {
        "title": "Django Quize"
      },
      {
        "title": "React Quiz"
      },
    ]
  }
}

                =====================================

Query 2: 
{
  allQuestions(id:4){
    title
  }
  allAnswers(id:4){
    answerText
  }
}

Answer:
{
  "data": {
    "allQuestions": {
      "title": "What is Java"
    },
    "allAnswers": [
      {
        "answerText": "Java is the Old Backend Framework"
      }
    ]
  }
}

                =====================================

Query 3 Styling in the Query

query DynamicName($id: Int=1){
  allQuestions(id:$id){
    title
  }
  allAnswers(id:$id){
    answerText
  }
}

Answer:
{
  "data": {
    "allQuestions": {
      "title": "What is Java"
    },
    "allAnswers": [
      {
        "answerText": "Java is the Old Backend Framework"
      }
    ]
  }
}
'''
