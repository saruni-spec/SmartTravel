from flask import Blueprint,render_template
from models.vehicle import Vehicle
from models.booking import Booking
from models.user import User
from models.driver import Driver
from models.stages import Stages
from flask_login import login_required,current_user
from logic.restrictions import is_admin
from flask import request
from models.transaction import Transaction
from models.routes import Route
from datetime import datetime,timedelta
from logic.time_query import month



bp=Blueprint('admin',__name__)

@bp.route('/admin')
@login_required
@is_admin
def admin():
    return render_template('admin.html')

@bp.route('/admin/vehicles' ,methods=['GET','POST'])
@login_required
@is_admin
def vehicles():
    vehicles=Vehicle.query.all()
    query='all'
    filtered_data=[]
    if request.method=='POST':
        
        button=request.form.get('button_name')
        if button=='date_filter':
            query='date_filter'
            date=request.form.get('date')
            dt1 = datetime.strptime(date, "%Y-%m-%d")
            for vehicle in vehicles:
                if vehicle.date_registered is None:
                    vehicle.date_registered=datetime.now().strftime("%Y-%m-%d")
                    vehicle.commit()
                date2 = vehicle.date_registered
                
                dt2 = datetime.strptime(date2, "%m / %d / %Y")
                print(dt1,dt2)
                if dt1==dt2:
                    filtered_data.append(vehicle)
        if button=='month_filter':
            query='month_filter'
            month_name=request.form.get('month')
            month_no=month(month_name)
            for vehicle in vehicles:
                if vehicle.date_registered is None:
                    vehicle.date_registered=datetime.now().strftime("%Y-%m-%d")
                    vehicle.commit()
                dt = datetime.strptime(vehicle.date_registered, "%Y-%m-%d")

                month_reg = dt.strftime("%m")
                print(month_reg,month_no)
                if int(month_reg)==int(month_no):
                    filtered_data.append(vehicle)
        if button=='year_filter':
            query='year_filter'
            year=request.form.get('year')
            for vehicle in vehicles:
                if vehicle.date_registered is None:
                    vehicle.date_registered=datetime.now().strftime("%Y-%m-%d")
                    vehicle.commit()
                dt = datetime.strptime(vehicle.date_registered, "%Y-%m-%d")

                year_reg = dt.strftime("%Y")
                print(year_reg,year)
                if int(year_reg)==int(year):
                    filtered_data.append(vehicle)
        if button=='week_filter':
            query='week_filter'
            today=datetime.now().strftime("%Y-%m-%d")
            dt_today = datetime.strptime(today, "%Y-%m-%d")
            dt_week_ago = dt_today - timedelta(days=7)
            for vehicle in vehicles:
                if vehicle.date_registered is None:
                    vehicle.date_registered=datetime.now().strftime("%Y-%m-%d")
                    vehicle.commit()
                dt_date = datetime.strptime(vehicle.date_registered, "%Y-%m-%d")


                if dt_date >= dt_week_ago and dt_date <= dt_today:
                    filtered_data.append(vehicle)

        if button=='no_plate':
            query='no_plate'
            for vehicle in vehicles:
                data={'no_plate':vehicle.no_plate,'type':vehicle.vehicle_type}
                filtered_data.append(data)
        elif button=='capacity':
            query='capacity'
            
            for vehicle in vehicles:
                data={'no_plate':vehicle.no_plate,'capacity':vehicle.capacity}
                filtered_data.append(data)
        elif button=='owner_username':
            query='owner_username'
            
            for vehicle in vehicles:
                data={'no_plate':vehicle.no_plate,'owner_username':vehicle.owner_username}
                filtered_data.append(data)
        elif button=='driver_username':
            query='driver_username'
            
            for vehicle in vehicles:
                data={'no_plate':vehicle.no_plate,'driver_username':vehicle.driver_username}
                filtered_data.append(data)
        elif button=='color':
            query='color'
            
            for vehicle in vehicles:
                data={'no_plate':vehicle.no_plate,'color':vehicle.color}
                filtered_data.append(data)
        elif button=='is_active':
            query='is_active'
            
            for vehicle in vehicles:
                data={'no_plate':vehicle.no_plate,'is_active':vehicle.is_active}
                filtered_data.append(data)

        elif button=='for_hire':
            query='for_hire'
            
            for vehicle in vehicles:
                data={'no_plate':vehicle.no_plate,'for_hire':vehicle.for_hire}
                filtered_data.append(data)
        elif button=='build_type':
            query='build_type'
            
            for vehicle in vehicles:
                data={'no_plate':vehicle.no_plate,'build_type':vehicle.build_type}
                filtered_data.append(data)
        elif button=='date_registered':
            query='date_registered'
            
            for vehicle in vehicles:
                data={'no_plate':vehicle.no_plate,'date_registered':vehicle.date_registered}
                filtered_data.append(data)
        elif button=='ratings':
            query='ratings'
            
            for vehicle in vehicles:
                data={'no_plate':vehicle.no_plate,'ratings':vehicle.ratings}
                filtered_data.append(data)
        else:
            query='all'
            filtered_data=vehicles
            return render_template('admin_vehicles.html',vehicles=vehicles,query=query)

        return render_template('admin_vehicles.html',vehicles=filtered_data,query=query)


    return render_template('admin_vehicles.html',vehicles=vehicles,query=query)

