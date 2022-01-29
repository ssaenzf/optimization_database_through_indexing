ALTER TABLE inventory
ADD CONSTRAINT	foreign_key_inventory
       FOREIGN KEY (prod_id) REFERENCES products (prod_id) ON DELETE CASCADE;  
ALTER TABLE orderdetail
ADD CONSTRAINT	foreign_key_orderdetail_order
       FOREIGN KEY (orderid) REFERENCES orders (orderid) ON DELETE CASCADE; 
ALTER TABLE orderdetail 
ADD CONSTRAINT	foreign_key_orderdetail_prod
       FOREIGN KEY (prod_id) REFERENCES products (prod_id) ON DELETE CASCADE;  
ALTER TABLE orders
ADD CONSTRAINT	foreign_key_orders_customerid
       FOREIGN KEY (customerid) REFERENCES customers (customerid) ON DELETE CASCADE; 
ALTER TABLE imdb_actormovies
ADD CONSTRAINT	foreign_key_imdb_actormovies_actorid
       FOREIGN KEY (actorid) REFERENCES imdb_actors (actorid) ON DELETE CASCADE; 
ALTER TABLE imdb_actormovies 
ADD CONSTRAINT	foreign_key_imdb_actormovies_movieid
       FOREIGN KEY (movieid) REFERENCES imdb_movies (movieid) ON DELETE CASCADE;  
ALTER TABLE imdb_actormovies
  add primary key (actorid, movieid);

SELECT orderid, prod_id, count(*) as contador
INTO holdkey
FROM orderdetail
GROUP BY orderid, prod_id
HAVING count(*) > 1;

SELECT DISTINCT orderdetail.*
INTO holddups
FROM orderdetail, holdkey
WHERE orderdetail.orderid = holdkey.orderid
AND orderdetail.prod_id = holdkey.prod_id;

DELETE 
FROM orderdetail using holdkey
where orderdetail.prod_id=holdkey.prod_id and orderdetail.orderid=holdkey.orderid;

ALTER TABLE orderdetail
  add primary key (orderid, prod_id);
drop table holddups;
drop table holdkey;

 
