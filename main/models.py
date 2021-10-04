from django.db import models
from django.contrib.auth import get_user_model

from versatileimagefield.fields import VersatileImageField, PPOIField
User = get_user_model()

STATUS_CHOICES = (
    ('open', 'Открытое'),
    ('closed', 'Закрытое'),
    ('draft', 'Черновик'),
)


class Publication(models.Model):
    title = models.CharField('Тема', max_length=255)
    text = models.TextField('Описание')
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='pubs', verbose_name='Автор')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата редактирования', auto_now=True)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return f'Id{self.user}:{self.title}'


class Comment(models.Model):
    publication = models.ForeignKey(Publication,
                                    on_delete=models.CASCADE,
                                    related_name='comments', verbose_name='Публикация')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Автор')
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.publication} --> {self.user}'


class PublicationImage(models.Model):
    picture = models.ImageField(upload_to='images', null=True, blank=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='img')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


""""""""""""""""""""""""""""""


class Message(models.Model):
    sender = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='sender',  verbose_name='Отправитель')
    receiver = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='receiver', verbose_name='Получатель')
    message = models.CharField(max_length=1200,  verbose_name='Сообщение')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp', )


class UserPublicationRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Like'),
        (2, 'Funny'),
        (3, 'Tears'),
        (4, 'Angry'),
        (5, 'Sad')
    )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Comment,
                                on_delete=models.CASCADE)
    like = models.ManyToManyField(User,related_name='likes')
    favorite = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.user}: {self.product}, RATE{self.rate}'


class Favorite(models.Model):
    product = models.ForeignKey(Publication,
                                on_delete=models.CASCADE, related_name='publication')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, related_name='user_publication')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created', 'id', )


class PublicationLikes(models.Model):
    like_users = models.ManyToManyField(User)
    like_publication = models.ForeignKey(Publication,
                                         on_delete=models.CASCADE,
                                         null=True, related_name='like_publication')
