drop materialized view v_catalog_sales, v_catalog_returns, v_inventory, v_date_dim, v_store_sales, v_item, v_warehouse;
drop materialized view v_catalog_sales, v_catalog_returns, v_inventory, v_date_dim, v_store_sales, v_item, v_warehouse, v7, v8, v9, v10, v11, v12, v13;
drop materialized view v_catalog_sales, v_catalog_returns, v_inventory, v_date_dim, v_store_sales, v_item, v_warehouse, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19;
drop materialized view v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v15, v16, v17, v18, v19, v20, v21;


0:
create materialized view v0 as select * from catalog_sales;

1:
create materialized view v1 as select * from catalog_returns;

2:
create materialized view v2 as select * from store_sales;

3:
create materialized view v3 as select * from date_dim;

4:
create materialized view v4 as
select cs_sold_date_sk
      ,cs_sold_time_sk
      ,cs_list_price
      ,cs_sales_price
      ,cs_ext_sales_price
      ,cs_ext_wholesale_cost
from v0;


5:
create materialized view v5 as
select cs_sold_date_sk
      ,cs_sold_time_sk
from v4;


6:
create materialized view v6 as
select cs_list_price
      ,cs_sales_price
from v4;


7:
create materialized view v7 as
select cs_ext_sales_price
      ,cs_ext_wholesale_cost
from v4;


8:
create materialized view v8 as
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
create materialized view v9 as
select cs_sold_date_sk
      ,cs_sales_price
      ,cr_returned_date_sk
      ,cr_return_amount
from v8;


10:
create materialized view v10 as
select cs_sold_date_sk
      ,cr_returned_date_sk
from v9;


11:
create materialized view v11 as
select cs_sales_price
      ,cr_return_amount
from v9;


12:
create materialized view v12 as
select cs_sold_date_sk
      ,cr_returned_date_sk
      ,cs_sales_price
from v9;


13:
create materialized view v13 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
      ,ss_store_sk
      ,ss_list_price
      ,ss_sales_price
from v2;


14:
create materialized view v14 as
select ss_sold_date_sk
      ,ss_sold_time_sk
from v13;


15:
create materialized view v15 as
select ss_item_sk
      ,ss_customer_sk
      ,ss_store_sk
from v13;


16:
create materialized view v16 as
select ss_list_price
      ,ss_sales_price
from v13;


17:
create materialized view v17 as
select ss_item_sk
      ,ss_customer_sk
      ,cs_sales_price
      ,cr_returned_date_sk
      ,d_date_sk
      ,d_date
from v2, v3, v8
limit 50000000;


18:
create materialized view v18 as
select ss_item_sk
      ,cs_sales_price
      ,cr_returned_date_sk
      ,d_date_sk
      ,d_date
from v17;


19:
create materialized view v19 as
select cs_sales_price
      ,ss_item_sk
from v18;


20:
create materialized view v20 as
select cr_returned_date_sk
      ,d_date_sk
from v18;


21:
create materialized view v21 as
select ss_item_sk
      ,cr_returned_date_sk
      ,d_date
from v18;