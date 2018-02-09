from django.db import models
from .videos import Video
from .actions import Action
from .terms import Term


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.ForeignKey(
        'Gender',
        on_delete=models.CASCADE
        )
    age = models.ForeignKey(
        'Age',
        on_delete=models.CASCADE
        )
    education = models.ForeignKey(
        'Education',
        on_delete=models.CASCADE
        )
    occupation = models.ForeignKey(
        'Occupation',
        on_delete=models.CASCADE
        )
    country = models.ForeignKey(
        'Country',
        on_delete=models.CASCADE
        )
    video = models.ManyToManyField(Video, through="VideoWatched")
    score = models.ManyToManyField(Term, through="UserContentScore")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def get_user_vector(self):
        user_content_score = UserContentScore.objects.filter(user_id=self.id).order_by('term_id')

        num_terms = Term.objects.count()

        # Force evaluate queryset for fast .score
        len(user_content_score)
        user_vector = [None] * num_terms

        for ii in range(num_terms):
            user_vector[ii] = float(user_content_score[ii].score)

        return user_vector


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend")

    class Meta:
        verbose_name = "Friend"
        verbose_name_plural = "Friends"

    def __str__(self):
        return "user %s is friend with user %s" % (self.user, self.friend)


class VideoWatched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    liked = models.IntegerField()
    time_watched = models.DateTimeField(auto_now=True)
    interactions = models.ManyToManyField(Action, through="VideoInteractions")

    class Meta:
        verbose_name = "VideoWatched"
        verbose_name_plural = "VideosWatched"

    def __str__(self):
        return "user %s watched video %s" % (self.user, self.video)


class VideoInteractions(models.Model):
    video_watched = models.ForeignKey(VideoWatched, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    content_id = models.CharField(null=True, max_length=150)
    video_time = models.IntegerField(null=True)
    explicit_rf = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    time_action_performed = models.DateTimeField(auto_now=True)
    computed = models.BooleanField(default=0)

    class Meta:
        verbose_name = "VideoInteractions"
        verbose_name_plural = "VideosInteractions"

    def __str__(self):
        return "Action %s to video" % self.action


class UserContentScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=6, decimal_places=3)

    class Meta:
        verbose_name = "UserContentScore"
        verbose_name_plural = "UserContentScores"

    def __str__(self):
        return "Score for user %s on term %s is %f" % (self.user.username, self.term.term, self.score)

