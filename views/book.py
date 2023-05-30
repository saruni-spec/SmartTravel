from flask import render_template,Blueprint

bp=Blueprint('book',__name__)

@bp.route('/book',methods=['GET','POST'])
def book():
    return render_template('book.html')