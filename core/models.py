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
    job_title = models.CharField(max_length=200, default="AI Automation Engineer")
    hero_heading = models.CharField(max_length=500, default="Engineering Agentic Intelligence")
    hero_description = models.TextField(
        blank=True,
        default="Merging backend precision with agentic AI to build systems that reason, retrieve, and act.",
    )
    resume_summary = models.TextField(blank=True, default="")
    status_text = models.CharField(max_length=100, default="AI Automation Engineer")
    location_label = models.CharField(max_length=100, default="PK // REMOTE")
    stack_label = models.CharField(max_length=200, default="Django • Next.js • Gemini")
    contact_email = models.EmailField(blank=True, default="")
    whatsapp_url = models.CharField(max_length=500, blank=True, default="")
    github_url = models.CharField(max_length=500, blank=True, default="")
    linkedin_url = models.CharField(max_length=500, blank=True, default="")
    cv_file = models.FileField(upload_to="cvs/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return f"Profile of {self.user.email}"


class TechnicalSkill(models.Model):
    order = models.PositiveIntegerField(default=0)
    skill_id = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, default="smart_toy")
    tags = models.JSONField(default=list, blank=True)
    details = models.TextField(blank=True, default="")
    mastery = models.PositiveSmallIntegerField(default=80)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "technical skill"
        verbose_name_plural = "technical skills"

    def __str__(self):
        return f"{self.skill_id} — {self.title}"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("AI Agents", "AI Agents"),
        ("Backend", "Backend"),
        ("Automation", "Automation"),
    ]

    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="AI Agents")
    short_description = models.TextField()
    full_description = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    goal = models.TextField(blank=True, default="")
    result = models.TextField(blank=True, default="")
    architecture = models.JSONField(default=list, blank=True)
    pipeline_steps = models.JSONField(default=list, blank=True)
    metrics = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-year", "id"]
        verbose_name = "project"
        verbose_name_plural = "projects"

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
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


class EducationItem(models.Model):
    order = models.PositiveIntegerField(default=0)
    period = models.CharField(max_length=50)
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    tags = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "education item"
        verbose_name_plural = "education items"

    def __str__(self):
        return f"{self.institution} — {self.degree}"


class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    label = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "social link"
        verbose_name_plural = "social links"

    def __str__(self):
        return f"{self.platform}: {self.label}"


class HeroMetric(models.Model):
    order = models.PositiveIntegerField(default=0)
    value = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    color = models.CharField(max_length=20, blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "hero metric"
        verbose_name_plural = "hero metrics"

    def __str__(self):
        return f"{self.value} — {self.label}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, default="")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "contact message"
        verbose_name_plural = "contact messages"

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