@bp.route('/admin/bookings',methods=['GET','POST'])
@login_required
@is_admin
def bookings():
    data=Booking.query.all()
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
                
                dt2 = datetime.strptime(date2, "%m / %d / %Y")
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
                    entry={'id':booking.id,'user_name':booking.user_name}
                    filtered_data.append(entry)
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
            return render_template('admin_bookings.html',data=data,query=query)
        print(filtered_data,'filtered_data')
        return render_template('admin_bookings.html',data=filtered_data,query=query)

    return render_template('admin_bookings.html',data=data)

@bp.route('/admin/users',methods=['GET','POST'])
@login_required
@is_admin
def users():
    users=User.query.all()
    query='all'
    filtered_data=[]
    if request.method=='POST':
        button=request.form.get('button_name')
        if button=='user_name':
            query='user_name'
            for user in users:
                data={'user_name':user.user_name,'role':'None'}
                filtered_data.append(data)
        elif button=='email':
            query='email'
            
            for user in users:
                data={'user_name':user.user_name,'email':user.email}
                filtered_data.append(data)
        elif button=='phone':
            query='phone'
            
            for user in users:
                data={'user_name':user.user_name,'phone':user.phone}
                filtered_data.append(data)
        elif button=='address':
            query='address'
            
            for user in users:
                data={'user_name':user.user_name,'address':user.address}
                filtered_data.append(data)
        elif button=='is_driver':
            query='is_driver'
            

            for user in users:
                if user.driver_details:
                    is_driver='Yes'
                else:
                    is_driver='No'
                data={'user_name':user.user_name,'is_driver':is_driver}
                filtered_data.append(data)
        elif button=='is_owner':
            query='is_owner'
            
            
            for user in users:
                if user.owner_details:
                    is_owner='Yes'
                else:
                    is_owner='No'
                data={'user_name':user.user_name,'is_owner':is_owner}
                filtered_data.append(data)
                
        elif button=='date_registered':
            query='date_registered'
            
            for user in users:
                data={'user_name':user.user_name,'date_registered':user.date_registered}
                filtered_data.append(data)

        else:
            query='all'
            filtered_data=users
            return render_template('admin_users.html',users=users,query=query)

        return render_template('admin_users.html',users=filtered_data,query=query)

    return render_template('admin_users.html',users=users)

@bp.route('/admin/drivers',methods=['GET','POST'])
@login_required
@is_admin
def drivers():
    all_users=User.query.all()
    users=[]
    for user in all_users:
        if user.driver_details:
            users.append(user)

            
            
    filtered_data=[]
    if request.method=='POST':
        button=request.form.get('button_name')
        if button=='user_name':
            query='user_name'
            for user in users:
                data={'user_name':user.user_name,'role':'None'}
                filtered_data.append(data)
        elif button=='email':
            query='email'
            
            for user in users:
                data={'user_name':user.user_name,'email':user.email}
                filtered_data.append(data)
        elif button=='phone':
            query='phone'
            
            for user in users:
                data={'user_name':user.user_name,'phone':user.phone}
                filtered_data.append(data)
        elif button=='address':
            query='address'
            
            for user in users:
                data={'user_name':user.user_name,'address':user.address}
                filtered_data.append(data)
        elif button=='date_registered':
            query='date_registered'
            
            for user in users:
                data={'user_name':user.user_name,'date_registered':user.date_registered}
                filtered_data.append(data)
        elif button=='licence_no':
            query='licence_no'

            for user in users:
                data={'user_name':user.user_name,'licence_no':user.driver_details.licence_no}
                filtered_data.append(data)
        elif button=='vehicle_no':
            query='vehicle_no'

            for user in users:
                data={'user_name':user.user_name,'vehicle_no':user.driver_details.drives.no_plate}
                filtered_data.append(data)
                
        else:
            query='all'
            filtered_data=users
            return render_template('admin_drivers.html',users=users,query=query)

        return render_template('admin_drivers.html',users=filtered_data,query=query)
    return render_template('admin_drivers.html',users=users)



