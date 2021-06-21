# weather_app
Charts with weather parameters

Create folders ./posgressql/data and ./posgressql/dumps

Build containers:

  docker-compose -f docker-compose.dev.yml build db
  docker-compose -f docker-compose.dev.yml build backend
  docker-compose -f docker-compose.dev.yml build frontend

Up all containers:

  docker-compose -f docker-compose.dev.yml up db backend
  docker-compose -f docker-compose.dev.yml up frontend

To make test db data: 
  
  Open backend container: docker exec -it container_name /bin/bash

  Run: 
    python manage.py shell
    import init_db_data
    init_db_data.generate_data()
   
 Use app. You are breathtaking!
  
