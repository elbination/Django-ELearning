from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from slugify import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from .fields import OrderField


def get_current_timestamp():
    ct = datetime.now()
    result = round(ct.timestamp())
    return result


# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=500, unique=True, editable=False)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + '-' + str(get_current_timestamp()))
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Order for a new module will be assigned by adding 1 to the last module
    # of the same Course object
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    # Limit the ContentType objects that can be used for the generic relation
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file'
                                     )})
    object_id = models.PositiveIntegerField()
    # Retrieve or set the related object directly
    # Built on top of the two other fields
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


# No database associated with the ItemBase model
# since it's an abtract model
class ItemBase(models.Model):
    # $(class)s_related => each child model will be generated automatically
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    # Rendering a template and returning the rendered content as a string
    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self}
        )


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
