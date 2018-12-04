drop table v_catalog_sales, v_catalog_returns, v_inventory, v_date_dim, v_store_sales, v_item, v_warehouse;
drop table v_catalog_sales, v_catalog_returns, v_inventory, v_date_dim, v_store_sales, v_item, v_warehouse, v7, v8, v9, v10, v11, v12, v13;
drop table v_catalog_sales, v_catalog_returns, v_inventory, v_date_dim, v_store_sales, v_item, v_warehouse, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19;
drop table v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v15, v14, v16, v17, v18, v19, v20;


0:
create table v0 as select * from catalog_sales_text;

1:
create table v1 as select * from catalog_returns_text;

2:
create table v2 as select * from store_sales_text;

3:
create table v3 as select * from date_dim_text;

4:
create table v4 as
select cs_sold_date_sk
      ,cs_sold_time_sk
      ,cs_list_price
      ,cs_sales_price
      ,cs_ext_sales_price
      ,cs_ext_wholesale_cost
from v0;


5:
create table v5 as
select cs_sold_date_sk
      ,cs_sold_time_sk
from v4;


6:
create table v6 as
select cs_list_price
      ,cs_sales_price
from v4;


7:
create table v7 as
select cs_ext_sales_price
      ,cs_ext_wholesale_cost
from v4;


8:
create table v8 as
select cs_sold_date_sk
      ,cs_sold_time_sk
      ,cs_list_price
      ,cs_sales_price
      ,cr_returned_date_sk
      ,cr_return_amount
      ,cr_return_tax
from v0, v1
limit 50000000;


9:
create table v9 as
select cs_sold_date_sk
      ,cs_sales_price
      ,cr_returned_date_sk
      ,cr_return_amount
from v8;


10:
create table v10 as
select cs_sold_date_sk
      ,cr_returned_date_sk
from v9;


11:
create table v11 as
select cs_sales_price
      ,cr_return_amount
from v9;


12:
create table v12 as
select cs_sold_date_sk
      ,cr_returned_date_sk
      ,cs_sales_price
from v9;


13:
create table v13 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
      ,ss_store_sk
      ,ss_list_price
      ,ss_sales_price
from v2;


14:
create table v14 as
select ss_sold_date_sk
      ,ss_sold_time_sk
from v13;


15:
create table v15 as
select ss_item_sk
      ,ss_customer_sk
      ,ss_store_sk
from v13;


16:
create table v16 as
select ss_list_price
      ,ss_sales_price
from v13;


17:
create table v17 as
select ss_item_sk
      ,ss_customer_sk
      ,cs_sales_price
      ,cr_returned_date_sk
      ,d_date_sk
      ,d_date
from v2, v3, v8
limit 50000000;


18:
create table v18 as
select ss_item_sk
      ,cs_sales_price
      ,cr_returned_date_sk
      ,d_date_sk
      ,d_date
from v17;


19:
create table v19 as
select cs_sales_price
      ,ss_item_sk
from v18;


20:
create table v20 as
select cr_returned_date_sk
      ,d_date_sk
from v18;


21:
create table v21 as
select ss_item_sk
      ,cr_returned_date_sk
      ,d_date
from v18;