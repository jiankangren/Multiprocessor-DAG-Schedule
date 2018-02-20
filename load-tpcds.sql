copy call_center from '/tmp/data-5G/handled/call_center.dat' with delimiter as '|' NULL '';
    copy catalog_page from '/tmp/data-5G/handled/catalog_page.dat' with delimiter as '|' NULL '';
    copy catalog_returns from '/tmp/data-5G/handled/catalog_returns.dat' with delimiter as '|' NULL '';
    copy catalog_sales from '/tmp/data-5G/handled/catalog_sales.dat' with delimiter as '|' NULL '';
    copy customer from '/tmp/data-5G/handled/customer.dat' with delimiter as '|' NULL '';
    copy customer_address from '/tmp/data-5G/handled/customer_address.dat' with delimiter as '|' NULL '';
    copy customer_demographics from '/tmp/data-5G/handled/customer_demographics.dat' with delimiter as '|' NULL '';
    copy date_dim from '/tmp/data-5G/handled/date_dim.dat' with delimiter as '|' NULL '';
    copy dbgen_version from '/tmp/data-5G/handled/dbgen_version.dat' with delimiter as '|' NULL '';
    copy household_demographics from '/tmp/data-5G/handled/household_demographics.dat' with delimiter as '|' NULL '';
    copy income_band from '/tmp/data-5G/handled/income_band.dat' with delimiter as '|' NULL '';
    copy inventory from '/tmp/data-5G/handled/inventory.dat' with delimiter as '|' NULL '';
    copy item from '/tmp/data-5G/handled/item.dat' with delimiter as '|' NULL '';
    copy promotion from '/tmp/data-5G/handled/promotion.dat' with delimiter as '|' NULL '';
    copy reason from '/tmp/data-5G/handled/reason.dat' with delimiter as '|' NULL '';
    copy ship_mode from '/tmp/data-5G/handled/ship_mode.dat' with delimiter as '|' NULL '';
    copy store from '/tmp/data-5G/handled/store.dat' with delimiter as '|' NULL '';
    copy store_returns from '/tmp/data-5G/handled/store_returns.dat' with delimiter as '|' NULL '';
    copy store_sales from '/tmp/data-5G/handled/store_sales.dat' with delimiter as '|' NULL '';
    copy time_dim from '/tmp/data-5G/handled/time_dim.dat' with delimiter as '|' NULL '';
    copy warehouse from '/tmp/data-5G/handled/warehouse.dat' with delimiter as '|' NULL '';
    copy web_page from '/tmp/data-5G/handled/web_page.dat' with delimiter as '|' NULL '';
    copy web_returns from '/tmp/data-5G/handled/web_returns.dat' with delimiter as '|' NULL '';
    copy web_sales from '/tmp/data-5G/handled/web_sales.dat' with delimiter as '|' NULL '';
    copy web_site from '/tmp/data-5G/handled/web_site.dat' with delimiter as '|' NULL '';



    SELECT nspname || '.' || relname AS "relation",
    pg_size_pretty(pg_relation_size(C.oid)) AS "size"
  FROM pg_class C
  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
  WHERE nspname NOT IN ('pg_catalog', 'information_schema')
  ORDER BY pg_relation_size(C.oid) DESC;



  http://blog.csdn.net/u011563666/article/details/78751584
  http://www.voidcn.com/article/p-fxpwszws-bhw.html
  https://stackoverflow.com/questions/19463074/postgres-error-could-not-open-file-for-reading-permission-denied