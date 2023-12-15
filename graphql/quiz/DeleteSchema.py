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
        fields = ("id","title","category")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title","quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question","answer_text")


# compulsory to have in order to create objects and retrive them
class Query(graphene.ObjectType):

    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())
    all_quizzes = DjangoListField(QuizzesType) 

    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)

    def resolve_all_quizzes(root, info):
        return Quizzes.objects.all()



# ============================================================
#                  Delete Operations 
# ============================================================

class CategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        print("IN the deletion")
        category = Category.objects.get(id=id)
        category.delete()

        return f"deleted Object {id}"


class QuizMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    quiz = graphene.Field(QuizzesType)

    @classmethod
    def mutate(cls, root, info, id):
        quiz_obj = Quizzes.objects.get(id=id)
        quiz_obj.delete()
        return None


class QuestionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    question = graphene.Field(QuestionType)

    @classmethod
    def mutate(cls, root, info, id):
        print("\n**********in the deletion of quesiton...*************")
        question_obj = Question.objects.get(id=id)
        question_obj.delete()
        return 'hi deleted question'


class AnswerMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    answer = graphene.Field(AnswerType)

    @classmethod
    def mutate(cls, root, info, id):
        answer_obj = Answer.objects.get(id=id)
        answer_obj.delete()
        return None



class Mutation(graphene.ObjectType):
    delete_category = CategoryMutation.Field()
    delete_quiz     = QuizMutation.Field()
    delete_question = QuestionMutation.Field()
    delete_answer   = AnswerMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)



'''
#===================== Exmaple ======================

mutation deleteCategory {
    deleteCategory(id: 9) {
    category {
        id
        }
    }
}


mutation {
  deleteQuestion(id: 6) {
    question {
      __typename
    }
  }
}

'''