from flask import render_template,Blueprint

bp=Blueprint('payment',__name__)

@bp.route('/payment',methods=['GET','POST'])
def payment():
    return render_template('payment.html')