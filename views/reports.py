from flask import Blueprint,render_template,request
from flask_login import login_required,current_user
from datetime import datetime,timedelta
from models.booking import Booking
from logic.time_query import month
from logic.restrictions import is_driver,is_owner
from models.vehicle import Vehicle
from models.transaction import Transaction


bp=Blueprint('report',__name__)



@bp.route('/report')
@login_required
def report():
    if current_user.check_if_driver():
        print('ttttt')
    else:
        print('ffff')
    return render_template('report.html')


@bp.route('/report/booking',methods=['GET','POST'])
@login_required
def booking_history():
    data=Booking.query.filter_by(user_name=current_user.user_name).all()
    query='all'
    filtered_data=[]
    user_title=current_user.user_name
    if request.method=='POST':
        button=request.form.get('button_name')
        if button=='date_filter':
            query='date_filter'
            date=request.form.get('date')
            dt1 = datetime.strptime(date, "%Y-%m-%d")
            for booking in data:
                if booking.date is None:
                    booking.date=datetime.now().strftime("%Y-%m-%d")
                    booking.commit()
                date2 = booking.date
                
                dt2 = datetime.strptime(date2, "%Y-%m-%d")
                print(dt1,dt2,'date')
                if dt1==dt2:
                    filtered_data.append(booking)
        elif button=='month_filter':
            query='month_filter'
            month_name=request.form.get('month')
            month_no=month(month_name)
            for booking in data:
                if booking.date is None:
                    booking.date=datetime.now().strftime("%Y-%m-%d")
                    booking.commit()
                dt = datetime.strptime(booking.date, "%Y-%m-%d")

                month_reg = dt.strftime("%m")
                print(month_reg,month_no,'month')
                if int(month_reg)==int(month_no):
                    
                    filtered_data.append(booking)
        elif button=='year_filter':
            query='year_filter'
            year=request.form.get('year')
            for booking in data:
                if booking.date is None:
                    booking.date=datetime.now().strftime("%Y-%m-%d")
                    booking.commit()
                dt = datetime.strptime(booking.date, "%Y-%m-%d")

                year_reg = dt.strftime("%Y")
                print(year_reg,year,'year')
                if int(year_reg)==int(year):
                    filtered_data.append(booking)
        elif button=='week_filter':
            query='week_filter'
            today=datetime.now().strftime("%Y-%m-%d")
            dt_today = datetime.strptime(today, "%Y-%m-%d")
            dt_week_ago = dt_today - timedelta(days=7)
            for booking in data:
                if booking.date is None:
                    booking.date=datetime.now().strftime("%Y-%m-%d")
                    booking.commit()
                dt_date = datetime.strptime(booking.date, "%Y-%m-%d")


                if dt_date >= dt_week_ago and dt_date <= dt_today:
                    filtered_data.append(booking)
        elif button=='id':
            query='id'
            for booking in data:
                entry={'id':booking.id,'status':booking.Status}
                filtered_data.append(entry)
        elif button=='pickup_point':
            query='pickup_point'
            
            for booking in data:
                entry={'id':booking.id,'pickup_point':booking.pickup_point}
                filtered_data.append(entry)
        elif button=='time':
            query='time'
            
            for booking in data:
                entry={'id':booking.id,'time':booking.time}
                filtered_data.append(entry)
        elif button=='destination':
            query='destination'
            

            for booking in data:
                
                entry={'id':booking.id,'destination':booking.destination}
                filtered_data.append(entry)
        elif button=='vehicle_plate"':
            query='vehicle_plate'
            
            
            for booking in data:
                
                entry={'id':booking.id,'vehicle_plate':booking.vehicle_plate}
                filtered_data.append(entry)
                
        elif button=='date':
            query='date'
            
            for booking in data:
                entry={'id':booking.id,'date':booking.date}
                filtered_data.append(entry)

        elif button=='status':
            query='status'
            
            for booking in data:
                entry={'id':booking.id,'status':booking.Status}
                filtered_data.append(entry)
        
        elif button=='booking_type':
            query='booking_type'
            
            for booking in data:
                entry={'id':booking.id,'booking_type':booking.booking_type}
                filtered_data.append(entry)

        elif button=='payment_details':
            query='payment_details'
            
            for booking in data:
                if booking.payment_details:
                    
                    entry={'id':booking.id,'payment_details':booking.payment_details.status}
                else:
                    entry={'id':booking.id,'payment_details':'Payment Not Initiated'}
                filtered_data.append(entry)

        else:
            query='all'
            print('running else')
            filtered_data=data
        print(filtered_data,'filtered_data')
        print(query,'query')
        return render_template('booking_history.html',data=filtered_data,query=query,user_title=user_title)

    return render_template('booking_history.html',data=data,user_title=user_title)

