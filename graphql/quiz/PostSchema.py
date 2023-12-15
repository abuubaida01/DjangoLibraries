import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Quizzes, Category, Question, Answer
from django.shortcuts import get_object_or_404

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


# ============================================================
#                  CRUD Operations 
# ============================================================

class CategoryMutation(graphene.Mutation):
  class Arguments:
    name = graphene.String(required=True)

  category = graphene.Field(CategoryType)

  @classmethod
  def mutate(cls, root, info, name):
    category = Category.objects.create(name=name)
    category.save()
    return CategoryMutation(category=category)

'''
    mutation{
      createCategory(name:"DadaJan"){
        category{
          name
        }
      }
    }
'''


class QuizMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        category = graphene.ID()

    quiz = graphene.Field(QuizzesType)

    @classmethod
    def mutate(cls, root, info, title, category):
        # Create and save the Quiz instance
        category = get_object_or_404(Category,id=category)
        quiz_obj = Quizzes(title=title, category=category)
        quiz_obj.save()
        return QuizMutation(quiz=quiz_obj)


'''
mutation{
  createQuiz(category:3, title:"This is new Quiz"){
    quiz{
      title
    }
  }
}
'''



class QuestionMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        quiz = graphene.ID(required=True)
        technique = graphene.Int(required=False)
        difficulty = graphene.Int(required=False)

    question = graphene.Field(QuestionType)

    @classmethod
    def mutate(cls, root, info, title, quiz, technique, difficulty):
        # Create and save the Question instance
        quiz = Quizzes.objects.get(id=quiz)
        question_obj = Question(title=title, quiz=quiz, technique=technique, difficulty=difficulty)
        question_obj.save()
        return QuestionMutation(question=question_obj)

'''
mutation{
  createQuestion(difficulty:1, technique:1, quiz:2, title:"What is your name?"){
    question{
      title
    }
  }
}
'''



class AnswerMutation(graphene.Mutation):
    class Arguments:
        question = graphene.Int(required=True)
        answer_text = graphene.String(required=True)

    answer = graphene.Field(AnswerType)

    @classmethod
    def mutate(cls, root, info, question, answer_text):
        question = Question.objects.get(id=question)
        answer_obj = Answer(question=question, answer_text=answer_text)
        answer_obj.save()
        return AnswerMutation(answer=answer_obj)
'''
mutation{
  createAnswer(answerText:"I know the answer!", question:7){
    answer{
      answerText
    }
  }
}
'''


class Mutation(graphene.ObjectType):
  create_category =  CategoryMutation.Field()
  create_quiz = QuizMutation.Field()
  create_question = QuestionMutation.Field()
  create_answer = AnswerMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

