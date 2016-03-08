
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
  `xpath_category` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_supplier` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `xpath_brand` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
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
  `xpath_category`,
  `xpath_supplier`,
  `xpath_brand`
) VALUES (
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
	'{None, None}'),
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
	'{None, None}')
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
	'{None, None}')
	,
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
	'{None, None}')
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
	'{None, None}')
	;
	
	
	