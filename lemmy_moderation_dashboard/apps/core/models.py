from lemmy_moderation_dashboard.apps.lemmy_0_18 import models as lemmy_models


class LocalUser(lemmy_models.LocalUser):
    class Meta:
        proxy = True


class Person(lemmy_models.Person):
    class Meta:
        proxy = True


class Instance(lemmy_models.Instance):
    class Meta:
        proxy = True


class Comment(lemmy_models.Comment):
    class Meta:
        proxy = True
