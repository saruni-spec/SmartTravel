from flask import render_template,Blueprint
from extensions.extensions import service



bp=Blueprint('payment',__name__)

@bp.route('/payment',methods=['GET','POST'])
def payment():
    response = service.collect.checkout(phone_number=254745050238,
                                    email="smithsaruni16@gmail.com", amount=10, currency="KES", comment="Service Fees")

    return render_template('payment.html',response=response.get("url"))