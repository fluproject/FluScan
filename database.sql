CREATE DATABASE IF NOT EXISTS `fluscan` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `fluscan`;

CREATE TABLE `t_geo` (
  `id` int(11) NOT NULL,
  `host` int(11) DEFAULT NULL,
  `city` text,
  `region_code` text,
  `area_code` text,
  `time_zone` text,
  `dma_code` text,
  `metro_code` text,
  `country_code3` text,
  `latitude` text,
  `postal_code` text,
  `longitude` text,
  `country_code` text,
  `country_name` text,
  `continent` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `t_hosts` (
  `id` int(11) NOT NULL,
  `ip` varchar(250) DEFAULT NULL,
  `host` text,
  `date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `t_ports` (
  `id` int(11) NOT NULL,
  `host` int(11) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `service` text,
  `banner` text,
  `date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `t_geo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `host` (`host`);

ALTER TABLE `t_hosts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ip` (`ip`);

ALTER TABLE `t_ports`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `host` (`host`,`port`);