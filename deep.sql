14 (7*9):
create materialized view v14 as
select i_item_desc 
       ,v7.i_category 
       ,v7.i_class
       i_product_name
from v7, v9;



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
from v14, v10;


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
limit 50000000;

19(15*16):
create materialized view v19 as 
select  inv_after
        ,sum_agg
        i_item_id
from v15, v16
limit 50000000;