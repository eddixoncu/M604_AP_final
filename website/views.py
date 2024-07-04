from flask import Blueprint, render_template,redirect, url_for, request
from website.forms import LoginForm,OwnerForm, VehicleForm
from .controller import (update_vehicle_owner, get_owner_of_vehicle, get_owner_by_document, get_vehicles, get_owners, update_owner,
                        get_all_infractions,get_payment_status )
from .models import Owner

infractions = Blueprint ('infractions',__name__)

@infractions.route('/', methods=['GET','POST'])
def home():
    form = LoginForm()
    vehicles = get_vehicles()
    owners = get_owners()
    fines = get_all_infractions()
    get_payment_status()
    return render_template('home.html', form=form, vehicles=vehicles, owners=owners, fines=fines)


@infractions.route('/owner/<int:id>',methods=['GET','POST'])
def owner(id):
    form= OwnerForm()
   
    if (request.method == "POST") :
        is_valid =form.validate_on_submit() 
        print(f'valid is {is_valid}') 
        print(f'doc is {id}')
        print(f'name is {form.name.data}')
        print(f'last is {form.last_name.data}')
        owner = Owner(document_number=id,names= form.name.data, last_names=form.last_name.data)
        succes,reason = update_owner(owner)
        return redirect(url_for('infractions.home'))
    else:
        owner = get_owner_by_document(id)
        print(f'names is {owner.names}')
        form.name.data = owner.names
        form.last_name.data = owner.last_names
        return render_template('owner.html',id=id, form=form)


@infractions.route('/vehicle/<plate>',methods=['GET','POST'])
def vehicle(plate):
    current_owner = get_owner_of_vehicle(plate)
    form = VehicleForm()
    form.plate.data = plate

    data_owners = get_owners()
    choices=[]
    for downer in data_owners:
        towner = (downer.document_number,f'{downer.document_number}-{downer.names} {downer.last_names}')
        choices.append(towner)
    form.owners.choices = choices
    if request.method == 'GET':
        return render_template('vehicle.html', plate=plate,form=form, 
                                full_name = f'{current_owner.names} {current_owner.last_names}',
                                document_number=current_owner.document_number)
    else:
        new_document_number = form.owners.data
        print(f'assigning to {new_document_number}')
        reuslt = update_vehicle_owner(plate, new_document_number)
        if reuslt:
            return redirect(url_for('infractions.home'))
        else:
            print('Vehicle cannot be updated')
            return redirect(url_for('infractions.error',key='BUS01'))

@infractions.route('/error/<key>', methods=['GET'])
def error(key):
    errors = {
    "BUS01": "VEHICLE CANNOT CHANGE OWNER BECAUSE IT HAS UNPAID SANCTIONS",
    "BUS02": "ERROR 2",
    "BUS03": 'ERROR 3'
    }   
    issue =''
    try:
        key= key.upper();

        issue = errors[key]

    except: issue ='UNKNOWN ERROR!'

    return render_template('error.html', issue=issue)
