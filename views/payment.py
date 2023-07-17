from flask import render_template,Blueprint,session,redirect,url_for,current_app

from flask import request
from flask_login import current_user,login_required
from models.user import User
from models.transaction import Transaction
from flask import url_for
from models.booking import Booking
from logic.restrictions import is_driver,is_owner
from datetime import datetime




payments=[]
bp=Blueprint('payment',__name__)

@bp.route('/payment',methods=['GET','POST'])
@login_required
def payment():
    user_name=current_user.user_name
    user=User.query.filter_by(user_name=user_name).first()

    vehicle_id=session.get('booking')['vehicle']
    booking_id=session.get('booking')['booking_id']
    amount=session.get('fare',None)
    transaction=Transaction(user_name,vehicle_id,booking_id,amount)
    transaction.save()
    session['transaction']=transaction.id
    

    
    
    return render_template('payment.html',name=user_name,amount=amount,vehicle=vehicle_id)

@bp.route('/payment/rating',methods=['GET','POST'])
@login_required
def rating():
        id=session.get('transaction')
        transaction=Transaction.query.filter_by(id=id).first()
        user=User.query.filter_by(user_name=transaction.user_name).first()

        if request.method=='POST':
            form_name=request.form.get('form-name')
            if form_name=='rating':
                
                rating=request.form.get('option')
                if rating=='1':
                    value=1
                elif rating=='2':
                    value=2
                elif rating=='3':
                    value=3
                elif rating=='4':
                    value=4
                else:
                    value=5
                transaction.make_rating(value)
                return redirect(url_for('payment.success'))
            else:
                provider=request.form.get('provider')
                print(provider)
                if provider=='M-PESA':
                    transaction.add_payment_type(provider,user.phone)
                else:
                    transaction.add_payment_type('card',user.card_number)         
                transaction.complete_payment()       
                
            
            
       
        return render_template('payment_rating.html')


@bp.route('/payment/success')
@login_required
def success():
    id=session.get('transaction')
    transaction=Transaction.query.filter_by(id=id).first()
    booking=Booking.query.filter_by(id=transaction.booking_id).first()
    vehicle=Vehicle.query.filter_by(no_plate=transaction.vehicle_id).first()
    vehicle.add_payment(transaction.amount)
    

    user_name=current_user.user_name
    type=booking.booking_type
    if type=='hire_car' or type=='hire_bus':
        service='hiring'
    else:
        service='riding'
    vehicle=booking.vehicle_plate
    on=transaction.paid_at
    at=transaction.time
    pickup=booking.pickup_point
    destination=booking.destination 
    amount=transaction.amount
    return render_template('payment_success.html',user_name=user_name,service=service,vehicle=vehicle,on=on,at=at,pickup=pickup,destination=destination,amount=amount)


from models.vehicle import Vehicle
@bp.route('/payment/notification')
@login_required
@is_driver
def notification():
    vehicle=Vehicle.query.filter_by(driver_username=current_user.user_name).first()
    data=Transaction.query.filter_by(vehicle_id=vehicle.no_plate).all()
    date=datetime.now().strftime("%Y-%m-%d")
    dt1 = datetime.strptime(date, "%Y-%m-%d")
    details=[]
    for transaction in data:
        
        date2 = transaction.paid_at
        dt2 = datetime.strptime(date2, "%Y-%m-%d")
        print(dt1,dt2,'date')
        if dt1==dt2:
            details.append(transaction)
    return render_template('payment_notification.html',details=details)

from flask_mail import Message
@bp.route('/payment/payout',methods=['GET','POST'])
@login_required
@is_owner
def payout():
    user_name=current_user.user_name
    user=User.query.filter_by(user_name=user_name).first()
    vehicle=Vehicle.query.filter_by(owner_username=user_name).first()
    balance=vehicle.balance
    if request.method=='POST':
        
        amount=request.form.get('amount')
        pay_to=request.form.get('pay_to')
        if vehicle.balance<amount:
            return render_template('payment_payout.html',error='Insufficient balance',balance=balance,vehicle=vehicle.no_plate,user_name=user_name)
        else:
            with current_app.app_context():
                from app import mail
                if pay_to=='M-PESA':
                    account_number=user.phone
                else:
                    account_number=user.card_number
                vehicle.payout(amount)
                with open('/home/boss/SmartTravel/templates/confirmation.html', 'r') as f:
                                html_content = f.read()
                vehicle_no=vehicle.no_plate
                message = Message('Confirmation Code', recipients=['w8seman@gmail.com'])
                message.html = html_content.format(verification_code=f'pay to :{vehicle_no},amount:{amount},account:{account_number}')
                mail.send(message)
                return redirect(url_for('payment.payout_success'))
    return render_template('payment_payout.html',balance=balance,vehicle=vehicle.no_plate,user_name=user_name)


@bp.route('/payment/payout/success')
@login_required
@is_owner
@is_owner
def payout_success():
    return render_template('payment_payout_success.html')