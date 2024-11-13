from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=500)
    options = models.JSONField()  # Store options as JSON
    correct_option = models.CharField(max_length=100)  # Store the correct option

    def __str__(self):
        return self.question_text


# Model to represent coding questions
class CodingQuestion(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    constraints = models.TextField()
    example_input = models.TextField()
    example_output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Model to represent test cases for a question
class TestCase(models.Model):
    question = models.ForeignKey(CodingQuestion, related_name='test_cases', on_delete=models.CASCADE)
    input_data = models.TextField()
    expected_output = models.TextField()
    is_public = models.BooleanField(default=False)  # Public test cases are visible to users

    def __str__(self):
        return f"Test Case for {self.question.title}"


# Model to represent user submissions
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(CodingQuestion, related_name='submissions', on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50, choices=[('Python', 'Python'), ('Java', 'Java'), ('C++', 'C++')])
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user.username} for {self.question.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    solved_questions = models.ManyToManyField(CodingQuestion, blank=True)
    # New fields
    first_name = models.CharField(max_length=30, blank=True)  # Add first_name field
    email = models.EmailField(blank=True)  # Optional, since user already has an email
    age = models.PositiveIntegerField(null=True, blank=True)  # Age field
    learning_style = models.CharField(max_length=50, blank=True)  # Preferred learning style
    education_level = models.CharField(max_length=50, blank=True)  # Education level
    interests = models.JSONField(default=list, blank=True)  # List of interests
    goals = models.JSONField(default=list, blank=True)  # List of goals
    is_setup = models.BooleanField(default=False)  # Profile setup status

    avatar = models.ImageField(default='profile_images/default.png', upload_to='profile_images')
    bio = models.TextField(blank=True)  # Make bio optional

    def __str__(self):
        return self.user.username
