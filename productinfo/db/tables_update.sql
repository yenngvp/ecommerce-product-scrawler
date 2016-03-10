
-- Add url column to tmp_product table
ALTER TABLE `productinfo`.`tmp_product`
ADD COLUMN `url` VARCHAR(256) NULL AFTER `timestamp`,
ADD UNIQUE INDEX `url_UNIQUE` (`url` ASC);

-- Create table tmp_product_link
CREATE TABLE `tmp_product_link` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `update_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `create_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `changefreq` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- Create table domain
DROP TABLE IF EXISTS `domain`;
CREATE TABLE `domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `active` tinyint(1) DEFAULT 1,
  `sitemap_robot_urls` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sitemap_follow` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sitemap_rules` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `update_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `create_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `xpath_name` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_price` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_last_price` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_summary` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_description` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_spec` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_sku` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_image_url` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_breadcum` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_supplier` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_brand` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_category` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_subcat1` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_subcat2` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pagination` tinyint(1) DEFAULT 0,
  `max_item_perpage` int(4) DEFAULT 0,
  `pagination_regex` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_product_box` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_pagination` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `link_extract_type` tinyint(1) DEFAULT 0,
  `link_extract_regex`varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- INSERT DATA
INSERT INTO `domain`
(
  `name`,
  `url`,
  `sitemap_robot_urls`,
  `sitemap_follow`,
  `sitemap_rules`,
  `xpath_name`,
  `xpath_price`,
  `xpath_last_price`,
  `xpath_summary`,
  `xpath_description`,
  `xpath_spec`,
  `xpath_sku`,
  `xpath_image_url`,
  `xpath_breadcum`,
  `xpath_supplier`,
  `xpath_brand`,
  `xpath_category`,
  `xpath_subcat1`,
  `xpath_subcat2`,
  `pagination`,
  `max_item_perpage`,
  `pagination_regex`,
  `xpath_product_box`,
  `xpath_pagination`,
  `link_extract_type`,
  `link_extract_regex`
) VALUES
	(
	'tiki.vn',
	'http://tiki.vn',
	'["http://tiki.vn/sitemap_main_index.xml"]', 
	'["sitemap_main_index"]',
	'[("", "parse")]',  
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, "/html/body/header/div/div[2]/div[1]/nav/ul"}', 				-- xpath_category
	'{None, "/html/body/header/div/div[2]/div[1]/nav/ul/li[1]/div/ul"}',	-- xpath_subcat1
	'{None, None}',
	'1',
	'40',
	'',
	'{None, "/html/body/div[6]/div/div/div[2]/div[2]"}',
	'{None, "/html/body/div[6]/div/div/div[2]/div[2]/div[4]/ul"}',
	'1',
	''
	)
	, 
	(
	'dienmaythienhoa.vn',
	'http://www.dienmaythienhoa.vn',
	'["http://www.dienmaythienhoa.vn/robots.txt"]', 
	'[]',
	'[("products", "parse")]', 
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}'
	'{None, None}',
	'1',
	'0',
	'{None, None}',
	'1',
	''
	),
	(
	'adayroi.com',
	'https://www.adayroi.com',
	'["https://www.adayroi.com/robots.txt"]', 
	'[]',
	'[("products", "parse")]',  
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}'
	'{None, None}',
	'1',
	'0',
	'{None, None}',
	'1',
	''
	)
	,
	(
	'lazada.vn',
	'http://www.lazada.vn',
	'["http://www.lazada.vn/sitemap.xml"]', 
	'[]',
	'[("", "parse")]',  
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}'
	'{None, None}',
	'1',
	'0',
	'{None, None}',
	'1',
	''
	)
	,
	(
	'thegioididong.com',
	'https://www.thegioididong.com',
	'["https://www.thegioididong.com/sitemap/sitemap_44.xml"]', 
	'[]',
	'[("products", "parse")]',  
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}',
	'{None, None}'
	'{None, None}',
	'1',
	'0',
	'{None, None}',
	'1',
	''
	)
	;
	
	
	