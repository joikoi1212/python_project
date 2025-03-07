from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _t
from django.utils.translation import gettext as _t2
from account.models import CustomUser

# Create your models here.

EXTERNAL_ID_MAXLENGTH = 255
EXTERNAL_API_URL_MAXLENGTH = 2000
EXTERNAL_STYLE_MAXLENGTH = 2000
PLAN_CHOICE_MAX_LEN = 255
PLAN_CHOICE_DESC_MAX_LEN = 300
SUBSCRIPTION_COST_MAX_DIGITS = 5

class PlanChoices(models.model):
      plan = models.CharField(
          max_lengtyh = 2,
          unique = True,
          blank = False,
          verbose_name = _t('Plan code'),
      )
      name = models.CharField(max_length = PLAN_CHOICE_MAX_LEN, unique = True, blank = False, verbose_name = _t('Plan name'))
      
      const = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_t('Cost'))
      
      is_active = models.BooleanField(default=False)
      date_added = models.DateTimeField(default=timezone.now)
      date_changed = models.DateTimeField(default=timezone.now)
      description1 = models.CharField(
          max_length=PLAN_CHOICE_DESC_MAX_LEN, verbose_name=_t('Plan description 1:')
      )
      description2 = models.CharField(
          max_length=PLAN_CHOICE_DESC_MAX_LEN, verbose_name=_t('Plan description 2:')
      )
      external_plan = models.CharField(
            max_length=EXTERNAL_ID_MAXLENGTH, unique = True, verbose_name=_t('External Plan ID')
      ) 
      external_api_url = models.CharField(
            max_length=EXTERNAL_API_URL_MAXLENGTH, unique = True, verbose_name=_t('External API URL')
      ) 
      external_style_json = models.CharField(
            max_length=EXTERNAL_STYLE_MAXLENGTH, unique = True, verbose_name=_t('External style JSON')
      ) 
      
      def __str__(self) -> str:
        return f"{str(self.name)} subscription"
    
      @classmethod
      async def afrom_plan_code(cls, plan_code: str) -> 'PlanChoices':
        return await PlanChoices.objects.aget(plan_code=plan_code)
      
      @classmethod
      def from_plan_code(cls, plan_code: str) -> 'PlanChoices':
        return PlanChoices.objects.get(plan_code=plan_code)
    

class Subscription (models.Model):
    class Plan_Choices(models.TextChoices):
        STANDARD = 'ST', _t('Standard Plan')
        PREMIUM = 'PR', _t('Premium Plan')

    plan = models.CharField(max_length=2, choices = PlanChoices, default=PlanChoices.STANDARD)
    
    const = models.DecimalField(max_digits=SUBSCRIPTION_COST_MAX_DIGITS, decimal_places=2, verbose_name=_t('Plan Cost'))
    
    date_subscribed = models.DateTimeField(default=timezone.now)
    
    payment_provider_id = models.CharField(
        max_length = EXTERNAL_ID_MAXLENGTH, verbose_name=_t('Payment provider id')
    )
    
    is_active = models.BooleanField(default=False)
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        plan_choice = Subscription.PlanChoices(self.plan)
        return f'{self.user.first_name} {self.user.last_name}: {plan_choice.label} {_t2("Subscription")}'