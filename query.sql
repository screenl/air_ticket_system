select * from flight where status="Upcoming";
/*  +---------------+------------+-----------------+-------------------+-------+---------------------+---------------------+--------+----------+
    | airline_name  | flight_num | arrival_airport | departure_airport | plane | arrival_time        | departure_time      | price  | status   |
    +---------------+------------+-----------------+-------------------+-------+---------------------+---------------------+--------+----------+
    | China Eastern |        909 | PVG             | JFK               |     1 | 2023-10-31 03:14:00 | 2023-10-31 18:14:00 | 300.00 | Upcoming |
    +---------------+------------+-----------------+-------------------+-------+---------------------+---------------------+--------+----------+
    1 row in set (0.00 sec) */

select * from flight where status="Delayed";
/*  +---------------+------------+-----------------+-------------------+-------+---------------------+---------------------+--------+---------+
    | airline_name  | flight_num | arrival_airport | departure_airport | plane | arrival_time        | departure_time      | price  | status  |
    +---------------+------------+-----------------+-------------------+-------+---------------------+---------------------+--------+---------+
    | China Eastern |        929 | JFK             | PVG               |     1 | 2023-11-20 05:14:00 | 2023-11-20 20:14:00 | 270.00 | Delayed |
    +---------------+------------+-----------------+-------------------+-------+---------------------+---------------------+--------+---------+
    1 row in set (0.00 sec) */

select name from customer join ticket on customer.email = ticket.customer_email where booking_agent_id is not null;
/*  +-----------+
    | name      |
    +-----------+
    | Guoyu Hou |
    +-----------+
    1 row in set (0.00 sec) */

select * from airplane where airline_name="China Eastern";
/*  +---------------+----+-------+
    | airline_name  | id | seats |
    +---------------+----+-------+
    | China Eastern |  1 |   200 |
    | China Eastern |  2 |   216 |
    +---------------+----+-------+
    2 rows in set (0.00 sec) */
