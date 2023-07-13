from flask import render_template,Blueprint,session
from extensions.extensions import service
from flask import request
from flask_login import current_user
from models.user import User
from models.transaction import Transaction




payments=[]
bp=Blueprint('payment',__name__)

@bp.route('/payment',methods=['GET','POST'])
def payment():
    user_name=current_user.username
    user=User.query.filter_by(user_name=user_name).first()

    vehicle_id=session.get('booking')['vehicle']
    booking_id=session.get('booking')['booking_id']
    amount=10
    transaction=Transaction(user_name,vehicle_id,booking_id,amount)
    transaction.save()

    card_number=user.card_number
    phone=user.phone
    email=user.email

    
    
    return render_template('payment.html',user_name=user_name,card_number=card_number,phone=phone,amount=amount,email=email)

@bp.route('/payment/rating',methods=['GET','POST'])
def verify():
       
        return render_template('payment_rating.html')


