--Tarea G
--Creacion indice
CREATE INDEX
idx_status ON orders (status);
--Primera consulta
explain select count(*)
from orders
where status is null;
--Segunda consulta
explain select count(*)
from orders
where status ='Shipped';
--Analyze de orders
analyze orders;
--Primera consulta
explain select count(*)
from orders
where status is null;
--Segunda consulta
explain select count(*)
from orders
where status ='Shipped';
--Tercera consula
explain select count(*)
from orders
where status ='Paid';
--Cuarta consulta
explain select count(*)
from orders
where status ='Processed';