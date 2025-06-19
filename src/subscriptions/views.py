from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from subscriptions.models import SubscriptionPrice,UserSubscription
import helper.billing
from subscriptions import utils as sub_utils

@login_required
def user_subscription_view(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    if request.method =="POST":
        print("refresh sub")
        finished = sub_utils.refresh_active_users_subscriptions(user_ids=[request.user.id],active_only=False)
        if finished:
            messages.success(request, "Your Plan Has Been refreshed")
        else:
            messages.error(request,"Your Plan Have Not Been refreshed, Please Try Again")
        return redirect(user_sub_obj.get_absolute_url())

    return render(request,'subscriptions/user_detail_view.html',{"subscription":user_sub_obj})

@login_required
def user_subscription_cancel_view(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    if request.method =="POST":
        if user_sub_obj.stripe_id and user_sub_obj.is_active_status:
            sub_data = helper.billing.cancel_subscription(user_sub_obj.stripe_id,
                                                          reason="User wanted to end",
                                                          feedback="other",
                                                          cancel_at_period_end=True,
                                                          raw=False)
            for k,v in sub_data.items():
                setattr(user_sub_obj,k,v)
            user_sub_obj.save()
            print("DEBUG SUB DATA:", sub_data)
            print("AFTER CANCEL:", user_sub_obj.serialize())

            messages.success(request,"Your Plan Has Been Cancelled")
        return redirect(user_sub_obj.get_absolute_url())

    return render(request,'subscriptions/user_cancel_view.html',{"subscription":user_sub_obj})

# Create your views here.
def subscription_price_view(request, interval = "month"):
    qs = SubscriptionPrice.objects.filter(featured=True)
    inv_mo = SubscriptionPrice.IntervalChoices.MONTHLY
    inv_yr = SubscriptionPrice.IntervalChoices.YEARLY
    monthly_qs = qs.filter(interval = SubscriptionPrice.IntervalChoices.MONTHLY)
    yearly_qs = qs.filter(interval=SubscriptionPrice.IntervalChoices.YEARLY)
    object_list = qs.filter(interval = inv_mo)
    url_path_name = "pricing_interval"
    mo_url = reverse(url_path_name,kwargs={"interval":inv_mo})
    yr_url = reverse(url_path_name,kwargs={"interval": inv_yr})
    active= inv_mo
    if interval == inv_yr:
        active = inv_yr
        object_list = qs.filter(interval=inv_yr)
    return render(request,"subscriptions/pricing.html",{"object_list":object_list,"mo_url":mo_url,"yr_url":yr_url,"active":active,})