@bp.route('/admin/riders',methods=['GET','POST'])
@login_required
@is_admin
def riders():
    all_users=User.query.all()
    users=[]
    for user in all_users:
        if not user.driver_details:
            users.append(user)

            
            
    filtered_data=[]
    if request.method=='POST':
        button=request.form.get('button_name')
        if button=='user_name':
            query='user_name'
            for user in users:
                data={'user_name':user.user_name,'role':'None'}
                filtered_data.append(data)
        elif button=='email':
            query='email'
            
            for user in users:
                data={'user_name':user.user_name,'email':user.email}
                filtered_data.append(data)
        elif button=='phone':
            query='phone'
            
            for user in users:
                data={'user_name':user.user_name,'phone':user.phone}
                filtered_data.append(data)
        elif button=='address':
            query='address'
            
            for user in users:
                data={'user_name':user.user_name,'address':user.address}
                filtered_data.append(data)
        elif button=='date_registered':
            query='date_registered'
            
            for user in users:
                data={'user_name':user.user_name,'date_registered':user.date_registered}
                filtered_data.append(data)

        else:
            query='all'
            filtered_data=users
            return render_template('admin_riders.html',users=users,query=query)

        return render_template('admin_riders.html',users=filtered_data,query=query)

    return render_template('admin_riders.html',users=users)


@bp.route('/admin/owners',methods=['GET','POST'])
@login_required
@is_admin
def owners():
    all_users=User.query.all()
    users=[]
    for user in all_users:
        if user.owner_details:
            users.append(user)

            
            
    filtered_data=[]
    if request.method=='POST':
        button=request.form.get('button_name')
        if button=='user_name':
            query='user_name'
            for user in users:
                data={'user_name':user.user_name,'role':'None'}
                filtered_data.append(data)
        elif button=='email':
            query='email'
            
            for user in users:
                data={'user_name':user.user_name,'email':user.email}
                filtered_data.append(data)
        elif button=='phone':
            query='phone'
            
            for user in users:
                data={'user_name':user.user_name,'phone':user.phone}
                filtered_data.append(data)
        elif button=='address':
            query='address'
            
            for user in users:
                data={'user_name':user.user_name,'address':user.address}
                filtered_data.append(data)
        elif button=='date_registered':
            query='date_registered'
            
            for user in users:
                data={'user_name':user.user_name,'date_registered':user.date_registered}
                filtered_data.append(data)
        elif button=='licence_no':
            query='licence_no'

            for user in users:
                data={'user_name':user.user_name,'licence_no':user.driver_details.licence_no}
                filtered_data.append(data)
        elif button=='vehicle_no':
            query='vehicle_no'

            for user in users:
                data={'user_name':user.user_name,'vehicle_no':user.driver_details.drives.no_plate}
                filtered_data.append(data)
                
        else:
            query='all'
            filtered_data=users
            return render_template('admin_owners.html',users=users,query=query)

        return render_template('admin_owners.html',users=filtered_data,query=query)
    return render_template('admin_owners.html',users=users)

@bp.route('/admin/transactions',methods=['GET','POST'])
@login_required
@is_admin
def transactions():
    data=Transaction.query.all()
    query='all'
    filtered_data=[]
    if request.method=='POST':
        button=request.form.get('button_name')
        if button=='id':
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
                entry={'id':transaction.id,'paid_at':transaction.paid_at}
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
                entry={'id':transaction.id,'date':transaction.date}
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
            return render_template('admin_transactions.html',data=data,query=query)

        return render_template('admin_transactions.html',data=filtered_data,query=query)

    return render_template('admin_transactions.html',data=data)

@bp.route('/admin/routes',methods=['GET','POST'])
@login_required
@is_admin
def routes():
    data=Route.query.all()
    query='all'
    filtered_data=[]
    if request.method=='POST':
        button=request.form.get('button_name')
        if button=='id':
            query='id'
            for route in data:
                entry={'id':route.id,'name':route.route_distane}
                filtered_data.append(entry)
        elif button=='route_distane':
            query='route_distane'
            for route in data:
                entry={'id':route.id,'name':route.route_distane}
                filtered_data.append(entry)
        elif button=='stages':
            query='stages'
            for route in data:
               
                entry={'id':route.id,'stages':route.stages}
                filtered_data.append(entry)
        else:
            query='all'
            return render_template('admin_routes.html',data=data,query=query)
        return render_template('admin_routes.html',data=filtered_data,query=query)

    return render_template('admin_routes.html',data=data)



@bp.route('/admin/stages',methods=['GET','POST'])
@login_required
@is_admin
def stages():
    data=Stages.query.all()
    query='all'
    filtered_data=[]
    if request.method=='POST':
        button=request.form.get('button_name')
        if button=='stage_name':
            query='stage_name'
            for stage in data:
                entry={'stage_no':stage.stage_no,'name':stage.stage_name}
                filtered_data.append(entry)
            
        elif button=='latitude':
            query='latitude'
            print(query)
            for stage in data:
                entry={'stage_no':stage.stage_no,'latitude':stage.latitude}
                filtered_data.append(entry)
        elif button=='longitude':
            query='longitude'
            print(query)
            for stage in data:
                entry={'stage_no':stage.stage_no,'longitude':stage.longitude}
                filtered_data.append(entry)
        else:
            query='all'
            print(query)
            return render_template('admin_stages.html',data=data,query=query)
        
        return render_template('admin_stages.html',data=filtered_data,query=query)

    return render_template('admin_stages.html',data=data)