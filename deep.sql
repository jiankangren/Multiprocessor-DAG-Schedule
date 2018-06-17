drop materialized view v_catalog_sales, v_catalog_returns, v_inventory, v_date_dim, v_store_sales, v_item, v_warehouse;
drop materialized view v_catalog_sales, v_catalog_returns, v_inventory, v_date_dim, v_store_sales, v_item, v_warehouse, v7, v8, v9, v10, v11, v12, v13;
drop materialized view v_catalog_sales, v_catalog_returns, v_inventory, v_date_dim, v_store_sales, v_item, v_warehouse, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18;


0:
create materialized view v_catalog_sales as select * from catalog_sales;

1:
create materialized view v_catalog_returns as select * from catalog_returns;

2:
create materialized view v_inventory as select * from inventory;

3:
create materialized view v_date_dim as select * from date_dim;

4:
create materialized view v_store_sales as select * from store_sales;

5:
create materialized view v_item as select * from item;

6:
create materialized view v_warehouse as select * from warehouse;

7:
create materialized view v7 as 
select  i_item_desc 
       ,i_category 
       ,i_class 
       ,i_current_price
       ,sum(cs_ext_sales_price) as itemrevenue 
       ,sum(cs_ext_sales_price)*100/sum(sum(cs_ext_sales_price)) over
           (partition by i_class) as revenueratio
 from v_catalog_sales
     ,v_item 
     ,v_date_dim
 where cs_item_sk = i_item_sk 
   and i_category in ('Jewelry', 'Sports', 'Books')
   and cs_sold_date_sk = d_date_sk
 and d_date between cast('2001-01-12' as date) 
        and (cast('2001-01-12' as date) + 30)
 group by i_item_id
         ,i_item_desc 
         ,i_category
         ,i_class
         ,i_current_price
 order by i_category
         ,i_class
         ,i_item_id
         ,i_item_desc
         ,revenueratio
limit 100;


8:
create materialized view v8 as 
select  *
 from(select w_warehouse_name
            ,i_item_id
            ,sum(case when (cast(d_date as date) < cast ('1998-04-08' as date))
                  then inv_quantity_on_hand 
                      else 0 end) as inv_before
            ,sum(case when (cast(d_date as date) >= cast ('1998-04-08' as date))
                      then inv_quantity_on_hand 
                      else 0 end) as inv_after
   from v_inventory
       ,v_warehouse
       ,v_item
       ,v_date_dim
   where i_current_price between 0.99 and 1.49
     and i_item_sk          = inv_item_sk
     and inv_warehouse_sk   = w_warehouse_sk
     and inv_date_sk    = d_date_sk
     and d_date between (cast ('1998-04-08' as date) - 30)
                    and (cast ('1998-04-08' as date) + 30)
   group by w_warehouse_name, i_item_id) x
 where (case when inv_before > 0 
             then inv_after / inv_before 
             else null
             end) between 2.0/3.0 and 3.0/2.0
 order by w_warehouse_name
         ,i_item_id
 limit 100;


 9:
 create materialized view v9 as
 select  i_product_name
             ,i_brand
             ,i_class
             ,i_category
             ,avg(inv_quantity_on_hand) qoh
       from v_inventory
           ,v_date_dim
           ,v_item
           ,v_warehouse
       where inv_date_sk=d_date_sk
              and inv_item_sk=i_item_sk
              and inv_warehouse_sk = w_warehouse_sk
              and d_month_seq between 1176 and 1176 + 11
       group by i_product_name
                       ,i_brand
                       ,i_class
                       ,i_category
order by qoh, i_product_name, i_brand, i_class, i_category
limit 100;


9v2:
 create materialized view v9 as
 select  i_product_name
             ,i_brand
             ,i_class
             ,i_category
             ,inv_quantity_on_hand qoh
             ,d_date_id
             ,w_street_number
             ,w_street_name
             ,w_street_type
       from v_inventory
           ,v_date_dim
           ,v_item
           ,v_warehouse
limit 1000000;

10:
create materialized view v10 as
select  dt.d_year 
       ,v_item.i_brand_id brand_id 
       ,v_item.i_brand brand
       ,sum(ss_ext_sales_price) sum_agg
