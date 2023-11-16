insert into airline (name) values ("China Eastern");

insert into airport (name,city) values ("JFK","NYC"),("PVG","Shanghai");

insert into customer (name,email,password,building_number,street,city,state,phone_number,passport_number,passport_expiration,passport_country,date_of_birth) values 
("Koji Tadokoro","yjsnpi@gmail.com","inm1919810","3-23-14","Kitazawa, Setagaya","Tokyo","Japan", "114514", "889464","2077-08-10","Japan","1919-08-10"),
("Guoyu Hou","diangunotto@163.com","jiucaihezi","No. 12306", "Kainankai Avenue", "Anshan", "China", "1234567", "5c42dm", "2024-01-01", "China", "1996-03-08");

insert into agent (agent_email,password,booking_agent_id) values ("joebiden@usa.gov","123456789","1");

insert into works_for (agent_email,airline_name) values ("joebiden@usa.gov","China Eastern");

insert into airplane (airline_name,id,seats) values 
("China Eastern",1,200),
("China Eastern",2,216);

insert into flight (airline_name,flight_num,arrival_airport,departure_airport, plane,arrival_time, departure_time,price,status) values
("China Eastern", 909, "PVG","JFK",1,"2023-10-31 03:14:00","2023-10-31 18:14:00",300.00,"Upcoming"),
("China Eastern", 919, "PVG","JFK",2,"2023-11-05 02:14:00","2023-11-05 17:14:00",350.00,"In-progress"),
("China Eastern", 929, "JFK","PVG",1,"2023-11-20 05:14:00","2023-11-20 20:14:00",270.00,"Delayed");

insert into ticket (ticket_id,airline_name,customer_email,flight_num,purchased_date,booking_agent_id) values 
("00001","China Eastern","yjsnpi@gmail.com",909,"2023-10-02",null),
("00002","China Eastern","diangunotto@163.com",919,"2023-10-15","1");
