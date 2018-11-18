drop materialized view v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15;


0:
create table v0 as select * from store_sales_text;


1:
create table v1 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
      ,ss_cdemo_sk
      ,ss_hdemo_sk
      ,ss_addr_sk
      ,ss_store_sk
      ,ss_promo_sk
      ,ss_ticket_number
      ,ss_quantity
      ,ss_wholesale_cost
      ,ss_list_price
      ,ss_sales_price
      ,ss_ext_discount_amt
      ,ss_ext_sales_price
      ,ss_ext_wholesale_cost
      ,ss_ext_list_price
      ,ss_ext_tax
      ,ss_coupon_amt
      ,ss_net_paid
      ,ss_net_paid_inc_tax
      ,ss_net_profit
from v0;


2:
create table v2 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
      ,ss_cdemo_sk
      ,ss_hdemo_sk
      ,ss_addr_sk
      ,ss_store_sk
      ,ss_promo_sk
      ,ss_ticket_number
      ,ss_quantity
      ,ss_wholesale_cost
      ,ss_list_price
      ,ss_sales_price
      ,ss_ext_discount_amt
      ,ss_ext_sales_price
      ,ss_ext_wholesale_cost
      ,ss_ext_list_price
      ,ss_ext_tax
      ,ss_coupon_amt
from v1;


3:
create table v3 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
      ,ss_cdemo_sk
      ,ss_hdemo_sk
      ,ss_addr_sk
      ,ss_store_sk
      ,ss_promo_sk
      ,ss_ticket_number
      ,ss_quantity
      ,ss_wholesale_cost
      ,ss_list_price
      ,ss_sales_price
      ,ss_ext_discount_amt
      ,ss_ext_sales_price
from v2;



4:
create table v4 as select * from inventory_text;



5:
create table v5 as
select inv_date_sk
      ,inv_item_sk
      ,inv_warehouse_sk
      ,inv_quantity_on_hand
from v4;


6:
create table v6 as
select inv_date_sk
      ,inv_item_sk
      ,inv_quantity_on_hand
from v5;


7:
create table v7 as
select * from v2, v5 
where ss_item_sk = inv_item_sk
limit 10000000;


8:
create table v8 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
      ,ss_cdemo_sk
      ,ss_hdemo_sk
      ,ss_addr_sk
      ,ss_store_sk
      ,inv_date_sk
      ,inv_warehouse_sk
from v7;


9:
create table v9 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
      ,ss_cdemo_sk
from v8;


10:
create table v10 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
from v9;


11:
create table v11 as
select * from v10;


12:
create table v12 as
select ss_list_price
      ,ss_sales_price
      ,ss_ext_discount_amt
      ,ss_ext_sales_price
      ,ss_ext_wholesale_cost
      ,ss_ext_list_price
      ,ss_ext_tax
      ,ss_coupon_amt
      ,ss_item_sk
      ,inv_warehouse_sk
      ,inv_quantity_on_hand
from v7;


13:
create table v13 as
select ss_ext_list_price
      ,ss_ext_tax
      ,ss_coupon_amt
      ,ss_item_sk
      ,inv_warehouse_sk
      ,inv_quantity_on_hand
from v12;


14:
create table v14 as
select ss_item_sk
      ,inv_warehouse_sk
      ,inv_quantity_on_hand
from v13;


15:
create table v15 as
select ss_item_sk
from v14;



create table inventory_text
(
inv_date_sk               int,
inv_item_sk               int,
inv_warehouse_sk          int,
inv_quantity_on_hand      bigint
)
USING csv
OPTIONS(header "false", delimiter "|", path "/home/tpcds/inventory.dat");

cache table inventory_text;


select count(*) from inventory_text where inv_date_sk = 2450815;



inv = sc.textFile('hdfs://home/tpcds/store_sales.dat')
inv_t = sales.map(lambda x: x.split('|')).map(lambda x: Row(id=x[0], c1=x[1], c2=x[2], c3=x[3]))
tbl = sqlContext.inferSchema(sales_t)
tbl.registerTempTable('inventory')
sqlContext.sql('select * from inventory').collect()


