drop table v0; 
drop table v1;
drop table v2;
drop table v3;
drop table v4;
drop table v5;
drop table v6;
drop table v7;
drop table v8;
drop table v9;
drop table v10;
drop table v11;
drop table v12;
drop table v13;
drop table v14;
drop table v15;
drop table v16;
drop table v17;
drop table v18;
drop table v19;
drop table v20;
drop table v21;
drop table catalog_sales_text;
drop table catalog_returns_text;
drop table store_sales_text;
drop table date_dim_text;


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
from v0 cross join v1
limit 50000;


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
from v2 cross join v3 cross join v8
limit 50000;


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