@bp.route('/report/vehicle_bookings',methods=['GET','POST'])
@login_required
def vehicle_bookings():
    vehicle=Vehicle.query.filter_by(driver_username=current_user.user_name).first()
    if vehicle is None:
        vehicle=Vehicle.query.filter_by(owner_username=current_user.user_name).first()
    data=Booking.query.filter_by(vehicle_plate=vehicle.no_plate).all()
    user_title=f'{vehicle.driver_username},{vehicle.no_plate}'
    query='all'
    filtered_data=[]
    if request.method=='POST':
        button=request.form.get('button_name')
        if button=='date_filter':
            query='date_filter'
            date=request.form.get('date')
            dt1 = datetime.strptime(date, "%Y-%m-%d")
            for booking in data:
                if booking.date is None:
                    booking.date=datetime.now().strftime("%Y-%m-%d")
                    booking.commit()
                date2 = booking.date
                
                dt2 = datetime.strptime(date2, "%Y-%m-%d")
                print(dt1,dt2,'date')
                if dt1==dt2:
                    filtered_data.append(booking)
        elif button=='month_filter':
            query='month_filter'
            month_name=request.form.get('month')
            month_no=month(month_name)
            for booking in data:
                if booking.date is None:
                    booking.date=datetime.now().strftime("%Y-%m-%d")
                    booking.commit()
                dt = datetime.strptime(booking.date, "%Y-%m-%d")

                month_reg = dt.strftime("%m")
                print(month_reg,month_no,'month')
                if int(month_reg)==int(month_no):
                    
                    filtered_data.append(booking)
        elif button=='year_filter':
            query='year_filter'
            year=request.form.get('year')
            for booking in data:
                if booking.date is None:
                    booking.date=datetime.now().strftime("%Y-%m-%d")
                    booking.commit()
                dt = datetime.strptime(booking.date, "%Y-%m-%d")

                year_reg = dt.strftime("%Y")
                print(year_reg,year,'year')
                if int(year_reg)==int(year):
                    filtered_data.append(booking)
        elif button=='week_filter':
            query='week_filter'
            today=datetime.now().strftime("%Y-%m-%d")
            dt_today = datetime.strptime(today, "%Y-%m-%d")
            dt_week_ago = dt_today - timedelta(days=7)
            for booking in data:
                if booking.date is None:
                    booking.date=datetime.now().strftime("%Y-%m-%d")
                    booking.commit()
                dt_date = datetime.strptime(booking.date, "%Y-%m-%d")


                if dt_date >= dt_week_ago and dt_date <= dt_today:
                    filtered_data.append(booking)
        elif button=='id':
            query='id'
            for booking in data:
                entry={'id':booking.id,'status':booking.Status}
                filtered_data.append(entry)
        elif button=='user_name':
            query='user_name'
            for booking in data:
                entry={'id':booking.id,'user_name':booking.user_name}
                filtered_data.append(entry)
        elif button=='pickup_point':
            query='pickup_point'
            
            for booking in data:
                entry={'id':booking.id,'pickup_point':booking.pickup_point}
                filtered_data.append(entry)
        elif button=='phone':
            query='phone'
            
            for booking in data:
                entry={'id':booking.id,'phone':booking.phone}
                filtered_data.append(entry)
        elif button=='time':
            query='time'
            
            for booking in data:
                entry={'id':booking.id,'time':booking.time}
                filtered_data.append(entry)
        elif button=='destination':
            query='destination'
            

            for booking in data:
                
                entry={'id':booking.id,'destination':booking.destination}
                filtered_data.append(entry)
                
        elif button=='date':
            query='date'
            
            for booking in data:
                entry={'id':booking.id,'date':booking.date}
                filtered_data.append(entry)

        elif button=='status':
            query='status'
            
            for booking in data:
                entry={'id':booking.id,'status':booking.Status}
                filtered_data.append(entry)
        
        elif button=='booking_type':
            query='booking_type'
            
            for booking in data:
                entry={'id':booking.id,'booking_type':booking.booking_type}
                filtered_data.append(entry)

        elif button=='payment_details':
            query='payment_details'
            
            for booking in data:
                if booking.payment_details:
                    
                    entry={'id':booking.id,'payment_details':booking.payment_details.status}
                else:
                    entry={'id':booking.id,'payment_details':'Payment Not Initiated'}
                filtered_data.append(entry)

        else:
            query='all'
            print('running else')
            filtered_data=data
        print(filtered_data,'filtered_data')
        print(query,'query')
        return render_template('vehicle_booking.html',data=filtered_data,query=query,user_title=user_title)

    return render_template('vehicle_booking.html',data=data,user_title=user_title)


