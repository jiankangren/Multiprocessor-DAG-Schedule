drop materialized view v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19;


0:
create materialized view v0 as select * from catalog_sales;

1:
create materialized view v1 as select * from catalog_returns;

2:
create materialized view v2 as select * from store_sales;

3:
create materialized view v3 as select * from date_dim;

4:
create materialized view v4 as select * from inventory;

5:
create materialized view v5 as select * from web_sales;

6:
create materialized view v6 as select * from store_returns;

7:
create materialized view v7 as select * from customer;

8:
create materialized view v8 as select * from customer_address;

9:
create materialized view v9 as select * from customer_demographics;

10:
create materialized view v10 as select * from web_returns;

11:
create materialized view v11 as select * from item;


12:
create materialized view v12 as
select cs_sold_date_sk
      ,cs_sales_price
      ,cr_returned_date_sk
      ,cr_return_amount
      ,ss_item_sk
      ,ss_customer_sk
      ,d_date_sk
      ,d_date
from v0, v1, v2, v3
limit 50000000;


13:
create materialized view v13 as
select cs_sold_date_sk
      ,cr_returned_date_sk
      ,ss_item_sk
      ,d_date_sk
from v12;


14:
create materialized view v14 as
select v12.cs_sold_date_sk
      ,v12.cs_sales_price
      ,v12.cr_returned_date_sk
      ,v13.ss_item_sk
from v12, v13
limit 50000000;


15:
create materialized view v15 as
select v12.cr_returned_date_sk
      ,v12.cr_return_amount
from v12
limit 50000000;


16:
create materialized view v16 as
select v12.ss_item_sk
      ,v12.ss_customer_sk
from v12
limit 50000000;


17:
create materialized view v17 as
select v12.d_date_sk
      ,v12.d_date
from v12
limit 50000000;


18:
create materialized view v18 as
select v12.cs_sales_price
      ,v12.cr_returned_date_sk
      ,v14.ss_item_sk
      ,v15.cr_return_amount
      ,v16.ss_customer_sk
      ,v17.d_date
      ,v19.i_item_id
from v12, v14, v15, v16, v17, v19
limit 5000000;


19:
create materialized view v19 as
select inv_item_sk
      ,ws_item_sk
      ,sr_ticket_number
      ,c_customer_sk
      ,ca_address_id
      ,cd_education_status
      ,wr_returned_time_sk
      ,i_item_id
from v4, v5, v6, v7, v8, v9, v10, v11
limit 60000000;