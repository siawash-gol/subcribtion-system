from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime as dt, timedelta
from django.utils.timezone import now
from django.utils.text import slugify
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=155, db_index=True)
    complete = models.BooleanField(default=False)
    publish = models.DateField(auto_now_add=True)
    desc = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Plan(models.Model):
    PERIOD_DURATION = (
        ('minutes', 'minutes'),
        ('days', 'days'),
        ('weeks', 'weeks'),
        ('months', 'months'),
    )

    class PlanTypeChoices(models.TextChoices):
        FREE = 'Free'
        PLAN_MONTH_ONE = 'Plan Month One'
        PLAN_MONTH_TWO = 'Plan Month Two'
        PLAN_YEAR_ONE = 'Plan Year One'

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    plan = models.CharField(max_length=100, choices=PlanTypeChoices.choices, default=PlanTypeChoices.FREE)
    slug = models.SlugField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.ManyToManyField('PlanFeatures', related_name='plan_features')
    duration = models.PositiveIntegerField(default=7)
    duration_period = models.CharField(max_length=64, choices=PERIOD_DURATION)

    def __str__(self):
        return f"{self.plan}"

    @property
    def get_features(self):
        return [
            {
                "name": feature.title,
                "description": feature.description
            }
            for feature in self.features.all()
        ]

    @property
    def get_duration(self):
        return f"{self.duration} {self.duration_period}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.plan}-{self.category.name}")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'


class PlanFeatures(models.Model):
    title = models.CharField(max_length=155)
    description = models.CharField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Plan Feature'
        verbose_name_plural = 'Plan Features'


class UserPlan(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name='user_plan')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, related_name='user_plan', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.BooleanField(default=False)
    currency = models.CharField(max_length=5, default="USD")  # Default currency
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.plan.plan}"

    def get_features(self):
        return self.plan.get_features if self.plan else []

    class Meta:
        verbose_name = 'User Plan'
        verbose_name_plural = 'User Plans'


@receiver(post_save, sender=UserPlan)
def create_subscription(sender, instance, created, **kwargs):
    if instance and instance.status:
        expires_in = now() + timedelta(days=instance.plan.duration)
        Subscription.objects.update_or_create(
            user_plan=instance,
            defaults={"expires_in": expires_in}
        )


class Subscription(models.Model):
    user_plan = models.ForeignKey(UserPlan, on_delete=models.CASCADE, related_name='subscriptions')
    expires_in = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_plan.user.username} - {self.user_plan.plan.plan}"

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'


class PlanDiscount(models.Model):
    occasion = models.CharField(max_length=255, default='No occasion')
    for_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    expires_in = models.DateTimeField(null=True)

    def __str__(self):
        return self.occasion

    class Meta:
        verbose_name = 'Plan Discount'
        verbose_name_plural = 'Plan Discounts'


class DiscountCode(models.Model):
    code = models.CharField(max_length=32, unique=True)
    occasion = models.CharField(max_length=255, default='No occasion')
    for_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    expires_in = models.DateTimeField(null=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Discount Code'
        verbose_name_plural = 'Discount Codes'


class UsedDiscountCode(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True)
    used_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Used Discount Code'
        verbose_name_plural = 'Used Discount Codes'
        unique_together = ('user', 'discount_code')
