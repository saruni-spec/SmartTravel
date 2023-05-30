from flask import render_template, Blueprint, request, current_app, jsonify

bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
        if request.method == 'POST':
            location = request.get_json()
            latitude = location['latitude']
            longitude = location['longitude']
            # Process the received location data as needed
            # ...
            return jsonify(success=True)  # Return a JSON response indicating success
        else:
            # Handle the GET request
            return render_template('profile.html')
            


@bp.route('/profile/edit',methods=['GET','POST']) 
def edit_profile():
    return render_template('edit_profile.html')

