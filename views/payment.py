from flask import render_template,Blueprint
from extensions.extensions import service
from flask import request


payments=[]
bp=Blueprint('payment',__name__)

@bp.route('/payment',methods=['GET','POST'])
def payment():


    response = service.collect.checkout(phone_number=254745050238,
                                    email="smithsaruni16@gmail.com", amount=10, currency="KES", comment="Service Fees")
    payments.append(response)
    return render_template('payment.html',response=response.get("url"))

@bp.route('/payment/verify',methods=['GET','POST'])
def verify():
        response = payments[0]
        print(response)
        response = service.collect.status(invoice_id="<invoice-id>")
        print(response)

        return 'success'


