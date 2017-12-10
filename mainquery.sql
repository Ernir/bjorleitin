SELECT
  beer_search_v2_untappdentity.untappd_id,
  untappd_name                        AS name,
  beer_search_v2_brewery.alias        AS brewery,
  max(price)                          AS max_price,
  min(price)                          AS min_price,
  max(volume)                         AS max_volume,
  min(volume)                         AS min_volume,
  abv,
  beer_search_v2_simplifiedstyle.name AS style_name,
  json_agg(DISTINCT container_id)     AS containers,
  rating,
  beer_search_v2_country.name         AS country_name,
  min(first_seen_at)                  AS first_seen_at,
  json_agg(stock)                     AS stock
FROM beer_search_v2_untappdentity
  INNER JOIN (SELECT
                name,
                untappd_info_id,
                price,
                volume,
                container_id,
                first_seen_at,
                jsonb_array_elements(atvr_stock) AS stock
              FROM beer_search_v2_atvrproduct
              WHERE untappd_info_id IS NOT NULL
              UNION
              SELECT
                name,
                untappd_info_id,
                price,
                volume,
                container_id,
                first_seen_at,
                json_build_object('store', 'Sérpöntunarlisti Járns og Glers', 'stock',
                                  available_in_jog :: INT) :: JSONB AS stock
              FROM beer_search_v2_jogproduct
              WHERE untappd_info_id IS NOT NULL) AS products
    ON beer_search_v2_untappdentity.id = products.untappd_info_id
  LEFT OUTER JOIN beer_search_v2_brewery
    ON beer_search_v2_untappdentity.brewery_id = beer_search_v2_brewery.id
  LEFT OUTER JOIN beer_search_v2_untappdstyle
    ON beer_search_v2_untappdentity.style_id = beer_search_v2_untappdstyle.id
  LEFT OUTER JOIN beer_search_v2_simplifiedstyle
    ON beer_search_v2_untappdstyle.simplifies_to_id = beer_search_v2_simplifiedstyle.id
  LEFT OUTER JOIN beer_search_v2_country
    ON beer_search_v2_brewery.country_id = beer_search_v2_country.id
--WHERE abv IS NOT NULL
GROUP BY beer_search_v2_untappdentity.untappd_id,
  untappd_name,
  abv,
  ibu,
  beer_search_v2_brewery.alias,
  beer_search_v2_simplifiedstyle.name,
  rating,
  beer_search_v2_country.name
ORDER BY untappd_name;
