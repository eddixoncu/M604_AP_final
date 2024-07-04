class Vehicle:
    def __init__(self, plate, brand) -> None:
        self.plate = plate
        self.brand = brand
        
class Owner:
    def __init__(self,document_number, names, last_names) -> None:
        self.document_number= document_number
        self.names =names
        self.last_names=last_names


class VehiclePerson:
    def __init__(self, plate, brand, document_number, full_name) -> None:
        self.plate = plate
        self.brand = brand
        self.document_number= document_number
        self.full_name = full_name

class Fine:
    def __init__(self,plate, infraction_date, departament,city, amount,is_paid) -> None:
        self.plate=plate
        self.infraction_date=infraction_date
        self.departament=departament
        self.city=city
        self.amount=amount
        self.is_paid=is_paid

class PaymentChart:
    def __init__(self, yes, no)-> None:
        self.yes= yes
        self.no=no
    
    def to_dict(self):
        return {
            'yes': self.yes,
            'no': self.no,
        } 