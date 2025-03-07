from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user
from common.auth import aclient_required
from common.django_utils import arender
from .models import Subscription
from django.core.exceptions import ObjectDoesNotExist
from writer.models import Article
# Create your views here.

# async def dashboard(request: HttpRequest) -> HttpResponse:
#    return render(request, 'client/dashboard.html')
PlanChoices = Subscription.PlanChoices

@aclient_required
async def dashboard(request: HttpRequest) -> HttpResponse:
    user = await aget_user(request)
    subscription_plan = "No subscription yet"  # Define before try-except
    
    try:
        subscription = await Subscription.objects.aget(user=user, is_active=True)
        plan = PlanChoices(subscription.plan)
        subscription_plan = plan.label
    except ObjectDoesNotExist:
        pass  # No need to redefine, it defaults to "No subscription yet"

    context = {'subscription_plan': subscription_plan}
    return await arender(request, 'client/dashboard.html', context)

@aclient_required
async def browse_articles(request: HttpRequest) -> HttpResponse:
        user = await aget_user(request)
        subscription = None
        try:
                subscription = await Subscription.objects.aget(user = user, is_active = True)
                plan = PlanChoices(subscription.plan)
                if plan == PlanChoices.STANDARD:
                        articles = Article.objects.filter(is_premium = False)
                else:
                        articles = Article.objects.all()
        except ObjectDoesNotExist:
                articles = []
        
      
        context = {'has_subscription': subscription is not None, 'articles': articles}
        return await arender(request, 'client/browse-articles.html', context)
    

@aclient_required
async def subscribe_plan(request: HttpRequest) -> HttpResponse:
       return await arender(request, "client/subscribe-plan.html")      

@aclient_required
async def update_client(request: HttpRequest) -> HttpResponse:
        user = await aget_user(request)
        subscription = None
        try:
                subscription = await Subscription.objects.aget(user = user, is_active = True)
        except ObjectDoesNotExist:
                pass
        context = {'subscription': subscription is not None}
        return await arender(request, 'client/update-client.html', context)
 
@aclient_required
async def create_subscription(request: HttpRequest, sub_id: int, plan: str) -> HttpResponse:
        plan_choice = PlanChoices(plan)
        user = await aget_user(request)
        await Subscription.objects.acreate(const = '3.00' if plan_choice == PlanChoices.STANDARD else '9.00', plan=plan_choice.value, payment_provider_id=sub_id, user=user, is_active=True)
        context = {"subscription": plan_choice.label}
        return await arender(request, 'client/create-subscription.html', context)