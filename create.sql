create table airline (
    name varchar(50) primary key
);

create table airport (
    name varchar(50) primary key,
    city varchar(50) not null
);

create table airplane (
	airline_name varchar(50),
    foreign key (airline_name) references airline(name),
    id int not null,
    seats int not null check(seats>0),
    primary key (airline_name,id)
);

create table flight (
	airline_name varchar(50),
    foreign key (airline_name) references airline(name),
    flight_num int not null,
    departure_airport varchar(50),
    arrival_airport varchar(50),
    plane int,
    foreign key (arrival_airport) references airport(name),
	foreign key (departure_airport) references airport(name),
	foreign key (airline_name,plane) references airplane(airline_name,id),
    arrival_time timestamp not null, 
    departure_time timestamp not null,
    price decimal(10,2) not null check (price>=0),
    status varchar(50) not null,
    primary key (airline_name,flight_num)
);

create table agent (
    agent_email varchar(50) primary key,
    password varchar(50) not null, -- consider hashing for security
    booking_agent_id int(50) AUTO_INCREMENT unique not null
);

create table works_for (
	airline_name varchar(50),
    agent_email varchar(50),
    foreign key (airline_name) references airline(name),
    foreign key (agent_email) references agent(agent_email),
    primary key (airline_name, agent_email)
);

create table customer (
    name varchar(50) not null,
    email varchar(50) primary key,
    password varchar(50) not null,
    building_number varchar(10) not null,
    street varchar(50) not null,
    city varchar(50) not null,
    state varchar(50) not null,
    phone_number varchar(20) not null,
    passport_number varchar(20) not null,
    passport_expiration date not null,
    passport_country varchar(50) not null,
    date_of_birth date not null
);

create table ticket (
	airline_name varchar(50),
    customer_email varchar(50),
    flight_num int,
    booking_agent_id varchar(50),
    ticket_id int(50) auto_increment primary key,
    foreign key (airline_name) references airline(name),
    foreign key (customer_email) references customer(email),
    foreign key (airline_name,flight_num) references flight(airline_name,flight_num),
    commission decimal(11,4) DEFAULT 0,
    purchased_date date not null
);

create table airline_staff (
	airline_name varchar(50),
    username varchar(50) primary key,
    foreign key (airline_name) references airline(name),
    password varchar(50) not null, 
    first_name varchar(20) not null, 
    last_name varchar(20) not null, 
    date_of_birth date not null
);

create table permission (
	username varchar(50),
    foreign key (username) references airline_staff(username),
    permission varchar(50),
    primary key (username,permission)
);