# guane-intern-fastapi

## Database

The database used was postgres v-10.12

### Database creation

CREATE TABLE dogs (id serial PRIMARY KEY, name VARCHAR(20) not null, picture VARCHAR(100), create_date TIMESTAMP not null, update_date TIMESTAMP not null, is_adopted BOOLEAN, age SMALLINT, weight FLOAT);

### Database inserts

INSERT INTO dogs (name, picture, create_date, update_date, is_adopted, age, weight) VALUES ('Luzy', 'https://dog.ceo/api/breeds/image/random', '2020-05-21 10:58:55.104954', '2020-05-21 10:59:55.104954', True, 10, 10.2);

INSERT INTO dogs (name, picture, create_date, update_date, is_adopted, age, weight) VALUES ('Bruna', 'https://images.dog.ceo/breeds/hound-ibizan/n02091244_5943.jpg', '2020-04-21 10:58:55.104954', '2020-05-21 10:59:55.104954', True, 8, 6.2);
