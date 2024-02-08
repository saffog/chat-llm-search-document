class User:
    def __init__(self, full_name, email, role, date_start, country, password) -> None:
        self.full_name = full_name
        self.email = email
        self.role = role
        self.date_start = date_start
        self.country = country
        self.password = password
        
    def to_dict(self):
        return {
            "fullName": self.full_name,
            "email": self.email,
            "role": self.role,
            "dateStart": self.date_start,
            "country": self.country,
            "password": self.password
        }
        

users = [
    User(full_name='Juan Pérez', email='juan.perez@baufest.com', role='Desarrollador Frontend',
        date_start='2022-03-01', country='México', password='password123'),
    User(full_name='Ana García', email='ana.garcia@baufest.com', role='Desarrollador Backend',
        date_start='2021-09-15', country='España', password='password123'),
    User(full_name='Carlos Rodríguez', email='carlos.rodriguez@baufest.com', role='Diseñador UX/UI',
        date_start='2022-01-10', country='Argentina', password='password123'),
    User(full_name='Laura Méndez', email='laura.mendez@baufest.com', role='Gerente de Proyectos',
        date_start='2021-07-05', country='Colombia', password='password123'),
    User(full_name='Daniel González', email='daniel.gonzalez@baufest.com', role='Desarrollador Fullstack',
        date_start='2022-04-20', country='Chile', password='password123'),
    User(full_name='Silvina Pliego', email='silvina.pliego@baufest.com', role='Desarrollador Fullstack',
        date_start='2022-01-20', country='Uruguay', password='password123')
]