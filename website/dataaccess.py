import sqlite3
from .models import VehiclePerson, Owner,Fine, PaymentChart

_path='transit_registry.db'


def get_vehicles_from_db():
    try:
        vehicles = []
        with sqlite3.connect(_path ) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT V.plate, b.brand, ifnull((p.NOMBRES ||' '||p.APELLIDOS),'') owner
from vehicles V
INNER JOIN brands b on b.id=V.brand_id
LEFT JOIN vehicle_person vp on vp.plate = V.plate
LEFT JOIN PERSON p on vp.numero_documento = p.numero_documento
limit 17""")
            output = cursor.fetchall()
            for row in output:
                v = VehiclePerson(plate=row[0],brand= row[1],full_name=row[2],document_number=0)
                vehicles.append(v)

        return vehicles


    except Exception as exc:
        print(f"ISSUE on get_vehicles_from_db: {exc}")
        return[]


def get_owners_from_db():
    try:
        people = []
        with sqlite3.connect(_path)as conn:
            cursor=conn.cursor();
            cursor.execute("""
                           SELECT  NUMERO_DOCUMENTO, NOMBRES, APELLIDOS
                           from  person
                           limit 10""")
            output = cursor.fetchall()
            for row in output:
                p = Owner(document_number=row[0],names=row[1],last_names=row[2])
                people.append(p)
        return people
    except Exception as exc:
        print(f"ISSUE on get_owners_from_db: {exc}")

def get_owner_by_document_db(document_number):
    try:
        with sqlite3.connect(_path) as conn:
            print('consultado ower ', document_number)
            cursor = conn.cursor()
            sql = f'''
                  select  p.NUMERO_DOCUMENTO, p.NOMBRES, p.APELLIDOS FROM person p WHERE p.NUMERO_DOCUMENTO = '{document_number}' 
                   '''
            #args=(document_number)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                print('SI EXISTE OWNER')
                owner = Owner(document_number=row[0],names=row[1],last_names=row[2])
                return True,owner
            else:
                print('NO EXISTE OWNER')
                return False, "Owner not found"
            
    except Exception as exc:
        reason = f"ISSUE on get_owner_by_document_db: {exc}"
        print(reason)
        return False,reason
    

def get_owner_of_vehicle_db (plate):
    try:
        with sqlite3.connect(_path) as conn:
            cursor = conn.cursor()
            sql=f'''
                SELECT p.numero_documento, p.NOMBRES, p.APELLIDOS
from vehicles v
left join vehicle_person vp on vp.plate = v.plate
LEFT join person p on vp.numero_documento = p.numero_documento
where v.plate = '{plate}'
                '''
            #args =(plate)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                print('SI EXISTE OWNER')
                owner = Owner(document_number=row[0],names=row[1],last_names=row[2])
                return True,owner
            else:
                print('NO EXISTE OWNER')
                return False, "Owner not found"

    except Exception as exc:
        reason = f"ISSUE on get_owner_of_vehicle_db: {exc}"
        print(reason)
        return False,reason

    
def update_owner_db(owner:Owner) :
    try:
        with sqlite3.connect(_path) as conn:
            cursor = conn.cursor()
            sql=""" UPDATE person SET nombres=?, apellidos=? WHERE numero_documento=? ;
                """
            args=(owner.names,owner.last_names, owner.document_number)
            cursor.execute(sql,args)
            return True, ""
    
    except Exception as exc:
        reason = f"ISSUE on update_owner_db: {exc}"
        print(reason)
        return False,reason
    
def update_vehicle_owner_db(plate, document_number):
    try:
        with sqlite3.connect(_path) as conn:
            cursor = conn.cursor()
            sql=f'''
                UPDATE vehicle_person SET numero_documento ={document_number} 
                WHERE plate = '{plate}'
                '''
            cursor.execute(sql)
            return True,""

    except Exception as exc:
        reason = f"ISSUE on update_vehicle_owner_db: {exc}"
        print(reason)
        return False,reason
    
def check_vehicle_unpaid_infractions(plate):
    try:
        with sqlite3.connect(_path) as conn:
            cursor =conn.cursor()
            sql =f"""
            select * from infractions where plate = '{plate}' AND IS_PAID ='NO'
            """
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return True,"Vehicle has pending infractions to be paid"
            else:
                return False, ""
    except Exception as exc:
        reason = f"ISSUE on vehicle_paid_infractions: {exc}"
        print(reason)
        return False,reason
    
def get_all_infractions_db ():

    try:
        sanctions =[]
        with sqlite3.connect(_path) as conn:
            cursor = conn.cursor()
            sql=f'''
                select plate, infraction_date, departament,city, amount,is_paid from infractions
                '''
            cursor.execute(sql)
            output = cursor.fetchall()
            for row in output:
                v = Fine(plate=row[0],infraction_date=row[1],departament=row[2],
                         city=row[3], amount=row[4],is_paid=row[5])
                sanctions.append(v)
            return sanctions

    except Exception as exc:

        reason = f"ISSUE on get_all_infractions_db: {exc}"
        print(reason)
        return False,reason
    
def get_payment_status_db():
    try:
        payments = []
        with sqlite3.connect(_path)as conn:
            cursor=conn.cursor();
            cursor.execute("""
                           select IS_PAID, count (IS_PAID) as 'count' from infractions group by is_paid
                        """)
            output = cursor.fetchall()
            p=PaymentChart(0,0)
            for row in output:
               
                if row[0]=='SI':
                    p=PaymentChart(yes=row[1], no=0)
                else:
                    p=PaymentChart(no=row[1],yes=0)
                   
                payments.append(p)
        
        return payments
    except Exception as exc:
        print(f"ISSUE on get_payment_status_db: {exc}")