@bp.route('/report/transaction',methods=['GET','POST'])
@login_required
def transaction_history():
    user_title=current_user.user_name
    data=Transaction.query.filter_by(user_name=current_user.user_name).all()
    query='all'
    filtered_data=[]
    if request.method=='POST':
        button=request.form.get('button_name')
        if button=='date_filter':
            query='date_filter'
            date=request.form.get('date')
            dt1 = datetime.strptime(date, "%Y-%m-%d")
            for transaction in data:
                if transaction.paid_at is None:
                    transaction.paid_at=datetime.now().strftime("%Y-%m-%d")
                    transaction.commit()
                date2 = transaction.paid_at
                print(dt1,'gg',date2,'date')
                dt2 = datetime.strptime(date2, "%Y-%m-%d")
                print(dt1,dt2,'date')
                if dt1==dt2:
                    filtered_data.append(transaction)
        elif button=='month_filter':
            query='month_filter'
            month_name=request.form.get('month')
            month_no=month(month_name)
            for transaction in data:
                if transaction.paid_at is None:
                    transaction.paid_at=datetime.now().strftime("%Y-%m-%d")
                    transaction.commit()
                print(transaction.paid_at,'transaction.paid_at')
                
                dt = datetime.strptime(transaction.paid_at, "%Y-%m-%d")

                month_reg = dt.strftime("%m")
                print(month_reg,month_no,'month')
                if int(month_reg)==int(month_no):
                    
                    filtered_data.append(transaction)
        elif button=='year_filter':
            query='year_filter'
            year=request.form.get('year')
            for transaction in data:
                if transaction.paid_at is None:
                    transaction.paid_at=datetime.now().strftime("%Y-%m-%d")
                    transaction.commit()
                dt = datetime.strptime(transaction.paid_at, "%Y-%m-%d")

                year_reg = dt.strftime("%Y")
                print(year_reg,year,'year')
                if int(year_reg)==int(year):
                    filtered_data.append(transaction)
        elif button=='week_filter':
            query='week_filter'
            today=datetime.now().strftime("%Y-%m-%d")
            dt_today = datetime.strptime(today, "%Y-%m-%d")
            dt_week_ago = dt_today - timedelta(days=7)
            for transaction in data:
                if transaction.paid_at is None:
                    transaction.paid_at=datetime.now().strftime("%Y-%m-%d")
                    transaction.commit()
                dt_date = datetime.strptime(transaction.paid_at, "%Y-%m-%d")


                if dt_date >= dt_week_ago and dt_date <= dt_today:
                    filtered_data.append(transaction)
        elif button=='id':
            query='id'
            for transaction in data:
                entry={'id':transaction.id,'status':transaction.status}
                filtered_data.append(entry)

        elif button=='amount':
            query='amount'
            
            for transaction in data:
                entry={'id':transaction.id,'amount':transaction.amount}
                filtered_data.append(entry)
        elif button=='rating':
            query='rating'
            
            for transaction in data:
                entry={'id':transaction.id,'rating':transaction.rating}
                filtered_data.append(entry)
        elif button=='paid_at':
            query='paid_at'
            
            for transaction in data:
                entry={'id':transaction.id,'paid_at':transaction.time}
                filtered_data.append(entry)
        elif button=='payment_type':
            query='payment_type'
            

            for transaction in data:
                
                entry={'id':transaction.id,'payment_type':transaction.payment_type}
                filtered_data.append(entry)
        elif button=='vehicle_id"':
            query='vehicle_id'
            
            
            for transaction in data:
                
                entry={'id':transaction.id,'vehicle_id':transaction.vehicle_id}
                filtered_data.append(entry)
                
        elif button=='date':
            query='date'
            
            for transaction in data:
                entry={'id':transaction.id,'date':transaction.paid_at}
                filtered_data.append(entry)

        elif button=='status':
            query='status'
            
            for transaction in data:
                entry={'id':transaction.id,'status':transaction.status}
                filtered_data.append(entry)
        
        elif button=='card_number':
            query='card_number'
            
            for transaction in data:
                entry={'id':transaction.id,'card_number':transaction.card_number}
                filtered_data.append(entry)


        else:
            query='all'
            filtered_data=data

        return render_template('transaction_history.html',data=filtered_data,query=query,user_title=user_title)

    return render_template('transaction_history.html',data=data,user_title=user_title)



