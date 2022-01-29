explain select count(distinct(customerid)) from customers
where exists(select null from orders
where orders.customerid=customers.customerid
and orders.totalamount>100
and ( EXTRACT (YEAR FROM (orders.orderdate))) = 2017 
and ( EXTRACT(month FROM (orders.orderdate))) = 1
);


CREATE INDEX
idx_amount ON orders (totalamount);

explain select count(distinct(customerid)) from customers
where exists(select null from orders
where orders.customerid=customers.customerid
and orders.totalamount>100
and ( EXTRACT (YEAR FROM (orders.orderdate))) = 2017 
and ( EXTRACT(month FROM (orders.orderdate))) = 1
);

drop index idx_amount;
CREATE INDEX
idx_amount_date ON orders (totalamount, orderdate);

explain select count(distinct(customerid)) from customers
where exists(select null from orders
where orders.customerid=customers.customerid
and orders.totalamount>100
and ( EXTRACT (YEAR FROM (orders.orderdate))) = 2017 
and ( EXTRACT(month FROM (orders.orderdate))) = 1
);


drop index idx_amount_date;
CREATE INDEX
idx_date ON orders (orderdate);


explain select count(distinct(customerid)) from customers
where exists(select null from orders
where orders.customerid=customers.customerid
and orders.totalamount>100
and ( EXTRACT (YEAR FROM (orders.orderdate))) = 2017 
and ( EXTRACT(month FROM (orders.orderdate))) = 1
);


drop index idx_date;


