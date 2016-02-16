
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
CREATE TABLE `domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sitemap_robot` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
