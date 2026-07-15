from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    about_description = models.TextField(blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return f"Profile of {self.user.email}"


class PersonaSection(models.Model):
    heading = models.CharField(max_length=255)
    description = models.TextField()
    image_role_label = models.CharField(max_length=120, default="AI Automation Engineer")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "persona section"
        verbose_name_plural = "persona section"

    def __str__(self):
        return self.heading


class PhilosophyParagraph(models.Model):
    order = models.PositiveIntegerField(default=0)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "philosophy paragraph"
        verbose_name_plural = "philosophy paragraphs"

    def __str__(self):
        return f"Paragraph {self.order}"


class TechnicalSkill(models.Model):
    order = models.PositiveIntegerField(default=0)
    skill_id = models.CharField(max_length=10)
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=200)
    proficiency = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=20, default="#a855f7")
    icon = models.CharField(max_length=50, default="Bot")
    tags = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "technical skill"
        verbose_name_plural = "technical skills"

    def __str__(self):
        return f"{self.skill_id} — {self.title}"


class Project(models.Model):
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    short_description = models.TextField()
    architectural_vision = models.TextField()
    tags = models.JSONField(default=list, blank=True)
    icon = models.CharField(max_length=50, default="Activity")
    color = models.CharField(max_length=20, default="#a855f7")
    featured = models.BooleanField(default=False)
    timeline = models.CharField(max_length=100)
    lead_role = models.CharField(max_length=150)
    environment = models.CharField(max_length=150)
    goal = models.TextField()
    result = models.TextField()
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-year", "id"]
        verbose_name = "project"
        verbose_name_plural = "projects"

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="projects/")
    order = models.PositiveIntegerField(default=0)
    alt_text = models.CharField(max_length=200, blank=True, default="")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "project image"
        verbose_name_plural = "project images"

    def __str__(self):
        return f"{self.project.title} image #{self.order}"