@bp.route('/report/vehicle_transactions',methods=['GET','POST'])
@login_required
def vehicle_transactions():
    vehicle=Vehicle.query.filter_by(driver_username=current_user.user_name).first()
    if vehicle is None:
        vehicle=Vehicle.query.filter_by(owner_username=current_user.user_name).first()
    data=Transaction.query.filter_by(vehicle_id=vehicle.no_plate).all()
    user_title=f'{vehicle.driver_username},{vehicle.no_plate}'
    query='all'
    filtered_data=[]
    if request.method=='POST':
        button=request.form.get('button_name')
        if button=='date_filter':
            query='date_filter'
            date=request.form.get('date')
            dt1 = datetime.strptime(date, "%Y-%m-%d")
            for transaction in data:
                if transaction.paid_at is None:
                    transaction.paid_at=datetime.now().strftime("%Y-%m-%d")
                    transaction.commit()
                date2 = transaction.paid_at
                print(dt1,'gg',date2,'date')
                dt2 = datetime.strptime(date2, "%Y-%m-%d")
                print(dt1,dt2,'date')
                if dt1==dt2:
                    filtered_data.append(transaction)
        elif button=='month_filter':
            query='month_filter'
            month_name=request.form.get('month')
            month_no=month(month_name)
            for transaction in data:
                if transaction.paid_at is None:
                    transaction.paid_at=datetime.now().strftime("%Y-%m-%d")
                    transaction.commit()
                dt = datetime.strptime(transaction.paid_at, "%Y-%m-%d")

                month_reg = dt.strftime("%m")
                print(month_reg,month_no,'month')
                if int(month_reg)==int(month_no):
                    
                    filtered_data.append(transaction)
        elif button=='year_filter':
            query='year_filter'
            year=request.form.get('year')
            for transaction in data:
                if transaction.paid_at is None:
                    transaction.paid_at=datetime.now().strftime("%Y-%m-%d")
                    transaction.commit()
                dt = datetime.strptime(transaction.paid_at, "%Y-%m-%d")

                year_reg = dt.strftime("%Y")
                print(year_reg,year,'year')
                if int(year_reg)==int(year):
                    filtered_data.append(transaction)
        elif button=='week_filter':
            query='week_filter'
            today=datetime.now().strftime("%Y-%m-%d")
            dt_today = datetime.strptime(today, "%Y-%m-%d")
            dt_week_ago = dt_today - timedelta(days=7)
            for transaction in data:
                if transaction.paid_at is None:
                    transaction.paid_at=datetime.now().strftime("%Y-%m-%d")
                    transaction.commit()
                dt_date = datetime.strptime(transaction.paid_at, "%Y-%m-%d")


                if dt_date >= dt_week_ago and dt_date <= dt_today:
                    filtered_data.append(transaction)
        elif button=='id':
            query='id'
            for transaction in data:
                entry={'id':transaction.id,'status':transaction.status}
                filtered_data.append(entry)
        elif button=='user_name':
            query='user_name'
            for transaction in data:
                entry={'id':transaction.id,'user_name':transaction.user_name}
                filtered_data.append(entry)
        elif button=='amount':
            query='amount'
            
            for transaction in data:
                entry={'id':transaction.id,'amount':transaction.amount}
                filtered_data.append(entry)
        elif button=='rating':
            query='rating'
            
            for transaction in data:
                entry={'id':transaction.id,'rating':transaction.rating}
                filtered_data.append(entry)
        elif button=='paid_at':
            query='paid_at'
            
            for transaction in data:
                entry={'id':transaction.id,'paid_at':transaction.time}
                filtered_data.append(entry)
        elif button=='payment_type':
            query='payment_type'
            

            for transaction in data:
                
                entry={'id':transaction.id,'payment_type':transaction.payment_type}
                filtered_data.append(entry)
        
                
        elif button=='date':
            query='date'
            
            for transaction in data:
                entry={'id':transaction.id,'date':transaction.paid_at}
                filtered_data.append(entry)

        elif button=='status':
            query='status'
            
            for transaction in data:
                entry={'id':transaction.id,'status':transaction.status}
                filtered_data.append(entry)
        
        elif button=='card_number':
            query='card_number'
            
            for transaction in data:
                entry={'id':transaction.id,'card_number':transaction.card_number}
                filtered_data.append(entry)


        else:
            query='all'
            filtered_data=data

        return render_template('vehicle_transactions.html',data=filtered_data,query=query,user_title=user_title)

    return render_template('vehicle_transactions.html',data=data,user_title=user_title)