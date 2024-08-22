# Generated by Django 5.1 on 2024-08-22 21:10

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("title", models.CharField(max_length=200, null=True)),
                ("code", models.CharField(max_length=200, null=True, unique=True)),
                ("credit", models.IntegerField(default=0, null=True)),
                ("summary", models.TextField(blank=True, max_length=200, null=True)),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("Bachelor", "Bachelor Degree"),
                            ("Master", "Master Degree"),
                        ],
                        max_length=25,
                        null=True,
                    ),
                ),
                (
                    "year",
                    models.IntegerField(
                        choices=[
                            (1, "1"),
                            (2, "2"),
                            (3, "3"),
                            (4, "4"),
                            (5, "5"),
                            (6, "6"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "semester",
                    models.CharField(
                        choices=[
                            ("First", "First"),
                            ("Second", "Second"),
                            ("Third", "Third"),
                        ],
                        max_length=200,
                    ),
                ),
                (
                    "is_elective",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Program",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150, unique=True)),
                ("summary", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="CourseAllocation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "courses",
                    models.ManyToManyField(
                        related_name="allocated_course", to="course.course"
                    ),
                ),
                (
                    "lecturer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="allocated_lecturer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.session",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Module",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="modules",
                        to="course.course",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="course",
            name="program",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="course.program"
            ),
        ),
        migrations.CreateModel(
            name="Upload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                (
                    "file",
                    models.FileField(
                        upload_to="course_files/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                [
                                    "pdf",
                                    "docx",
                                    "doc",
                                    "xls",
                                    "xlsx",
                                    "ppt",
                                    "pptx",
                                    "zip",
                                    "rar",
                                    "7zip",
                                ]
                            )
                        ],
                    ),
                ),
                ("updated_date", models.DateTimeField(auto_now=True, null=True)),
                ("upload_time", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.course"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UploadVideo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("slug", models.SlugField(blank=True, unique=True)),
                (
                    "video",
                    models.FileField(
                        upload_to="course_videos/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"]
                            )
                        ],
                    ),
                ),
                ("summary", models.TextField(blank=True, null=True)),
                ("duration", models.DurationField(null=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.course"
                    ),
                ),
                (
                    "documents",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lesson_documents",
                        to="course.upload",
                    ),
                ),
                (
                    "module",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="course.module",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PracticalAssessment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=200, null=True)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("template_code", models.TextField(blank=True, null=True)),
                ("solution_code", models.TextField(blank=True, null=True)),
                ("instructions", models.TextField(blank=True, null=True)),
                ("timer", models.DurationField(blank=True, null=True)),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.uploadvideo",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code_main", models.TextField(blank=True, null=True)),
                ("code_test", models.TextField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("submitted", models.BooleanField(default=False)),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.uploadvideo",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProgress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("completed", models.BooleanField(default=False)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.course"
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.uploadvideo",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("language", models.CharField(max_length=20)),
                ("code_main", models.TextField(blank=True, null=True)),
                ("code_test", models.TextField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "name")},
            },
        ),
    ]
