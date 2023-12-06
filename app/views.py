from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from . models import Product,Customer,Cart,Payment,OrderPlaced,Favour
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import random
import razorpay
from django.conf import settings


# Create your views here.


def hello(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(Favour.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())

def men(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(Favour.objects.filter(user=request.user))
    return render(request,'app/men.html')



def drop(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(Favour.objects.filter(user=request.user))

    return render(request,"app/women.html",locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem=0

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem=len(Favour.objects.filter(user=request.user))

        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem=0

        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
           wishitem=len(Favour.objects.filter(user=request.user))

        return render(request,"app/category.html",locals())
    
@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        wishlist = Favour.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishitem=0
        
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem=len(Favour.objects.filter(user=request.user))

        return render(request,"app/productdetail.html",locals())
    



class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        totalitem = 0
        wishitem=0

        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user)) 
           wishitem=len(Favour.objects.filter(user=request.user))

        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations!User registered successfully')
            

        else:
            messages.warning(request,"Invalid input data")
        return render(request,'app/customerregistration.html',locals())
        


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem = 0
        wishitem=0

        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
           wishitem=len(Favour.objects.filter(user=request.user))

        return render(request,'app/profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']


            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations ! Profile saved successfully")
        else:
            messages.success(request,"Invalid input data")

        return render(request,'app/profile.html',locals())
            


@login_required        
def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem=0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(Favour.objects.filter(user=request.user))

    return render(request,'app/address.html',locals())



@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
           wishitem=len(Favour.objects.filter(user=request.user))

        return render(request,'app/updateAddress.html',locals())

    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
            
        return redirect("address")


@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")


@login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity*p.product.discounted_price
        amount= amount + value
    totalamount=amount+40
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(Favour.objects.filter(user=request.user))

    return render(request,'app/addtocart.html',locals())


@login_required
def plus_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity*p.product.discounted_price
            amount= amount + value
        totalamount=amount+40
        #print(prod_id)
        data={
              'quantity':c.quantity,
              'amount':amount,
              'totalamount':totalamount
        }
        return JsonResponse(data)



@login_required
def minus_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity*p.product.discounted_price
            amount= amount + value
        totalamount=amount+40
        #print(prod_id)
        data={
              'quantity':c.quantity,
              'amount':amount,
              'totalamount':totalamount
        }
        return JsonResponse(data)


@login_required
def remove_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount= amount + value
        totalamount=amount+40
       
        data={
              'quantity':c.quantity,
              'amount':amount,
              'totalamount':totalamount
        }
        return JsonResponse(data)



@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          wishitem=len(Favour.objects.filter(user=request.user))

        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)

        famount = 0
        for p in cart_items:
            value=p.quantity * p.product.discounted_price
            famount=famount + value
        totalamount=famount+40
        razoramount=int(totalamount * 100)
        client=razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data={"amount":razoramount,"currency":"INR","receipt":"order_rcptid_12"}
        payment_response=client.order.create(data=data)
        print(payment_response)
        #{'id': 'order_MxHMDkdiLLJyd7', 'entity': 'order', 'amount': 28739, 'amount_paid': 0, 'amount_due': 28739, 'currency': 'INR', 'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1699293499}
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status == 'created' :
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request,'app/checkout.html',locals())  

@login_required
def payment_done(request):
    user = request.user
    if user.is_authenticated:
        
     order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    #print("payment_done :oid=",order_id,"pid=",payment_id,"cid=",cust_id)
    user=request.user
    #return redirect("orders")
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    cart.save()
    for c in cart:
        print(c)
    OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
    #c.delete()
    Cart.objects.filter(user=request.user).delete()
    return redirect("orders")


#@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(Favour.objects.filter(user=request.user))

    order_placed=OrderPlaced.objects.filter(user=request.user)
    context= {
        'totalitem': totalitem,
        'wishitem': wishitem,
        'order_placed': order_placed,
    }
    return render(request,'app/orders.html', context)


# Generate and send OTP via email
#@login_required
def send_otp_email(user_email):
    otp = str(random.randint(100000, 999999))
    send_mail(
       'Password Reset OTP',
        f'Your OTP for password reset is: {otp}',
        'your_email@example.com',  # Replace with your email
        [user_email],
        fail_silently=False,
    )
    return otp

# View for sending OTP
#@login_required
def send_otp(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        if user_email:
            otp = send_otp_email(user_email)
            request.session['otp'] = otp  # Store OTP in the session
            return redirect('otp_verification')  # Redirect to OTP verification page
        else:
            messages.error(request, 'Please enter a valid email address.')

    return render(request, 'send_otp.html')  # Create a template for email input

# View for OTP verification
#@login_required
def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        if entered_otp == stored_otp:
            return redirect("password_reset")  # Redirect to the password reset page
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'otp_verification.html')  

# Password reset view
#@login_required
def password_reset(request):
    if request.method == 'POST':
        user=request.user
        # Reset the user's password and clear the OTP session
        new_password = request.POST.get('new_password')
        # Set the new password for the user
        # You can use Django's built-in password reset functionality or your custom logic
        # For example, using Django's built-in functionality:
        user.set_password(new_password)
        user.save()
        
        del request.session['otp']  # Clear the stored OTP from the session
        messages.success(request, 'Password reset successful. You can now log in with your new password.')
        return redirect('password_reset_complete')  # Redirect to the login page

    return render(request, 'password_reset.html')  # Create a template for password reset
    

def pwcomplete(request):
    return render(request,"app/password_reset_complete.html")



def plus_wishlist(request,id):
   
        #prod_id=request.GET['prod_id']
        print(id)
        product=Product.objects.get(id=id)
        user=request.user
        Favour(user=user,product=product).save()
        data={
            'message':'Wishlist added successfully'
        }
        return JsonResponse(data)


def minus_wishlist(request,id):
    #if request.method == 'GET':
        #prod_id=request.GET['prod_id']
        print(id)
        product=Product.objects.get(id=id)
        user=request.user
        Favour.objects.filter(user=user,product=product).delete()
        data={
            'message':'Wishlist removed successfully'
        }
        return JsonResponse(data)


def searchbar(request):
    return render(request,'app/searchbar.html')


@login_required
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        
        wishitem = len(Favour.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html",locals())


@login_required
def show_wishlist(request):
    user=request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Favour.objects.filter(user=request.user))
    product = Favour.objects.filter(user=user)
    return render(request,'app/wishlist.html',locals())