from  v_date_dim dt 
      ,v_store_sales
      ,v_item
 where dt.d_date_sk = v_store_sales.ss_sold_date_sk
   and v_store_sales.ss_item_sk = v_item.i_item_sk
   and v_item.i_manufact_id = 436
   and dt.d_moy=12
 group by dt.d_year
      ,v_item.i_brand
      ,v_item.i_brand_id
 order by dt.d_year
         ,sum_agg desc
         ,brand_id
 limit 100;

 11:
 create materialized view v11 as
 select  
   w_state
  ,i_item_id
  ,sum(case when (cast(d_date as date) < cast ('1998-04-08' as date)) 
    then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end) as sales_before
  ,sum(case when (cast(d_date as date) >= cast ('1998-04-08' as date)) 
    then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end) as sales_after
 from
   v_catalog_sales left outer join v_catalog_returns on
       (cs_order_number = cr_order_number 
        and cs_item_sk = cr_item_sk)
  ,v_warehouse 
  ,v_item
  ,v_date_dim
 where
     i_current_price between 0.99 and 1.49
 and i_item_sk          = cs_item_sk
 and cs_warehouse_sk    = w_warehouse_sk 
 and cs_sold_date_sk    = d_date_sk
 and d_date between (cast ('1998-04-08' as date) - 30)
                and (cast ('1998-04-08' as date) + 30) 
 group by
    w_state,i_item_id
 order by w_state,i_item_id
limit 100;


12:
create materialized view v12 as 
select  dt.d_year
  ,v_item.i_category_id
  ,v_item.i_category
  ,sum(ss_ext_sales_price)
 from   v_date_dim dt
  ,v_store_sales
  ,v_item
 where dt.d_date_sk = v_store_sales.ss_sold_date_sk
  and v_store_sales.ss_item_sk = v_item.i_item_sk
  and v_item.i_manager_id = 1   
  and dt.d_moy=12
  and dt.d_year=1998
 group by   dt.d_year
    ,v_item.i_category_id
    ,v_item.i_category
 order by       sum(ss_ext_sales_price) desc,dt.d_year
    ,v_item.i_category_id
    ,v_item.i_category
limit 100;


13:
create materialized view v13 as
select i_item_desc 
      ,i_category 
      ,i_class 
      ,i_current_price
      ,sum(ss_ext_sales_price) as itemrevenue 
      ,sum(ss_ext_sales_price)*100/sum(sum(ss_ext_sales_price)) over
          (partition by i_class) as revenueratio
from  
  v_store_sales
      ,v_item 
      ,v_date_dim
where 
  ss_item_sk = i_item_sk 
    and i_category in ('Jewelry', 'Sports', 'Books')
    and ss_sold_date_sk = d_date_sk
  and d_date between cast('2001-01-12' as date) 
        and (cast('2001-01-12' as date) + 30)
group by 
  i_item_id
        ,i_item_desc 
        ,i_category
        ,i_class
        ,i_current_price
order by 
  i_category
        ,i_class
        ,i_item_id
        ,i_item_desc
        ,revenueratio;


14 (7*9):
create materialized view v14 as
select i_item_desc 
       ,v7.i_category 
       ,v7.i_class
       i_product_name
from v7, v9
limit 1000000;



15(8*10):
create materialized view v15 as
select w_warehouse_name
            ,i_item_id
            ,inv_before
            ,inv_after
            ,sum_agg
from v8, v10;



16(11*13):
create materialized view v16 as
select w_state
  ,i_item_id
  ,sales_before
  ,i_item_desc 
  ,i_category 
  ,i_class 
  ,i_current_price
  ,itemrevenue
  ,revenueratio
from v11, v13;

17(14*10):
create materialized view v17 as
select i_item_desc 
       ,i_category 
       ,brand_id
       ,sum_agg
from v14, v10
limit 1000000;



18(14*15):
create materialized view v18 as 
select i_item_desc 
       ,i_category 
       ,i_product_name
       ,w_warehouse_name
       ,i_item_id
       ,inv_before 
       ,inv_after
       ,sum_agg
from v14, v15
limit 1000000;

19(15*16):
create materialized view v19 as 
select  inv_after
        ,sum_agg
        i_item_id
from v15, v16
limit 1000000;