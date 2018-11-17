import factory
import factory.fuzzy
import factory.django
from django.contrib.auth.models import User
from django.db.models.signals import post_save


@factory.django.mute_signals(post_save)
class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'billjobs.UserProfile'
        django_get_or_create = ('user',)

    billing_address = factory.Faker('address')
    user = factory.SubFactory(
            'billjobs.tests.factories.UserFactory', profile=None)


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'steve'
    password = 'gates'
    first_name = 'Steve'
    last_name = 'Gates'
    email = 'steve.gates@billjobs.org'
    userprofile = factory.RelatedFactory(UserProfileFactory, 'user')


class SuperUserFactory(UserFactory):
    username = 'bill'
    password = 'jobs'
    first_name = 'Bill'
    last_name = 'Jobs'
    email = 'bill.jobs@billjobs.org'
    is_staff = True
    is_superuser = True


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'billjobs.Service'

    reference = factory.Sequence(lambda n: 'SE%03d' % n)
    name = factory.fuzzy.FuzzyText()
    price = factory.fuzzy.FuzzyInteger(100, 200, 10)


class BillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'billjobs.Bill'

    user = factory.SubFactory(UserFactory)
    amount = factory.fuzzy.FuzzyInteger(100, 200, 10)
