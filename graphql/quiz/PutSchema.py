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
#                  CRUD Operations 
# ============================================================

class CategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name 
        category.save()

        return CategoryMutation(category=category)

'''
mutation{
    updateCategory(id:10, name:"Theory"){
        category{
        name
        }
    }
}
'''

class QuizMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        id = graphene.ID()


    quiz = graphene.Field(QuizzesType)

    @classmethod
    def mutate(cls, root, info, title, id):
        # Create and save the Quiz instance
        quiz_obj = Quizzes.objects.get(id=id)
        quiz_obj.title = title
        quiz_obj.save()
        return QuizMutation(quiz=quiz_obj)

"""
mutation{
        updateQuiz(id:4, title:"New Java Quiz"){
        quiz{
        title
        }
    }
}
"""

class QuestionMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        technique = graphene.Int(required=False)
        difficulty = graphene.Int(required=False)
        id = graphene.ID(required=True)

    question = graphene.Field(QuestionType)

    @classmethod
    def mutate(cls, root, info, title, technique, difficulty, id):
        # Create and save the Question instance
        question_obj = Question.objects.get(id=id)
        question_obj.title = title
        question_obj.technique = technique if technique else question_obj.technique
        question_obj.difficulty = difficulty if difficulty else question_obj.difficulty
        question_obj.save()
        return QuestionMutation(question=question_obj)
'''
mutation{
    updateQuestion(difficulty:1, technique:2, title:"HOw to find names", id:7){
        question{
        title
        }
    }
}
'''



class AnswerMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        answer_text = graphene.String(required=True)

    answer = graphene.Field(AnswerType)

    @classmethod
    def mutate(cls, root, info, id, answer_text):
        answer_obj = Answer.objects.get(id=id)
        answer_obj.answer_text = answer_text
        answer_obj.save()
        return AnswerMutation(answer=answer_obj)
'''
mutation{
    updateAnswer(id:4, answerText:"Answer is Abu-Ubaida"){
        answer{
        answerText
        }
    }
}
'''


class Mutation(graphene.ObjectType):
    update_category =  CategoryMutation.Field()
    update_quiz = QuizMutation.Field()
    update_question = QuestionMutation.Field()
    update_answer = AnswerMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)



'''
#===================== Exmaple ======================
'''